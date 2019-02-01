from v3modules import DCMAPI, ChangeLogUtils, AdUtils, UtilUtils, CampaignUtils
import pandas

Api = DCMAPI.DCMAPI()
listValues = {"action":"ACTION_UPDATE","objectType":"OBJECT_AD","minChangeTime":UtilUtils.getBeginningofYear()}
logs = ChangeLogUtils.getChangeLog(Api, listValues)
deletedLogs = [x for x in logs if x["fieldName"] == "Active status" and x["newValue"] == "false"]
changeLogArray = []
for log in deletedLogs:
    changeLog = [x for x in logs if x["objectId"] == log["objectId"]]
    commentChange = (len([x for x in changeLog if "inactivity" in x["newValue"]]) > 0)
    if commentChange:
        changeLogArray.extend([x for x in changeLog if x["fieldName"] == "Active status"])


for log in changeLogArray:
    obj = {}
    currentAd = AdUtils.getAd(Api,log["objectId"])
    adEndDate = UtilUtils.stringToDateTimeObject(currentAd['endTime'])
    changeTime = UtilUtils.stringToDateTimeObject(log['changeTime'])
    if changeTime < adEndDate:
        test = 0

test = 0


for log in logs:
    obj = {}
    currentAd = AdUtils.getAd(Api,log["objectId"])
    currentCampaign = CampaignUtils.getCampaign(Api, currentAd["campaignId"])
    changetime = UtilUtils.formatDateTime(log["changeTime"])
    userProfile = log['userProfileName']
    obj["Campaign Name"] = currentCampaign["name"]
    obj["Ad Name"] = currentAd["name"]
    obj["Ad Id"] = currentAd["id"]
    obj["Change Time"] = changetime
    obj["User Profile"] = userProfile
    obj["Ad End Date"] = UtilUtils.formatDateTime(currentAd["endTime"])
    changeLogArray.append(obj)


df = pandas.DataFrame(data=changeLogArray)
writer = pandas.ExcelWriter('Updated Ads Report.xlsx',engine='xlsxwriter')
workbook = writer.book
df.to_excel(writer, sheet_name ="Info", index = False)
worksheet =  writer.sheets['Info']
writer.save()
    
test = 0 