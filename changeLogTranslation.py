from modules.ChangeLogs import ChangeLogs
from modules.Ad import Ad
from modules.AsyncCampaign import AsyncCampaign
from modules.Placements import Placement
from modules.Creative import Creative
from modules.Sites import Sites
from modules.ssms_connector import SSMSConnector
import re
import datetime

def getBeginningofWeek():
    from datetime import datetime, timedelta
    currentdate = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return currentdate

currentTime = getBeginningofWeek()
initialChangeLog = ChangeLogs()
initialSession = initialChangeLog.session
initialEventLoop = initialChangeLog.eventLoop
ssms = SSMSConnector()
def TrueToYes(boolean):
    if boolean == True:
        return "Yes"
    else:
        return "No"
def checkSession(obj):
    global initialSession
    if obj.session != initialSession:
        initialSession = obj.session
    return obj
def extractAdInfo(adObject):
    try:
        hardCutoff = adObject.body["deliverySchedule"]["hardCutoff"]
    except:
        hardCutoff = True
    finalAdObject = {"Ad_ID":adObject.body["id"],
    "Ad_Name":adObject.body["name"],
    "Ad_Type":adObject.body["type"],
    "Ad_Is_Active":TrueToYes(adObject.body["active"]),
    "Ad_Start_Time":adObject.body["startTime"],
    "Ad_End_Time":adObject.body["endTime"],
    "Hard_Cut_Off":TrueToYes(hardCutoff)
    }
    return finalAdObject 
def extractPlacementInfo(placementObject):
    finalPlacementObject = {
        "Placement_ID":placementObject.body["id"],
        "Placement_Name":placementObject.body["name"],
        "Placement_Start_Date":placementObject.body["pricingSchedule"]["startDate"],
        "Placement_End_Date":placementObject.body["pricingSchedule"]["endDate"],
        "Placement_Compatibility":placementObject.body["compatibility"]
    }
    return finalPlacementObject
def extractSiteInfo(siteObject):
    siteName = "{0} ({1})".format(siteObject.body["name"], siteObject.body["id"])
    finalSiteObject = {
        "Site":siteName
    }
    return finalSiteObject
def extractCampaignInfo(campaignObject):
    finalCampaignObject = {
        "Campaign_ID":campaignObject.body["id"],
        "Campaign_Name":re.sub("'","''",campaignObject.body["name"])
    }
    return finalCampaignObject
def extractCreativeInfo(creativeObject):
                     
    finalCreativeObject = {
        "Creative_ID":creativeObject.body["id"],
        "Creative_Name":creativeObject.body["name"],
        "Creative_Type":creativeObject.body["type"],
        "Creative_Click_Through_URL":creativeObject.body["clickthrough"],
        "Creative_Date":creativeObject.body["startTime"]
    }
    return finalCreativeObject
def generateInsertQuery(finalObject):
        query = "Insert Into glops.AdOps_Active_Campaigns_Report_Staging (Campaign_Name, Campaign_ID, Site, Placement_ID, Placement_Name, Placement_Start_Date, Placement_End_Date, Ad_ID, Ad_Name, Ad_Type, Ad_Is_Active, Ad_Start_Time, Ad_End_Time, Hard_Cut_Off, Creative_ID, Creative_Name, Creative_Type, Creative_Click_Through_URL, Creative_Date, Placement_Compatibility) Values ('{Campaign_Name}',{Campaign_ID},'{Site}',{Placement_ID},'{Placement_Name}','{Placement_Start_Date}','{Placement_End_Date}',{Ad_ID},'{Ad_Name}','{Ad_Type}','{Ad_Is_Active}','{Ad_Start_Time}','{Ad_End_Time}','{Hard_Cut_Off}',{Creative_ID},'{Creative_Name}','{Creative_Type}','{Creative_Click_Through_URL}','{Creative_Date}','{Placement_Compatibility}')"
        query= query.format(**finalObject)
        ssms.runQuery(query)

def DeactivateRows(whereClauseObject):
    whereClause = "where "
    for column in whereClauseObject:
        if whereClause != "where ":
            whereClause += " and "
        whereClause += "{0} = {1}".format(column,whereClauseObject[column])
    query = "update glops.AdOps_Active_Campaigns_Report_Staging set Status = 'Inactive',Updated_By = suser_sname() ,Update_Date = getdate() {whereClause}"
    query = query.format(whereClause=whereClause)
    ssms.runQuery(query)
