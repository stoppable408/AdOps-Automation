from v3modules import CampaignUtils, AdUtils, PlacementUtils, ChangeLogUtils, UtilUtils, ReportUtils, DCMAPI
import re

Api = DCMAPI.DCMAPI()

campaignList = CampaignUtils.getAllCampaigns(Api)

for campaign in campaignList:
    listValues = {"campaignIds":campaign["id"]}
    ad = AdUtils.listAd(Api, listValues)
    test =0 