
from v3modules import DCMAPI, ChangeLogUtils, PlacementUtils, CampaignUtils, UtilUtils, AdUtils, MailUtils
import re, pandas

Api = DCMAPI.DCMAPI()
regex = re.compile("[1-5]L(M|G)")
def checkSubAccount(x):
    try:
        if x["subaccountId"] == "23262":
            return True
        else:
            return False
    except:
        return False
def checkCampaign(x):
    placement = PlacementUtils.getPlacement(Api, x["objectId"])
    print("checking " + placement["name"])
    campaign = CampaignUtils.getCampaign(Api, placement["campaignId"])
    if regex.search(campaign["name"]): 
        return placement
    else:
        return None


def getModifiedAds(adsToUse,existingads):
    modifiedAds = []
    existingads = [x["name"].strip() for x in existingads]
    for ad in adsToUse:
        currentAd = AdUtils.getAd(Api,ad)
        adName = currentAd["name"]
        if adName.strip() not in existingads:
            modifiedAds.append(ad)
    return modifiedAds


def pullAdsIntoCampaign(campaignId, placement, campaignAdList):
    print("pulling ads")
    campaign = CampaignUtils.getCampaign(Api, campaignId)
    videocodes = ["»FP»","»NC»","»TV»","»VP»","»VO»","»VS»"]
    englishAds = ["431196351","431196357", "431196360", "431196366"]
    spanishAds = ["431196348", "431196354","431196363", "431196345"]
    videoAds = ["431196342","431196372","431196375","431196369"]
    videoHispAds = ["433756626","433757505","433830394","433832422"]
    adsToUse = None
    name = placement["name"]
    campaignName = campaign["name"]
    if "Hispanic" in campaignName:
        adsToUse = spanishAds
    else:
        adsToUse = englishAds
    for code in videocodes:
        if code in name:
            if "Hispanic" in campaignName:
                adsToUse = videoHispAds
                break
            else:
                adsToUse = videoAds
                break
    if len(campaignAdList) == 0:
        adsToUse = getModifiedAds(adsToUse, campaignAdList)
    for ads in adsToUse:
        copy = AdUtils.copy(Api, ads, campaignId)
        AdUtils.insertAd(copy, Api)

listValues = {"action": "ACTION_CREATE", "objectType":"OBJECT_PLACEMENT", "minChangeTime":UtilUtils.getYesterday()}
Createlogs = ChangeLogUtils.getChangeLog(Api, listValues)
Createlogs = [x for x in Createlogs if "»SS»" in x["newValue"]]
listValues = {"action": "ACTION_UPDATE", "objectType":"OBJECT_PLACEMENT", "minChangeTime":UtilUtils.getYesterday()}
UpdateLogs = ChangeLogUtils.getChangeLog(Api, listValues)
UpdateLogs = [x for x in UpdateLogs if x["fieldName"] == "Name" and "»TP»" in x["oldValue"] and "»SS»" in x["newValue"]]
finalLogs = Createlogs + UpdateLogs
length = str(len(finalLogs))
print(length + " checking each placement Now")
finalLogs = [checkCampaign(x) for x in finalLogs if checkSubAccount(x)]
finalLogs = [x for x in finalLogs if x != None]
length = str(len(finalLogs))
print(length)

finalPlacementArray = []
for placement in finalLogs:
    placementAdList = AdUtils.listAd(Api, {"placementIds":placement["id"]})
    campaignAdList = AdUtils.listAd(Api, {"campaignIds":placement["campaignId"]})
    campaign = CampaignUtils.getCampaign(Api, placement["campaignId"])
    placementAdList = [x for x in placementAdList if "TRACKING" in x["name"] and x["archived"] == False]
    campaignAdList = [x for x in campaignAdList if "TRACKING" in x["name"] and x["archived"] == False]
    PlacementUtils.pushStaticClickTracking(Api, placement["id"])
    if len(campaignAdList) < 4:
        pullAdsIntoCampaign(placement["campaignId"], placement, campaignAdList)
        campaignAdList = AdUtils.listAd(Api, {"campaignIds":placement["campaignId"]})
        campaignAdList = [x for x in campaignAdList if "TRACKING" in x["name"] and x["archived"] == False]
    if len(placementAdList) < 4:
        for ad in campaignAdList:
            adObject = AdUtils.getAd(Api, ad["id"])
            AdUtils.associatePlacement(adObject,placement,Api) 
        finalPlacementArray.append({"Placement Name": placement["name"],"Campaign Name": campaign["name"], "Placement ID":placement["id"]})

if len(finalPlacementArray) > 0:
    df = pandas.DataFrame(data=finalPlacementArray)
    df = df[["Campaign Name", "Placement ID","Placement Name"]]
    writer = pandas.ExcelWriter('Updated SS Placements.xlsx',engine='xlsxwriter')
    workbook = writer.book
    headerObject = {"A1":"Campaign Name", "B1":"Placement ID", "C1":"Placement Name"}
    format1 =  workbook.add_format({'bg_color': '#0AADE9'})
    df.to_excel(writer, sheet_name ="Placements", index = False)
    worksheet =  writer.sheets['Placements']
    for obj in headerObject:
        worksheet.write(obj, headerObject[obj], format1) 
    print("Done!")    
    writer.save()

    MailUtils.send_email(['Updated SS Placements.xlsx'], "Site Served Placment Report", "Attached are the SS Placements that were updated today", ["Lennon.Turner@carat.com", "Kristine.Gillette@carat.com","Mike.DOrazio@carat.com","Holly.Champoux@carat.com","Ali.Ciaffone@carat.com"])

