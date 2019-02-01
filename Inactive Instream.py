# Run Daily
from v3modules import DCMAPI, AdUtils, CampaignUtils, UtilUtils, MailUtils
import datetime, re, pandas
Api = DCMAPI.DCMAPI()

updatedAdList = []
listvalues = {"active":False,"searchString":"In-stream","type":'AD_SERVING_DEFAULT_AD'}
adlist = AdUtils.listAd(Api,listvalues)
def checkCampaign(campaignId):
    campaign = CampaignUtils.getCampaign(Api,campaignId)
    if "2019" in campaign["name"]:
        return True
    else:
        return False
def checkDate(endTime):
    pattern = re.compile("\.(\d+)")
    endTime = re.sub(pattern,"",endTime)
    endTime = datetime.datetime.strptime(endTime,"%Y-%m-%dT%H:%M:%SZ")
    return endTime > datetime.datetime.today()
adlist = [x for x in adlist if checkDate(x["endTime"])]
adlist = [x for x in adlist if checkCampaign(x["campaignId"])]


for ad in adlist:
    # AdUtils.activateAd(ad["id"],Api)
    updatedAdList.append({"AdId":ad["id"],"campaignId":ad['campaignId'],"campaignName":CampaignUtils.getCampaign(Api,ad['campaignId'])["name"]})
test = 0


df = pandas.DataFrame(data=updatedAdList)
df = df[['campaignName','campaignId','AdId']]
writer = pandas.ExcelWriter('In-Stream Ad Report.xlsx',engine='xlsxwriter')
df.to_excel(writer, sheet_name ="Info", index = False)
worksheet =  writer.sheets['Info']
writer.save()
import os
import modules.send_mail as send_mail
directories = os.listdir()
reports = [x for x in directories if "In-Stream Ad Report" in x]
for report in reports:
    MailUtils.send_email([report], subject="In-steam Ad Report", message="Attached are the updated ads", recipients=["Lennon.Turner@amnetgroup.com", ])