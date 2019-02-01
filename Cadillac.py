from v3modules import DCMAPI, CampaignUtils, PlacementUtils
import pandas, datetime
def checkDate(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    today = datetime.datetime.today()
    return today > date
finalArray = []
Api = DCMAPI.DCMAPI()
listvalues = {"advertiserIds":3876774, "archived":False}
campaignList = CampaignUtils.getCampaignList(Api,listvalues)
campaignList = [c for c in campaignList if checkDate(c["endDate"])]

for campaign in campaignList:
    listvalues = {"campaignIds":campaign["id"],"active":True,"archived":False}
    placementList = PlacementUtils.listPlacement(Api,listvalues)
    placementList = [c for c in placementList if checkDate(c['pricingSchedule']["endDate"])]
    for placement in placementList:
        print("running")
        obj = {"Campaign Name":campaign["name"], "Campaign ID":campaign["id"],"Placement Name":placement["name"],"Placement ID":placement["id"]}
        finalArray.append(obj)

df = pandas.DataFrame(finalArray)
writer = pandas.ExcelWriter('Cadillac Report.xlsx',engine='xlsxwriter')
df.to_excel(writer, sheet_name ="Info", index = False)
writer.save()