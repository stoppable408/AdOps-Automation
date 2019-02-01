from v3modules import PlacementUtils, ChangeLogUtils, DCMAPI, CampaignUtils, UtilUtils, AdUtils
import datetime
Api = DCMAPI.DCMAPI()
campaignArray = []
listValues = {"active":False,"archived":True,"searchString":"TRACKING"}
adList = AdUtils.listAd(Api,listValues)
November1 = datetime.datetime.strptime('2018-11-15T03:00:00Z',"%Y-%m-%dT%H:%M:%SZ")
def compareAds(ad):
    try:
        adDate = datetime.datetime.strptime(ad['startTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        adDate = datetime.datetime.strptime(ad['startTime'], "%Y-%m-%dT%H:%M:%S.999Z")
    return adDate > November1
def checkName(ad):
    array =["Bonus", "General", "First Strike", "Holiday"]
    for element in array:
        if element in ad["name"]:
            return True
    return False
adList = [x for x in adList if compareAds(x) and checkName(x)]
payload = {"placementAssignments":[]}
for ad in adList:
    try:
        test = ad["placementAssignments"]
        campaignArray.append(ad["campaignId"])
    except:
        pass
    AdUtils.updateAd(Api, ad["id"], payload)
    
test =0 