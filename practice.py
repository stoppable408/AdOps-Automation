from v3modules import CampaignUtils, AdUtils, PlacementUtils, ChangeLogUtils, UtilUtils, ReportUtils
import re

beginningOfWeek = UtilUtils.getBeginningofWeek()
placementListValues = {"action":"action_create","objectType":"OBJECT_PLACEMENT","minChangeTime":beginningOfWeek}
campaignListValues = {"action":"action_create","objectType":"OBJECT_CAMPAIGN","minChangeTime":beginningOfWeek}
newPlacements = [x for x in ChangeLogUtils.getChangeLog(placementListValues) if "_SS_" in x["newValue"]]
newCampaigns = ChangeLogUtils.getChangeLog(campaignListValues)
finalPlacementArray = []
finalCampaignArray = []



def filterPlacement(placement, campaignName):
    finalPlacementObject = {"Campaign Name":campaignName,"Placement ID":placement["id"],"Placement Name":placement["name"]}
    return finalPlacementObject

def filterTrackingAdList(adList):
    BonusAd = [x for x in campaign.adList if "TRACKING" in x["name"] and "Bonus" in x["name"]][0]
    FirstAd = [x for x in campaign.adList if "TRACKING" in x["name"] and "First" in x["name"]][0]
    HolidayAd = [x for x in campaign.adList if "TRACKING" in x["name"] and "Holiday" in x["name"]][0]
    GeneralAd = [x for x in campaign.adList if "TRACKING" in x["name"] and "General" in x["name"]][0]
    return [BonusAd, HolidayAd, FirstAd, GeneralAd]

def getModifiedAds(adsToUse,existingads):
    modifiedAds = []
    existingads = [x["name"].strip() for x in existingads]
    for ad in adsToUse:
        currentAd = AdUtils.getAd(ad)
        adName = currentAd["name"]
        if adName.strip() not in existingads:
            modifiedAds.append(ad)
    return modifiedAds

def pullAdsIntoCampaign(campaign, modifiedAds=None):
    englishAds = ["411816686","411815576", "411848029", "411816665"]
    spanishAds = ["409389455", "409389461","410964991", "409389458"]
    if "Hispanic" in campaign["name"]:
        adsToUse = spanishAds
    else:
        adsToUse = englishAds
    if modifiedAds != None or len(modifiedAds) == 0:
        adsToUse = getModifiedAds(adsToUse, modifiedAds)
    for ads in adsToUse:
        currentAd = AdUtils.copy(ads,campaign["name"])
        AdUtils.insertAd(currentAd)

regex = re.compile(r'(\d+)LM\/')
for placement in range(0, len(newPlacements)): 
    print("checking placement %s of %s" % (str(placement + 1), len(newPlacements)))
    placementId = newPlacements[placement]["objectId"]
    placementObject = PlacementUtils.getPlacement(placementId)
    campaign = CampaignUtils.getCampaign(placementObject["campaignId"])
    if regex.search(campaign["name"]):
        listValues = {"placementIds":placementId}
        PlacementUtils.pushStaticClickTracking(placementId)
        placementAds = [x for x in AdUtils.listAd(listValues) if "TRACKING" in x["name"]]
        listValues = {"campaignIds":campaign["id"]}
        campaignAds = [x for x in  AdUtils.listAd(listValues) if "TRACKING" in x["name"] and x["active"] == True]
        if len(campaignAds) > 4:
            filterTrackingAdList(campaignAds)
        if len(campaignAds) < 4:
            pullAdsIntoCampaign(campaign, campaignAds)
            campaign.getAds()
            campaignAds = [x for x in  AdUtils.listAd(listValues) if "TRACKING" in x["name"] and x["active"] == True]

        numberOfAds = len(placementAds)
        print(numberOfAds)
        if numberOfAds < 4:
            finalPlacementArray.append(filterPlacement(placementObject, campaign["name"]))
            for ad in campaignAds:
                adObject = AdUtils.getAd(ad)
                AdUtils.associatePlacement(adObject, placement)

headerObject = {"A1":"Campaign Name", "B1":"Placement ID", "C1":"Placement Name"}
ReportUtils.printResult(finalPlacementArray,headerObject,"Placements")