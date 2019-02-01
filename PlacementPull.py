from v3modules import PlacementUtils, ChangeLogUtils, DCMAPI, CampaignUtils, UtilUtils
import pandas as pd
import datetime, re
import time

start = time.time()

Api = DCMAPI.DCMAPI()


listValues = {"searchString":"»"}
placements = PlacementUtils.listPlacement(Api, listValues)
# placements = [x for x in placements if "»" in x["name"]]
def fitPlacement(placement):
    finalObject = {}
    def getCampaignName(campaignID):
        global CampaignObject
        try:
            return CampaignObject[campaignID]
        except:
            campaign = CampaignUtils.getCampaign(Api,campaignID)
            CampaignObject[campaignID] = campaign["name"]
            print("adding campaign: {campaignName}".format(campaignName=campaign["name"]))
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
    finalObject["Action"] = "Create"
    try:
        finalObject["Placement_Group_Id"] = placement["placementGroupId"]
        if placement["placementGroupId"] in PlacementgroupObject:
            finalObject["Placement_Group_Name"] = PlacementgroupObject[placement["placementGroupId"]]
        else:
            finalObject["Placement_Group_Name"] = Api.generateRequestUrl("placementGroups",objectId=placement["placementGroupId"]).get().response["name"]
            PlacementgroupObject[placement["placementGroupId"]] = finalObject["Placement_Group_Name"]
            print("adding Placement Group: {PG_Name}".format(PG_Name=finalObject["Placement_Group_Name"]))
    except: 
        finalObject["Placement_Group_Id"] = "N/A"
        finalObject["Placement_Group_Name"] = "N/A"
    FinalPlacementArray.append(finalObject)
    return None

FinalPlacementArray = []
CampaignObject = {}
PlacementgroupObject = {}
print("flattening placements")
for placement in range(0, len(placements)):
    print("placement {num} of {length}".format(num=str(int(placement)+1), length=len(placements)))
    fitPlacement(placements[placement])
print("saving file..")
df = pd.DataFrame(data=FinalPlacementArray)

df = df[["Campaign_name","Campaign_id","Placement_Name","Placement_id","Planned_Cost","Planned_Impressions","Start_date","End_date","Date of Creation","Placement_Group_Name","Placement_Group_Id"]]
df.to_csv("Placement_Report.csv", sep="^")
end = time.time()
print(end - start)