from v3modules.TraffickingObject import TraffickingObject
from v3modules.Ad import Ad
from v3modules import UtilUtils, CampaignUtils
from v3modules import DCMAPI
import datetime

Api = DCMAPI.DCMAPI()
def compareAdDates(ad):
    today = datetime.datetime.today()
    adDate = datetime.datetime.strptime(ad["endTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
    return today > adDate

def checkCampaignEndDate(ad):
    campaignId = ad["campaignId"]
    campaign = CampaignUtils.getCampaign(Api, campaignId)
    today = datetime.datetime.today()
    campaignDate = datetime.datetime.strptime(campaign["endDate"], "%Y-%m-%d")
    return today < campaignDate
advertiserSet ={
    "5288214":"GLO»Chevrolet FC»Display»A",
    "5354228":"GLO»Chevrolet Global Advertising»Display»A",
    "6015329":"GLO»Global Content Studio»Display»A",
    "4568611":"US»ACDelco»Display»A",
    "3876773":"US»Buick»Display»A",
    "6198719":"US»Cadillac Certified Pre-Owned»Display»A",
    "3876774":"US»Cadillac»Display»A",
    "3876777":"US»Certified Pre-Owned»Display»A",
    "4569406":"US»Certified Service»Display»A",
    "4569405":"US»Chevrolet Performance»Display»A",
    "3876771":"US»Chevrolet»Display»A",
    "5361629":"US»Factory Pre-Owned Collection»Display»A",
    "3876780":"US»Fleet Commercial Operations»Display»A",
    "4568613":"US»Genuine GM Parts»Display»A",
    "4635253":"US»GM Accessories»Display»A",
    "3876782":"US»GM Card»Display»A",
    "4496783":"US»GM Finance and Insurance»Display»A",
    "4852937":"US»GM Fuels and Lubes»Display»A",
    "5724659":"US»GM Marine»Display»A",
    "4508180":"US»GM Marketing Strategy Support and Recall»Display»A",
    "3876772":"US»GMC»Display»A",
    "5314814":"US»Maven»Display»A",
    "3876775":"US»OnStar»Display»A",
    "5139395":"US»Vehicle Purchase Programs»Display»A"
}
finalAdList = []
for advertiser in advertiserSet:
    currentAdvertiser = str(advertiser)
    to = TraffickingObject().getAdsByAdvertiser(currentAdvertiser)
    adList = [x for x in to.ads if ("11:59" in x["endTime"] or "3:59" in x["endTime"]) and "Brand-neutral" not in x['name'] and "TRACKING" not in x["name"] and "AD_SERVING_DEFAULT_AD" not in x["type"]]
    adList = [x for x in adList if compareAdDates(x) and checkCampaignEndDate(x)]
    adList = [{"name":x["name"],"type":x["type"], "id":x["id"], "advertiser":advertiserSet[currentAdvertiser],"start_time":UtilUtils.formatDateTime(x["startTime"]),"end_time":UtilUtils.formatDateTime(x["endTime"])} for x in adList if x["deliverySchedule"]['hardCutoff'] == False]

    finalAdList.extend(adList)
test = 0 
import pandas
df = pandas.DataFrame(data=finalAdList)
df = df[["advertiser","id","name","start_time","end_time","type"]]
writer = pandas.ExcelWriter('Hard Cut Off Report.xlsx',engine='xlsxwriter')
workbook = writer.book
df.to_excel(writer, sheet_name ="Info", index = False)
worksheet =  writer.sheets['Info']
writer.save()