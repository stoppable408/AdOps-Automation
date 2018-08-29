from v3modules import DCMAPI, CampaignUtils, AdUtils, EventUtils, CreativeUtils, AdvertiserUtils

Api = DCMAPI.DCMAPI()
advertiserSet = AdvertiserUtils.getAdvertiserSet()
WhiteOpsCopy = EventUtils.getEvent(Api,2589192)
allCampaigns = CampaignUtils.getAllCampaigns(Api)
allCampaigns = [x for x in allCampaigns if "LMA" not in x["name"]]


def checkCompatibility(ad):
    creativeId = ad['creativeRotation']['creativeAssignments'][0]['creativeId']
    creative = CreativeUtils.getCreative(Api, creativeId)
    compatibility = creative["compatibility"][0]
    if compatibility == "DISPLAY":
        return True
    return False

def findWhiteOpsTag(campaignId):
    listValues = {"campaignId": campaignId}
    eventlist = EventUtils.listEvents(Api, listValues=listValues)
    for event in eventlist:
        if "White Ops" in event["name"]:
            payload = {"enabled":True, "id":event["id"]}
            return payload

for campaign in allCampaigns:
    print(campaign["name"])
    test = 21476547   
    payload = findWhiteOpsTag(test)
    listValues = {"campaignIds":test,"active":True,"archived":False}
    adList = AdUtils.listAd(Api,listValues=listValues,filter=True)
    adList = [x for x in adList if checkCompatibility(x)]
    for ad in adList:
        try:
            eventOverrides = ad['eventTagOverrides']
        except:
            eventOverrides = []
        if payload not in eventOverrides:
                AdUtils.insertEventTag(Api, ad["id"], payload)
