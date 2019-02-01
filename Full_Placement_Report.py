from v3modules import PlacementUtils, ChangeLogUtils, DCMAPI, CampaignUtils, UtilUtils
import pandas as pd
import datetime
import time

start = time.time()

Api = DCMAPI.DCMAPI()

FinalPlacementArray = []
CampaignObject = {}
delta = datetime.timedelta(minutes = 20)
# sixMonthsAgo = datetime.datetime.today() - delta
twoHoursAgo = datetime.datetime.now() - delta
minChangeTime = UtilUtils.datetimeToString(twoHoursAgo)
firstListValues = {"action":"ACTION_UPDATE","objectType":"OBJECT_PLACEMENT","minChangeTime":minChangeTime}
secondListValues = {"action":"ACTION_CREATE","objectType":"OBJECT_PLACEMENT","minChangeTime":minChangeTime}

updateChangeLogs = [x for x in ChangeLogUtils.getChangeLog(Api, firstListValues) if x["fieldName"] == "Name"]
createChangeLogs = ChangeLogUtils.getChangeLog(Api, secondListValues)

print(len(updateChangeLogs))
print(len(createChangeLogs))
# epoch = datetime.datetime.utcfromtimestamp(0)
# createTime = (sixMonthsAgo - epoch).total_seconds() * 1000.
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
        finalObject["Placement_Group_Name"] = Api.generateRequestUrl("placementGroups",objectId=placement["placementGroupId"]).get().response["name"]
    except: 
        finalObject["Placement_Group_Id"] = "N/A"
        finalObject["Placement_Group_Name"] = "N/A"
    FinalPlacementArray.append(finalObject)
    return None
# placementListValues = {"minStartDate":"2018-06-03"}
# print("getting placements")4
# placements = PlacementUtils.listPlacement(Api,placementListValues)


# def fitPlacement(placement):
#     global FinalPlacementArray
#     def getCampaignName(campaignID):
#         global CampaignObject
#         try:
#             return CampaignObject[campaignID]
#         except:
#             campaign = CampaignUtils.getCampaign(Api,campaignID)
#             CampaignObject[campaignID] = campaign["name"]
#             print("adding {campaignName}".format(campaignName=campaign["name"]))
#             return campaign["name"]
#     def getCreationDate(creationDate):
#         return datetime.datetime.fromtimestamp(creationDate//1000).strftime("%Y-%m-%d")
#     finalObject = {}
#     finalObject["Campaign_id"] = placement['campaignId']
#     finalObject["Campaign_name"] = getCampaignName(placement['campaignId'])
#     finalObject["Placement_id"] = placement["id"]
#     finalObject["Placement_Name"] = placement["name"]
#     finalObject["Planned_Cost"] = placement['pricingSchedule']["pricingPeriods"][0]["rateOrCostNanos"]
#     finalObject["Planned_Impressions"] = placement['pricingSchedule']["pricingPeriods"][0]["units"]
#     finalObject["Start_date"] = placement['pricingSchedule']['startDate']
#     finalObject["End_date"] = placement['pricingSchedule']['endDate']
#     finalObject["Date of Creation"] = getCreationDate(int(placement["createInfo"]["time"]))
#     FinalPlacementArray.append(finalObject)
# #     return None
# print("flattening placements")
# print(len(placements))
# placements = [x for x in placements if int(x["createInfo"]["time"]) > createTime]
# print(len(placements))
# [fitPlacement(x) for x in placements]
[fitPlacement(x, "Create") for x in createChangeLogs]
[fitPlacement(x, "Update") for x in updateChangeLogs]
print("saving file..")
if len(FinalPlacementArray) > 0:
    df = pd.DataFrame(data=FinalPlacementArray)
    df = df[["Campaign_name","Campaign_id","Placement_Name","Placement_id","Planned_Cost","Planned_Impressions","Start_date","End_date","Date of Creation","Placement_Group_Name","Placement_Group_Id","Action"]]
    # writer = pd.ExcelWriter('Full Placment Report.csv',engine='xlsxwriter')
    # workbook = writer.book
    df.to_csv("Full Placement Report.csv", sep="^")
    # worksheet =  writer.sheets['Info']
    # writer.save()
else:
    df = pd.DataFrame(columns=["Campaign_name","Campaign_id","Placement_Name","Placement_id","Planned_Cost","Planned_Impressions","Start_date","End_date","Date of Creation","Placement_Group_Name","Placement_Group_Id","Action"])
    df.to_csv("Full Placement Report.csv", sep="^")

end = time.time()
print(end - start)
