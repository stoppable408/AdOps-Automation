from modules.ChangeLogs import ChangeLogs
from modules.AsyncCampaign import AsyncCampaign
import re
import requests
import pandas as pd
def getBeginningofWeek():
    from datetime import datetime, timedelta
    currentdate = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return currentdate

currentDate = getBeginningofWeek()
changeLog = ChangeLogs().getNewPlacements(currentDate).activateTrackingAds().modifySSPlacements().getNewCampaigns(currentDate).verifyCampaigns()
initialSession = changeLog.session
initialEventLoop = changeLog.eventLoop
campaignArray = []
changeLog.getAllCampaignChanges(currentDate)
for log in changeLog.logs:
    if log["fieldName"] == 'End date':
        campaignID = log["objectId"]
        Campaign = AsyncCampaign(campaignID,initialEventLoop,initialSession)
        campaignObject = {"Name":Campaign.body["name"],"ID":campaignID,"Old Date":log["oldValue"],"New Date":log["newValue"]}
        campaignArray.append(campaignObject)
if len(campaignArray) > 0:
    df = pd.DataFrame(data=campaignArray)      
    df = df[["Name","ID","Old Date","New Date"]]
    writer = pd.ExcelWriter('Campaign Extension Report.xlsx',engine='xlsxwriter')
    workbook = writer.book
    df.to_excel(writer, sheet_name ="Info", index = False)
    worksheet =  writer.sheets['Info']
    writer.save()
# changelog = ChangeLogs().getCurrentObject(currentDate,"OBJECT_CAMPAIGN")
# endDateChange = [x for x in changelog.campaign if x["fieldName"] == "End date"]
# test = 0
# landingPageArray = []
# advertiserSet ={
#     "5288214":"GLO»Chevrolet FC»Display»A",
#     "5354228":"GLO»Chevrolet Global Advertising»Display»A",
#     "6015329":"GLO»Global Content Studio»Display»A",
#     "4568611":"US»ACDelco»Display»A",
#     "3876773":"US»Buick»Display»A",
#     "6198719":"US»Cadillac Certified Pre-Owned»Display»A",
#     "3876774":"US»Cadillac»Display»A",
#     "3876777":"US»Certified Pre-Owned»Display»A",
#     "4569406":"US»Certified Service»Display»A",
#     "4569405":"US»Chevrolet Performance»Display»A",
#     "3876771":"US»Chevrolet»Display»A",
#     "5361629":"US»Factory Pre-Owned Collection»Display»A",
#     "3876780":"US»Fleet Commercial Operations»Display»A",
#     "4568613":"US»Genuine GM Parts»Display»A",
#     "4635253":"US»GM Accessories»Display»A",
#     "3876782":"US»GM Card»Display»A",
#     "4496783":"US»GM Finance and Insurance»Display»A",
#     "4852937":"US»GM Fuels and Lubes»Display»A",
#     "5724659":"US»GM Marine»Display»A",
#     "4508180":"US»GM Marketing Strategy Support and Recall»Display»A",
#     "3876772":"US»GMC»Display»A",
#     "5314814":"US»Maven»Display»A",
#     "3876775":"US»OnStar»Display»A",
#     "5139395":"US»Vehicle Purchase Programs»Display»A"
# }
# parameterString = "advertiserIds="
# for advertiserId in advertiserSet:
#     parameterString

# # from modules.LandingPage import LandingPage
# # test = LandingPage()
# url = "https://www.googleapis.com/dfareporting/v3.0/userprofiles/{profileId}/advertiserLandingPages?advertiserIds=5288214&5354228".format(profileId=str(2532624))
# r = requests.get(url,headers=auth)

# campaignObject = AsyncCampaign(20124958).getAllCampaigns()
# initialSession = campaignObject.session
# initialEventLoop = campaignObject.eventLoop
# for campaign in campaignObject.allCampaigns:
#     currentAdvertiser = str(campaign['advertiserId'])

#     if currentAdvertiser not in advertiserSet:
#         continue
#     campaignId = campaign["id"]
#     advertiserName = advertiserSet[currentAdvertiser]
#     currentCampaign = AsyncCampaign(campaignId,initialEventLoop,initialSession).getLandingPages()
#     for landingpage in currentCampaign.landingPages:
#         profileId = currentCampaign.profile_id
#         auth = currentCampaign.auth
#         pageID = landingpage["id"]
#         pageName = landingpage["name"]
#         url = landingpage["url"]
#         r = currentCampaign.requests.get(url)
#         landingpageObject = {
#             "Advertiser":advertiserName,
#             "Name":pageName,
#             "Landing Page ID":pageID,
#             "Url":url,
#             "Status Code":r.status_code
#             }
#         landingPageArray.append(landingpageObject)
#         # pageID = str(22418309)
#         # patchURL = "https://www.googleapis.com/dfareporting/v3.0/userprofiles/{profileId}/advertiserLandingPages?id={pageID}".format(profileId=profileId,pageID=pageID)
#         # url = re.sub("http","https",landingpage["url"])
#         # payload = {"url":"https://www.chevrolet.com/idea"}
#         # print(payload)
#         # currentCampaign.requests.patch(patchURL, headers=auth, data=currentCampaign.json.dumps(payload))
#         # r = currentCampaign.requests.get(url)
#     test = 0
#         # print(r.status_code)

