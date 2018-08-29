from v3modules import DCMAPI, CampaignUtils, LandingPageUtils
import re




Api = DCMAPI.DCMAPI()

landingpages = LandingPageUtils.getAllDisplayLandingPages(Api)

for page in landingpages:
    if page["advertiserId"] != "4568611":
        continue
    if "https://" not in page["url"]:
        url = re.sub("http","https",page["url"])
        payload = {"url":url}
        LandingPageUtils.updateLandingPage(Api,page["id"],payload)   
        

# pageID = str(22418309)
# patchURL = "https://www.googleapis.com/dfareporting/v3.0/userprofiles/{profileId}/advertiserLandingPages?id={pageID}".format(profileId=profileId,pageID=pageID)
# url = re.sub("http","https",landingpage["url"])
# payload = {"url":"https://www.chevrolet.com/idea"}
# print(payload)
# currentCampaign.requests.patch(patchURL, headers=auth, data=currentCampaign.json.dumps(payload))
# r = currentCampaign.requests.get(url)


