from v3modules import DCMAPI, PlacementUtils, SiteUtils, ChangeLogUtils, UtilUtils, CampaignUtils
import datetime
Api = DCMAPI.DCMAPI()

finalPlacementList = []
noTranscodes = set()
transcodes = {
    "Samsung AdHub":(PlacementUtils.getPlacement(Api, 237980865),'1552768'),
    "National Cable Communications, LLC (NCC Media)": (PlacementUtils.getPlacement(Api, 227647455), '1483997'),
    "Gamut Media": (PlacementUtils.getPlacement(Api, 236055453),'3135124'),
    "Pulpo Media": (PlacementUtils.getPlacement(Api, 236970593),'1454811'),
    "KSL TV": (PlacementUtils.getPlacement(Api, 237246942),'4259704'),
    "Amazon AAP - SS":(PlacementUtils.getPlacement(Api, 237803655),'5087264'),
    "Hulu Latino": (PlacementUtils.getPlacement(Api, 236696286),'3161248'),
    "EMX Digital": (PlacementUtils.getPlacement(Api, 235786514),'4942271'),
    "Comcast Digital": (PlacementUtils.getPlacement(Api, 235823848),'4212262'),
    "Amobee": (PlacementUtils.getPlacement(Api, 235819558),'1547892'),
    "Premion": (PlacementUtils.getPlacement(Api, 227647443),'4161236'),
    "roku.com": (PlacementUtils.getPlacement(Api, 237116714),'2259437'),
    "Crackle.com":(PlacementUtils.getPlacement(Api, 237447154),'2709502'),
    "FoxSports.com": (PlacementUtils.getPlacement(Api, 237777513),'1512120'),
    "Hulu.com 1": (PlacementUtils.getPlacement(Api, 227393591),'1408680'),
    "Conversant, Inc": (PlacementUtils.getPlacement(Api, 235826116),'2216548'),
    "Univision": (PlacementUtils.getPlacement(Api, 237105971),'1388034'),
    "CBS Interactive": (PlacementUtils.getPlacement(Api, 227390249),'1378712'),
    "ABC.com": (PlacementUtils.getPlacement(Api, 227644293),'1408682'),
    "Compulse": (PlacementUtils.getPlacement(Api, 235811470),'5038911'),
    "Google - YouTube": (PlacementUtils.getPlacement(Api, 227393273),'1376944'),
    "Adsmovil.com": (PlacementUtils.getPlacement(Api, 227640675),'1729982'),
    "Comcast Spotlight - Houston": (PlacementUtils.getPlacement(Api, 227392295),'4484092'),
    "Fox Broadcasting Network - Fox Television": (PlacementUtils.getPlacement(Api, 236424874),'1865505'),
    "NBC Universal": (PlacementUtils.getPlacement(Api, 227649438),'1408681'),
    "Oath.com": (PlacementUtils.getPlacement(Api, 227481958),'4141356'),
    "2060 Digital": (PlacementUtils.getPlacement(Api, 235823299),'5054731'),
    "teads.tv": (PlacementUtils.getPlacement(Api, 236062704),'2127777'),
    "ESPN": (PlacementUtils.getPlacement(Api, 236415854),'1375549'),
    "WFLA Tampa": (PlacementUtils.getPlacement(Api, 235823887),'4643002'),
    "Walt Disney Internet Group - ABC.com": (PlacementUtils.getPlacement(Api, 236413424),'1408685'),
    "Spot X": (PlacementUtils.getPlacement(Api, 235804403),'5014190'),
    "Katz Media": (PlacementUtils.getPlacement(Api, 237203790),'4909861'),
    "AdTheorent, Inc": (PlacementUtils.getPlacement(Api, 235848649),'4444630'),
    "Pandora": (PlacementUtils.getPlacement(Api, 227393675),'1379001'),
    "QuantCast": (PlacementUtils.getPlacement(Api, 235850971),'1407713'),
    "FX Networks": (PlacementUtils.getPlacement(Api, 238364707),'4365346'),
    "The CW Television Network": (PlacementUtils.getPlacement(Api, 227394887),'1518998')
}
def checkPlacementEndDate(date):
    today = datetime.datetime.now()
    try:
        placementDate = datetime.datetime.strptime(date, "%m/%d/%Y")
    except:
        placementDate = datetime.datetime.strptime(date, "%Y-%m-%d")
    return today < placementDate
def checkVideo(placement):
    videocodes = ["»FP»","»NC»","»TV»","»VP»","»VO»","»VS»"]
    for code in videocodes:
        if code in placement:
            return True
    return False