def updateRows(updateObject,whereClauseObject):
    whereClause = "where "
    for column in whereClauseObject:
        if whereClause != "where ":
            whereClause += " and "
        whereClause += "{0} = {1}".format(column,whereClauseObject[column])
    toUpdate = ""
    for field in updateObject:
        try:
            int(updateObject[field])
            toUpdate += " {0} = {1}, ".format(field,updateObject[field])
        except:
            toUpdate += " {0} = '{1}', ".format(field,updateObject[field])
    query = "update glops.AdOps_Active_Campaigns_Report_Staging set {updateString} Updated_By = suser_sname(), Update_Date = getdate() {whereClause}"
    query = query.format(updateString=toUpdate,whereClause=whereClause)
    ssms.runQuery(query)
def selectQuery(whereClauseObject):
    whereClause = "where "
    for column in whereClauseObject:
        if whereClause != "where ":
            whereClause += " and "
        whereClause += "{0} = {1}".format(column,whereClauseObject[column])
    query = "SELECT Campaign_Name, Campaign_ID, Site, Placement_ID, Placement_Name,Placement_Start_Date,Placement_End_Date,Ad_ID,Ad_Name,Ad_Type,Ad_Is_Active,Ad_Start_Time,Ad_End_Time,Hard_Cut_Off,Creative_ID,Creative_Name,Creative_Type,Creative_Click_Through_URL, Placement_Compatibility FROM glops.AdOps_Active_Campaigns_Report_Staging {whereClause}"
    query = query.format(whereClause=whereClause)
    return ssms.to_df(query)

        

ChangeLogObjects = ["OBJECT_AD","OBJECT_CREATIVE","OBJECT_PLACEMENT","OBJECT_CAMPAIGN"]
adFields = ["Placement assignment","Creative assignment","Hard cut-off",'Start time','End time','Name','Active status']
invalidAdSet = set()
updateAdSet = set()
updateCreativeSet = set()
updatePlacementSet = set()
updateCampaignSet = set()
   

for obj in ChangeLogObjects:
    currentLog = initialChangeLog.getCurrentObject(currentTime,obj)


