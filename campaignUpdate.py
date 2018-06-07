from modules.ChangeLogs import ChangeLogs
from modules.AsyncCampaign import AsyncCampaign
import re

def getBeginningofWeek():
    from datetime import datetime, timedelta
    currentdate = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return currentdate

currentDate = getBeginningofWeek()
changeLog = ChangeLogs().getNewPlacements(currentDate).activateTrackingAds().modifySSPlacements().getNewCampaigns(currentDate).verifyCampaigns()
# advertiserSet = set([5288214,5354228,6015329,4568611,3876773,6198719,3876774,3876777,4569406,4569405,3876771,5361629,3876780,3899258,5835337,4568613,4635253,3876782,4496783,4852937,5724659,4508180,3876772,5314814,3876775,5139395])
# campaignObject = AsyncCampaign(20124958).getAllCampaigns()
# initialSession = campaignObject.session
# initialEventLoop = campaignObject.eventLoop
# for campaign in campaignObject.allCampaigns:
#     currentAdvertiser = int(campaign['advertiserId'])
#     if currentAdvertiser not in advertiserSet:
#         continue
#     campaignId = campaign["id"]
#     currentCampaign = AsyncCampaign(campaignId,initialEventLoop,initialSession).getLandingPages()
#     for landingpage in currentCampaign.landingPages:
#         profileId = currentCampaign.profile_id
#         auth = currentCampaign.auth
#         pageID = str(22287020)
#         patchURL = "https://www.googleapis.com/dfareporting/v3.0/userprofiles/{profileId}/advertiserLandingPages?id={pageID}".format(profileId=profileId,pageID=pageID)
#         url = re.sub("http","https",landingpage["url"])
#         payload = {"url":url}
#         print(payload)
#         # currentCampaign.requests.patch(patchURL, headers=auth, data=currentCampaign.json.dumps(payload))