def checkSite(siteId):
    for site in transcodes:
        if siteId == transcodes[site][1]:
            return True
    return False
def getSite(siteId):
    for site in transcodes:
        if siteId == transcodes[site][1]:
            return transcodes[site][0]
def compareVideoSettings(placement,template):
    try:
        placement["videoSettings"]["transcodeSettings"]["enabledVideoFormats"]
    except:
        try:
            placement["videoSettings"]["transcodeSettings"]= {'kind':'dfareporting#transcodeSetting','enabledVideoFormats':[]}
        except:
            placement["videoSettings"] = {}
    try:
        transcodes = template["videoSettings"]["transcodeSettings"]["enabledVideoFormats"]
    except:
        template["videoSettings"]["transcodeSettings"]= {'kind':'dfareporting#transcodeSetting','enabledVideoFormats':[]}
    try:
        sameVideoSettings = placement["videoSettings"] == template["videoSettings"]
        sameVideoActiveInput = placement["videoActiveViewOptOut"] == template["videoActiveViewOptOut"]
        sameVideoAdapterChoice = placement["vpaidAdapterChoice"] == template["vpaidAdapterChoice"]
        sameAdBlocking = placement["adBlockingOptOut"] == template["adBlockingOptOut"] 
        if sameVideoSettings and sameVideoActiveInput and sameVideoAdapterChoice and sameAdBlocking:
            return True
        else:
            return False
    except:
        return False
def excludePlacements(name):
    namesToExclude = ["PT0VDQ","PWDG1Q"]
    for names in namesToExclude:
        if names in name:
            return False
    return True

def TempAnalyzePlacement(placement):
    isLMA = PlacementUtils.checkLMA(Api, placement)
    if isLMA:
        placement = PlacementUtils.getPlacement(Api,placement["id"])
        date = datetime.datetime(2019,2,1)
        placementStartDate = UtilUtils.placementDateToDatetime(placement["pricingSchedule"]["startDate"])
        if placementStartDate > date:
            try:
                if "enabledVideoFormats" not in placement["videoSettings"]["transcodeSettings"]:
                    return True
                placement["videoSettings"]["transcodeSettings"]["enabledVideoFormats"] = {'kind':'dfareporting#transcodeSetting','enabledVideoFormats':[]}
            except:
                try:
                    placement["videoSettings"]["transcodeSettings"]= {'kind':'dfareporting#transcodeSetting','enabledVideoFormats':[]}
                except:
                    placement["videoSettings"] = {}

            PlacementUtils.updatePlacement(Api, {"videoSettings":placement["videoSettings"]}, placement["id"])
            return True
        else:
            return True
    return False


listValues = {"minStartDate":"2019-01-01","active":True,"archived":False}
placementList = PlacementUtils.listPlacement(Api,listValues)
NonSitePlacements =[x for x in placementList if  "»TP»" in x["name"] and checkVideo(x['name']) and not checkSite(x["siteId"])]
SiteplacementList = [x for x in placementList if  "»TP»" in x["name"] and checkVideo(x['name']) and checkSite(x["siteId"]) and excludePlacements(x["name"])]
for placement in NonSitePlacements:
    activeView = placement['videoActiveViewOptOut']
    adapter = placement['vpaidAdapterChoice']
    adBlockingOptOut = placement['adBlockingOptOut']
    if activeView == False and adapter == "DEFAULT" and adBlockingOptOut == False:
        continue
    else:
        if "Amobee" not in placement["name"]:
            videoSettings = {
                "videoActiveViewOptOut": False,
                "vpaidAdapterChoice": "DEFAULT",
                "adBlockingOptOut": False
            }
            PlacementUtils.updatePlacement(Api, videoSettings, placement["id"])
            finalPlacementList.append(placement["name"])

    

for placement in SiteplacementList:
    if "Hulu" in placement["name"]:
        updatedHuluPlacement = TempAnalyzePlacement(placement)
    else:
        updatedHuluPlacement = False
    if not updatedHuluPlacement:
        placementTemplate = getSite(placement["siteId"])
        isEqual = compareVideoSettings(placement,placementTemplate)
        if not isEqual:
            videoSettings = {
                "videoSettings": placementTemplate["videoSettings"],
                "videoActiveViewOptOut": placementTemplate["videoActiveViewOptOut"],
                "vpaidAdapterChoice": placementTemplate["vpaidAdapterChoice"],
                "adBlockingOptOut": placementTemplate["adBlockingOptOut"]
            }
            PlacementUtils.updatePlacement(Api, videoSettings, placement["id"])
            finalPlacementList.append(placement["name"])
        


print(finalPlacementList)
print("--------------------")
print(noTranscodes)
