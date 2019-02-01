from v3modules import DCMAPI, CampaignUtils, AdUtils, EventUtils, CreativeUtils, AdvertiserUtils, ChangeLogUtils, PlacementUtils

Api = DCMAPI.DCMAPI()
# advertiserSet = AdvertiserUtils.getAdvertiserSet()
AdobeTagCopy = EventUtils.getEvent(Api,2560485)
allCampaigns = CampaignUtils.getAllLMA(Api)
# allCampaigns = [c for c in allCampaigns if "LMA" not in c["name"]]




def findAdobeImpressionPixel(campaignId):
    listValues = {"campaignId": campaignId}
    eventlist = EventUtils.listEvents(Api, listValues=listValues)
    for event in eventlist:
        if "CDK" in event["name"]:
            payload = {"enabled":True, "id":event["id"]}
            return payload

    

for campaign in allCampaigns:
    # campaign["id"] = 20588848 
    print(campaign["name"])
    impressionPayload = findAdobeImpressionPixel(campaign["id"])
    if impressionPayload == None:
        print("adding eventBody")
        eventbody = {
        "campaignId": campaign["id"],
        "advertiserId": campaign['advertiserId'],
        "name": "CDK Impression Pixel",
        "accountId": campaign['accountId'],
        "type": "IMPRESSION_JAVASCRIPT_EVENT_TAG",
        "status": "ENABLED",
        "url": "https://dt.admission.net/vt.gif?cs:pa=carat&cs:pro=caratlmaads&cs:e=di&cs:a=carat_chev_ads&cachebust={CACHEBUSTER}&cs:vt:domain=www.chevydealer.com",
       }
        EventUtils.insertEvent(Api,eventbody)

    # clickPayload = findAdobeClickPixel(campaign["id"])
    # if clickPayload == None:
    #     print("adding eventBody")
    #     eventbody = {
    #     "campaignId": campaign["id"],
    #     "advertiserId": campaign['advertiserId'],
    #     "name": "Adobe Click",
    #     "accountId": campaign['accountId'],
    #     "type": "CLICK_THROUGH_EVENT_TAG",
    #     "status": "ENABLED",
    #     "url": "https://gm.demdex.net/event?d_event=click&d_src=313715&d_campaign=%ebuy!&d_site=%esid!&d_placement=%epid!&d_adsrc=%eadv!&d_adgroup=%eaid!&d_creative=%ecid!&d_rd=",
    #     }
    #     EventUtils.insertEvent(Api,eventbody)
    # listValues = {"campaignIds":campaign["id"],"active":True,"archived":False}
    # adList = AdUtils.listAd(Api,listValues=listValues,filter=True)
    # adList = [x for x in adList if checkCompatibility(x)]
    # for ad in adList:
    #     try:
    #         eventOverrides = ad['eventTagOverrides']
    #     except:
    #         eventOverrides = []
    #     if impressionPayload not in eventOverrides:
    #             AdUtils.insertEventTag(Api, ad["id"], impressionPayload)
    # if payload != None:
    #     EventUtils.deleteEvent(Api,payload["id"])
    # test = 0


