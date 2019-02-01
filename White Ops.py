from v3modules import DCMAPI, CampaignUtils, AdUtils, EventUtils, CreativeUtils, AdvertiserUtils, ChangeLogUtils, PlacementUtils

Api = DCMAPI.DCMAPI()
# advertiserSet = AdvertiserUtils.getAdvertiserSet()
AdobeClickCopy = EventUtils.getEvent(Api,2668824)
AdobeImpressionCopy = EventUtils.getEvent(Api,2695156)
# allCampaigns = [CampaignUtils.getCampaign(Api,20124958)]
# campaigns = CampaignUtils.getAllLMA(Api)
# allCampaigns = [x for x in campaigns if "103" not in x["name"] and "115" not in x["name"]]
# allCampaigns = [CampaignUtils.getCampaign(Api,21798175),CampaignUtils.getCampaign(Api,21815028),CampaignUtils.getCampaign(Api,21712772),CampaignUtils.getCampaign(Api,21736049),CampaignUtils.getCampaign(Api,21792915),CampaignUtils.getCampaign(Api,21825936),CampaignUtils.getCampaign(Api,21830580),CampaignUtils.getCampaign(Api,21884880)]
# allCampaigns = [c for c in allCampaigns if "LMA" not in c["name"]]22112046 
testList = [22064108,21937425,22061249,22046095,22046937,22060037,22059116,22063868,22086082,22110050,22112046,22052473]
allCampaigns = [CampaignUtils.getCampaign(Api,x) for x in testList]

# 21798175
# 21815028
# 21712772
# 21736049
# 21792915
# 21825936
# 21830580
# 21884880

def checkCompatibility(ad):
    creativeId = ad['creativeRotation']['creativeAssignments'][0]['creativeId']
    creative = CreativeUtils.getCreative(Api, creativeId)
    compatibility = creative["compatibility"][0]
    if compatibility == "DISPLAY" or compatibility == 'IN_STREAM_VIDEO':
        return True
    return False


def findAdobeImpressionPixel(campaignId):
    listValues = {"campaignId": campaignId}
    eventlist = EventUtils.listEvents(Api, listValues=listValues)
    for event in eventlist:
        if "Adobe Impression" in event["name"]:
            payload = {"enabled":True, "id":event["id"]}
            return payload

#  "defaultClickThroughEventTagProperties": {
#   "overrideInheritedEventTag": true,
#   "defaultClickThroughEventTagId": "2685868"
#  },
def findAdobeClickPixel(campaignId):
    listValues = {"campaignId": campaignId}
    eventlist = EventUtils.listEvents(Api, listValues=listValues)
    for event in eventlist:
        if "Adobe Click" in event["name"]:
            payload = {"overrideInheritedEventTag":True, "defaultClickThroughEventTagId":event["id"]}
            return payload

# def findEvidonPixel(campaignId):
#     listValues = {"campaignId": campaignId}
#     eventlist = EventUtils.listEvents(Api, listValues=listValues)
#     for event in eventlist:
#         if "Evidon" in event["name"]:
#             payload = {"overrideInheritedEventTag":True, "defaultClickThroughEventTagId":event["id"]}
#             return payload

for campaign in allCampaigns:
    # campaign["id"] = 20588848 
    print(campaign["name"])
    impressionPayload = findAdobeImpressionPixel(campaign["id"])
    if impressionPayload == None:
        print("adding eventBody")
        eventbody = {
        "campaignId": campaign["id"],
        "advertiserId": campaign['advertiserId'],
        "name": "Adobe Impression",
        "accountId": campaign['accountId'],
        "type": "IMPRESSION_IMAGE_EVENT_TAG",
        "status": "ENABLED",
        "url": AdobeImpressionCopy["url"] }
        EventUtils.insertEvent(Api,eventbody)

    clickPayload = findAdobeClickPixel(campaign["id"])
    if clickPayload == None:
        print("adding eventBody")
        eventbody = {
        "campaignId": campaign["id"],
        "advertiserId": campaign['advertiserId'],
        "name": "Adobe Click",
        "accountId": campaign['accountId'],
        "type": "CLICK_THROUGH_EVENT_TAG",
        "status": "ENABLED",
        "url":AdobeClickCopy["url"]  }
        EventUtils.insertEvent(Api,eventbody)

    # evidonPayLoad = findEvidonPixel(campaign["id"])
    # if evidonPayLoad == None:
    #     print("adding eventBody")
    #     eventbody = {
    #     "campaignId": campaign["id"],
    #     "advertiserId": campaign['advertiserId'],
    #     "name": "Evidon",
    #     "accountId": campaign['accountId'],
    #     "type": "IMPRESSION_JAVASCRIPT_EVENT_TAG",
    #     "status": "ENABLED",
    #     "url": "https://c.betrad.com/durly.js?;ad_wxh=%psz=!;;coid=971;nid=101960;",
    #     }
    #     EventUtils.insertEvent(Api,eventbody),"active":True,"archived":False
    listValues = {"campaignIds":campaign["id"],"active":True,"archived":False}
    adList = AdUtils.listAd(Api,listValues=listValues,filter=True)
    adList = [x for x in adList if checkCompatibility(x)]
    for ad in adList:
        try:
            eventOverrides = ad['eventTagOverrides']
            eventTagProperties = ad["defaultClickThroughEventTagProperties"]
        except:
            eventOverrides = []
            eventTagProperties = None
        if impressionPayload not in eventOverrides:
            AdUtils.insertEventTag(Api, ad["id"], impressionPayload)
        if clickPayload != eventTagProperties:
            AdUtils.inheritEventTag(Api, ad["id"], clickPayload)
    # if impressionPayload != None:
    #     EventUtils.deleteEvent(Api,impressionPayload["id"])
    # if clickPayload != None:
    #     EventUtils.deleteEvent(Api,clickPayload["defaultClickThroughEventTagId"])
    # if payload != None:
        # EventUtils.deleteEvent(Api,payload["id"])
    # test = 0



