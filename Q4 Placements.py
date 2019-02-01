from v3modules import DCMAPI, PlacementUtils, CampaignUtils, UtilUtils

Api = DCMAPI.DCMAPI()
LMACampaignObj = {}
NotLMAObj = {}
listValues = {"minStartDate":"2018-01-01","minEndDate":"2018-09-01", "maxEndDate":"2018-12-31", "archived":False}

def lmaCampaignCheck(placement):
    global LMACampaignObj
    global NotLMAObj
    campaignId = placement["campaignId"]
    if campaignId in LMACampaignObj:
        return True
    if campaignId in NotLMAObj:
        return False
    print("checking " + str(campaignId))
    campaign = CampaignUtils.getCampaign(Api, campaignId)
    if "LMA" in campaign["name"]:
        LMACampaignObj[campaign["id"]]  = campaign["name"]
        return True
    else:
        NotLMAObj[campaign["id"]]  = campaign["name"]
        return False
placementList = PlacementUtils.listPlacement(Api, listValues)
placementList = [{"Placement Name":x["name"],"Placement Id":x["id"],"Placement Start Date":UtilUtils.formatPlacementDate(x["pricingSchedule"]["startDate"]),"Placement End Date":UtilUtils.formatPlacementDate(x["pricingSchedule"]["endDate"]),"Campaign ID":x["campaignId"],"Campaign Name":LMACampaignObj[x["campaignId"]]} for x in placementList if lmaCampaignCheck(x) and ("_TPS_" in x["name"] or "»TP»" in x["name"])]

import pandas as pd
df = pd.DataFrame(data=placementList)
df = df[["Campaign Name", "Campaign ID", "Placement Name", "Placement Id", "Placement Start Date", "Placement End Date",]]
writer = pd.ExcelWriter('Q4 Placement Report.xlsx',engine='xlsxwriter')
workbook = writer.book
df.to_excel(writer, sheet_name ="Info", index = False)
worksheet =  writer.sheets['Info']
writer.save()
    
test = 0 