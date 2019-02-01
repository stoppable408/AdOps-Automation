from v3modules import DCMAPI, CreativeUtils, CampaignUtils

Api = DCMAPI.DCMAPI()

def activateCreative(creativeAssets):
    for asset in creativeAssets:
        asset["active"] = True
    return creativeAssets


listValues = {"archived":False, "searchString":"2019","subaccountId":"23262"}
campaignList = CampaignUtils.getCampaignList(Api, listValues)


for campaign in campaignList:
    listValues = {"active": True, "archived": False,"campaignId":campaign["id"]}
    creativeList = CreativeUtils.listCreatives(Api, listValues)
    for creative in creativeList:
        try:
            assets = [x for x in creative["creativeAssets"] if x["active"] == False]
        except:
            continue
        if len(assets) == 0:
            continue
        else:
            creativeAssets = activateCreative(creative["creativeAssets"])
            payload =  {"creativeAssets": creativeAssets}
            CreativeUtils.updateCreative(Api, creative["id"], payload)

