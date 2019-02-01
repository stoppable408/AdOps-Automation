from v3modules import CampaignUtils, DCMAPI, AdUtils, UtilUtils
import datetime
import pandas as pd


Api = DCMAPI.DCMAPI()
AdList = []
def compareAdDates(ad):
    today = datetime.datetime.today()
    adDate = datetime.datetime.strptime(ad["endTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
    return today > adDate

LMACampaigns = CampaignUtils.getAllLMA(Api)
for campaign in LMACampaigns:
    print("Analyzing {campaignName}".format(campaignName=campaign["name"]))
    listValues = {"campaignIds": campaign["id"], "active":True, "archived":False}
    ads = AdUtils.listAd(Api,listValues,True)
    ads = [x for x in ads if compareAdDates(x)]
    for ad in ads:
        AdUtils.deactivateAd(ad["id"], Api)
        AdList.append({"name":ad["name"], "id":ad["id"]})

df = pd.DataFrame(data=AdList)
writer = pd.ExcelWriter('Archived Ads Report.xlsx',engine='xlsxwriter')
workbook = writer.book
df.to_excel(writer, sheet_name ="Info", index = False)
worksheet =  writer.sheets['Info']
writer.save()
    