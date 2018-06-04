from modules.ChangeLogs import ChangeLogs
from modules.Ad import Ad
from modules.AsyncCampaign import AsyncCampaign
from modules.Placements import Placement
from modules.Creative import Creative
from modules.Sites import Sites
import re

def getBeginningofWeek():
    from datetime import datetime, timedelta
    currentdate = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return currentdate

currentTime = getBeginningofWeek()
initialChangeLog = ChangeLogs()
initialSession = initialChangeLog.session
initialEventLoop = initialChangeLog.eventLoop
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
    "Hard_Cut_Off":hardCutoff
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
        "Campaign_Name":campaignObject.body["name"]
    }
    return finalCampaignObject

ChangeLogObjects = ["OBJECT_AD","OBJECT_CREATIVE","OBJECT_PLACEMENT","OBJECT_CAMPAIGN"]
adFields = ["Placement assignment","Creative assignment","Hard cut-off",'Start time','End time','Name','Active status']




   

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
            currentAd = checkSession(Ad(adId,initialEventLoop,initialSession))
            currentPlacement = checkSession(Placement(placementID,initialEventLoop,initialSession))
            AdObject = extractAdInfo(currentAd)
            PlacementObject = extractPlacementInfo(currentPlacement)
            SiteObject = Sites(currentPlacement.body['siteId'],initialEventLoop,initialSession)
            CampaignObject = extractCampaignInfo(checkSession(AsyncCampaign(currentPlacement.body["campaignId"],initialEventLoop,initialSession)))
            test = 0

    def analyzeCreativeAssignments(creativeArray):
        pass
    def updateAdInfo(adArray):
        pass
    adArray = ChangeLog.ad
    for field in adFields:
        currentField = [x for x in adArray if x["fieldName"] == field]
        if field == "Placement assignment":
            analyzePlacementAssignments(currentField)
        if field == "Creative assignment":
            analyzeCreativeAssignments(currentField)
        else:
            updateAdInfo(currentField)

analyzeAdLogs(initialChangeLog)
            


