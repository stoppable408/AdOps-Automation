from v3modules import DCMAPI, CampaignUtils, AdUtils


Api = DCMAPI.DCMAPI()

campaignList = CampaignUtils.getAllCampaigns(Api)
campaignList = [x for x  in campaignList if "_2018" in x["name"]]
for campaign in campaignList:
    print(campaign["name"])
    campaignId = campaign["id"]
    listValues = {"campaignIds":campaignId,"archived":False}
    adList = [x for x in AdUtils.listAd(Api,listValues) if "Brand-neutral" not in x["name"]]
    [AdUtils.deactivateAd(x["id"],Api) for x in adList]