from v3modules import CampaignUtils, DCMAPI, AdUtils, UtilUtils
import datetime
import pandas as pd


Api = DCMAPI.DCMAPI()
AdList = []
def compareAdDates(ad):
    today = datetime.datetime(2017,1,1,12)
    adDate = datetime.datetime.strptime(ad["endTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
    return today > adDate
listValues = {"subaccountId":28400, "archived":False}
CanadaCampaigns = CampaignUtils.getCampaignList(Api, listValues)
for campaign in CanadaCampaigns:
    print("Analyzing {campaignName}".format(campaignName=campaign["name"]))
    listValues = {"campaignIds": campaign["id"], "active":True, "archived":False}
    ads = AdUtils.listAd(Api,listValues)
    ads = [x for x in ads if compareAdDates(x)]
    for ad in ads:
        AdUtils.deactivateAd(ad["id"], Api)
        AdList.append({"name":ad["name"], "id":ad["id"], "campaign name":campaign["name"], "campaign Id": campaign["id"]})

df = pd.DataFrame(data=AdList)
writer = pd.ExcelWriter('Archived Ads Report.xlsx',engine='xlsxwriter')
workbook = writer.book
df.to_excel(writer, sheet_name ="Info", index = False)
worksheet =  writer.sheets['Info']
writer.save()
    