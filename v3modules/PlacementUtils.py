

def getPlacement(Api, placementID):
    placement = Api.generateRequestUrl("placements",objectId=placementID).get().response
    try:
        placement = correctDate(Api, placement,placement["placementGroupId"])
    except:
        pass
    return placement

def correctDate(Api, placement,placementGroupId):
    placementGroup = Api.generateRequestUrl("placementGroups",objectId=placementGroupId).get().response
    placement["pricingSchedule"]["startDate"] = placementGroup["pricingSchedule"]["startDate"]
    placement["pricingSchedule"]["endDate"] = placementGroup["pricingSchedule"]["endDate"]
    return placement

def listPlacement(Api, listValues=None):
    placementList = Api.generateRequestUrl("placements",listValues=listValues).getlist("placements").response
    return placementList


def getAndFormatSite(Api, placement):
    siteId = placement["siteId"]
    site = Api.generateRequestUrl("sites",objectId=siteId).get().response
    siteName = "{0} ({1})".format(site["name"], site["id"])
    return siteName


def pushStaticClickTracking(Api, placementID):
    payload = {"tagSetting":{"includeClickThroughUrls": True,}}
    Api.generateRequestUrl("placements",listValues={"id":placementID}).patch(payload)

def sizeToDimension(sizeObject):
    finalSize = "{width} x {height}".format(width=sizeObject["width"], height=sizeObject["height"])
    return finalSize

def checkIfTrafficked(Api, placement,csdDict):
    def getCSDCreatives():
        print(placement["id"])
        creativeArray = csdDict.loc[csdDict["Id"] == numpy.int64(placement["id"])].iloc[0].values.tolist()
        creativeArray = creativeArray[9:len(creativeArray)]
        creativeArray = [x for x in creativeArray if isinstance(x,str)]
        return creativeArray
    from v3modules import AdUtils, CreativeUtils, UtilUtils
    print("checking ", placement["name"])
    import datetime
    import numpy
    isTrafficked = {"ad_Start_Time":"Not Trafficked","ad_End_Time":"Not Trafficked","creative_date":"Not Trafficked","DCM":"Not Trafficked","CSD":False,"placement_start_date":placement["pricingSchedule"]["startDate"],"placement_end_date":placement["pricingSchedule"]["endDate"]}
    placementAds = AdUtils.listAd(Api, {"placementIds":placement["id"]},True)
    if len(placementAds) == 0:
        return isTrafficked
    for ads in placementAds:
        try:
            creativeAssignments = ads["creativeRotation"]["creativeAssignments"]
        except:
            continue
        for creative in creativeAssignments:
            creativeID = creative["creativeId"]
            creativeElement = CreativeUtils.getCreative(Api, creativeID)
            timestamp = int(creativeElement["lastModifiedInfo"]["time"]) / 1e3
            creativeName = creativeElement["name"]
            csdCreatives = getCSDCreatives()
            creativeNameToTest = "»".join(creativeName.split("»")[:len(creativeName.split("»"))-3])
            creativeTestingString = None
            for element in csdCreatives:
                creativeTestingString = "»".join(element.split("»")[:len(element.split("»"))-3])
                print(creativeNameToTest, creativeTestingString)
                if creativeNameToTest == creativeTestingString:
                    isTrafficked = {"ad_Start_Time":UtilUtils.formatDateTime(ads["startTime"]),"ad_End_Time":UtilUtils.formatDateTime(ads["endTime"]),"creative_date":datetime.datetime.fromtimestamp(timestamp).strftime('%m/%d/%y %I:%M %p'),"DCM":creativeName,"CSD":True,"placement_start_date":placement["pricingSchedule"]["startDate"],"placement_end_date":placement["pricingSchedule"]["endDate"]}
                    return isTrafficked

            isTrafficked = {"ad_Start_Time":UtilUtils.formatDateTime(ads["startTime"]),"ad_End_Time":UtilUtils.formatDateTime(ads["endTime"]),"creative_date":datetime.datetime.fromtimestamp(timestamp).strftime('%m/%d/%y %I:%M %p'),"DCM":creativeName,"CSD":creativeTestingString,"placement_start_date":placement["pricingSchedule"]["startDate"],"placement_end_date":placement["pricingSchedule"]["endDate"]}
    return isTrafficked