def analyzeAdLogs(ChangeLog):
    def analyzePlacementAssignments(placementArray):
        addArray = [x for x in placementArray if x["action"] == "Add"]
        removeArray = [x for x in placementArray if x["action"] == "Remove"]
        for element in addArray:
            placementIDPattern = re.compile('id:(.*,)')
            idString = element["newValue"]
            idGrouping = re.search(placementIDPattern, idString).group(0)
            placementID = re.sub("id: |,","",idGrouping)
            adId = element["objectId"]
            if adId in invalidAdSet:
                continue
            currentAd = checkSession(Ad(adId,initialEventLoop,initialSession))
            try:
                currentAssignments =  currentAd.body["creativeRotation"]["creativeAssignments"]
            except:
                invalidAdSet.add(currentAd.body["id"])
                print(adId)
                continue
            currentPlacement = checkSession(Placement(placementID,initialEventLoop,initialSession))
            AdObject = extractAdInfo(currentAd)
            PlacementObject = extractPlacementInfo(currentPlacement)
            SiteObject = extractSiteInfo(checkSession(Sites(currentPlacement.body['siteId'],initialEventLoop,initialSession)))
            CampaignObject = extractCampaignInfo(checkSession(AsyncCampaign(currentPlacement.body["campaignId"],initialEventLoop,initialSession)))
            
            for assignment in currentAssignments:
                finalObject = {}
                CreativeInfo = checkSession(Creative(assignment["creativeId"]))
                CreativeInfo.body["clickthrough"] = assignment["clickThroughUrl"]['computedClickThroughUrl']
                timestamp = int(CreativeInfo.body["lastModifiedInfo"]["time"]) / 1e3
                CreativeInfo.body["startTime"] = datetime.datetime.fromtimestamp(timestamp).strftime('%m/%d/%y %I:%M %p')
                CreativeInfo = extractCreativeInfo(CreativeInfo)
                finalObject.update(AdObject)
                finalObject.update(PlacementObject)
                finalObject.update(SiteObject)
                finalObject.update(CampaignObject)
                finalObject.update(CreativeInfo)
                generateInsertQuery(finalObject)
        for element in removeArray:
            placementIDPattern = re.compile('id:(.*,)')
            idString = element["oldValue"]
            idGrouping = re.search(placementIDPattern, idString).group(0)
            placementID = re.sub("id: |,","",idGrouping)
            adId = element["objectId"]
            selectObject = {"Ad_ID":adId,"Placement_ID":placementID}
            DeactivateRows(selectObject)

    def analyzeCreativeAssignments(creativeArray):
        addArray = [x for x in creativeArray if x["action"] == "Add"]
        removeArray = [x for x in creativeArray if x["action"] == "Remove"]
        updateArray = [x for x in creativeArray if x["action"] == "Update"]
        for element in addArray:
            creativeIDPattern = re.compile('id:(.*, a)')
            idString = element["newValue"]
            idGrouping = re.search(creativeIDPattern, idString).group(0)
            creativeID = re.sub("id: |, a","",idGrouping)
            adId = element["objectId"]
            selectObject = {"Ad_ID":adId}
            currentAd = checkSession(Ad(adId,initialEventLoop,initialSession))
            for assignment in currentAd.body["creativeRotation"]["creativeAssignments"]:
                if assignment['creativeId'] == creativeID:
                    CreativeInfo = checkSession(Creative(assignment["creativeId"]))
                    CreativeInfo.body["clickthrough"] = assignment["clickThroughUrl"]['computedClickThroughUrl']
                    timestamp = int(CreativeInfo.body["lastModifiedInfo"]["time"]) / 1e3
                    CreativeInfo.body["startTime"] = datetime.datetime.fromtimestamp(timestamp).strftime('%m/%d/%y %I:%M %p')
                    CreativeInfo = extractCreativeInfo(CreativeInfo)
                    break
            rows = selectQuery(selectObject)
            for column in CreativeInfo:
                rows[column] = CreativeInfo[column]
            for row in rows.iterrows():
                generateInsertQuery(row[1].to_dict())
        for element in removeArray:
            creativeIDPattern = re.compile('id:(.*, a)')
            idString = element["oldValue"]
            idGrouping = re.search(creativeIDPattern, idString).group(0)
            creativeID = re.sub("id: |, a","",idGrouping)
            adId = element["objectId"]
            selectObject = {"Ad_ID":adId,"Creative_ID":creativeID}
            DeactivateRows(selectObject)
        for element in updateArray:
            creativeIDPattern = re.compile('id:(.*, a)')
            idString = element["oldValue"]
            idGrouping = re.search(creativeIDPattern, idString).group(0)
            creativeID = re.sub("id: |, a","",idGrouping)
            if creativeID in updateCreativeSet:
                continue
            adId = element["objectId"]
            currentAd = checkSession(Ad(adId,initialEventLoop,initialSession))
            for assignment in currentAd.body["creativeRotation"]["creativeAssignments"]:
                if assignment['creativeId'] == creativeID:
                    CreativeInfo = checkSession(Creative(assignment["creativeId"]))
                    CreativeInfo.body["clickthrough"] = assignment["clickThroughUrl"]['computedClickThroughUrl']
                    timestamp = int(CreativeInfo.body["lastModifiedInfo"]["time"]) / 1e3
                    CreativeInfo.body["startTime"] = datetime.datetime.fromtimestamp(timestamp).strftime('%m/%d/%y %I:%M %p')
                    CreativeInfo = extractCreativeInfo(CreativeInfo)
                    selectObject = {"Creative_ID":creativeID}
                    updateRows(CreativeInfo, selectObject)
                    updateCreativeSet.add(creativeID)
                    break
    def updateAdInfo(adArray):
        for ad in adArray:
            adId = ad["objectId"]
            if adId in updateAdSet:
                continue
            adInfo = extractAdInfo(checkSession(Ad(adId,initialEventLoop,initialSession)))
            selectObject = {"Ad_ID":adId}
            updateRows(adInfo,selectObject)
            updateAdSet.add(adId)
    adArray = ChangeLog.ad
    for field in adFields:
        currentField = [x for x in adArray if x["fieldName"] == field]
        if field == "Placement assignment":
            analyzePlacementAssignments(currentField)
        elif field == "Creative assignment":
            analyzeCreativeAssignments(currentField)
        else:
            updateAdInfo(currentField)
def analyzePlacementLogs(initialChangeLog):
    placementUpdates = [x for x in initialChangeLog.placement if x["action"] == "Update"]
    for placement in placementUpdates:
        placementID = placement["objectId"]
        if placementID not in updatePlacementSet:
            currentPlacement = extractPlacementInfo(checkSession(Placement(placementID,initialEventLoop,initialSession)))
            selectObject = {"Placement_ID":placementID}
            updateRows(currentPlacement, selectObject)
            updatePlacementSet.add(placementID)
def analyzeCampaignLogs(initialChangeLog):
    campaignUpdates = [x for x in initialChangeLog.campaign if x["action"] == "Update"]
    for campaign in campaignUpdates:
        campaignID = campaign["objectId"]
        if campaignID not in updateCampaignSet:
            currentCampaign = extractCampaignInfo(checkSession(AsyncCampaign(campaignID,initialEventLoop,initialSession)))
            selectObject = {"Campaign_ID":campaignID}
            updateRows(currentCampaign, selectObject)
            updateCampaignSet.add(campaignID)    

analyzeAdLogs(initialChangeLog)
analyzePlacementLogs(initialChangeLog)
analyzeCampaignLogs(initialChangeLog)


