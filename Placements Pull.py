from v3modules import PlacementUtils, ChangeLogUtils, DCMAPI, CampaignUtils, UtilUtils
import pandas as pd
import datetime, re
import time

start = time.time()

Api = DCMAPI.DCMAPI()

delta = datetime.timedelta(minutes = 5)
twoHoursAgo = datetime.datetime.now() - delta
minChangeTime = UtilUtils.datetimeToString(twoHoursAgo)
maxChangeTime = UtilUtils.datetimeToString(datetime.datetime.now())
print(minChangeTime)
print(maxChangeTime)
counter = 1
while True:
    correctionTime = UtilUtils.datetimeToString(datetime.datetime.now())
    firstListValues = {"action":"ACTION_UPDATE","objectType":"OBJECT_PLACEMENT","minChangeTime":minChangeTime, "maxChangeTime":maxChangeTime}
    secondListValues = {"action":"ACTION_CREATE","objectType":"OBJECT_PLACEMENT","minChangeTime":minChangeTime, "maxChangeTime":maxChangeTime}
    updateChangeLogs = [x for x in ChangeLogUtils.getChangeLog(Api, firstListValues) if x["fieldName"] == "Name"]
    createChangeLogs = ChangeLogUtils.getChangeLog(Api, secondListValues)

    print(len(updateChangeLogs))
    print(len(createChangeLogs))
    def fitPlacement(changeLog, action):
        finalObject = {}
        placement = PlacementUtils.getPlacement(Api, changeLog["objectId"])
        def getCampaignName(campaignID):
            global CampaignObject
            try:
                return CampaignObject[campaignID]
            except:
                campaign = CampaignUtils.getCampaign(Api,campaignID)
                CampaignObject[campaignID] = campaign["name"]
                print("adding {campaignName}".format(campaignName=campaign["name"]))
                return campaign["name"]    
        def getCreationDate(creationDate):
            return datetime.datetime.fromtimestamp(creationDate//1000).strftime("%Y-%m-%d")
        finalObject["Campaign_id"] = placement['campaignId']
        finalObject["Campaign_name"] = getCampaignName(placement['campaignId'])
        finalObject["Placement_id"] = placement["id"]
        finalObject["Placement_Name"] = placement["name"]
        finalObject["Planned_Cost"] = int(placement['pricingSchedule']["pricingPeriods"][0]["rateOrCostNanos"])/1000000000
        finalObject["Planned_Impressions"] = placement['pricingSchedule']["pricingPeriods"][0]["units"]
        finalObject["Start_date"] = placement['pricingSchedule']['startDate']
        finalObject["End_date"] = placement['pricingSchedule']['endDate']
        finalObject["Date of Creation"] = getCreationDate(int(placement["createInfo"]["time"]))
        finalObject["Action"] = action
        try:
            finalObject["Placement_Group_Id"] = placement["placementGroupId"]
            if placement["placementGroupId"] in PlacementgroupObject:
                finalObject["Placement_Group_Name"] = PlacementgroupObject[placement["placementGroupId"]]
            else:
                finalObject["Placement_Group_Name"] = Api.generateRequestUrl("placementGroups",objectId=placement["placementGroupId"]).get().response["name"]
                PlacementgroupObject[placement["placementGroupId"]] = finalObject["Placement_Group_Name"]
        except: 
            finalObject["Placement_Group_Id"] = "N/A"
            finalObject["Placement_Group_Name"] = "N/A"
        FinalPlacementArray.append(finalObject)
        return None

    FinalPlacementArray = []
    CampaignObject = {}
    PlacementgroupObject = {}
    fileTime = re.sub(":|T|Z","_",correctionTime)
    print("flattening placements")
    [fitPlacement(x, "Create") for x in createChangeLogs]
    [fitPlacement(x, "Update") for x in updateChangeLogs]
    print("saving file..")
    if len(FinalPlacementArray) > 0:
        df = pd.DataFrame(data=FinalPlacementArray)
        df = df[["Campaign_name","Campaign_id","Placement_Name","Placement_id","Planned_Cost","Planned_Impressions","Start_date","End_date","Date of Creation","Placement_Group_Name","Placement_Group_Id"]]
        df.to_csv("{time}_Placement_Report.csv".format(time = str(counter)), sep="^")
        counter += 1
    else:
        time.sleep(1200)
    minChangeTime = correctionTime
    end = time.time()
    print(end - start)
    print(correctionTime)
