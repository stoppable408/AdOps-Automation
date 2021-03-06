
def getAd(Api,AdId):
    ad = Api.generateRequestUrl("ads",objectId=AdId).get().response
    return ad

def listAd(Api, listValues=None,filter=False):
    adList = Api.generateRequestUrl("ads",listValues=listValues).getlist("ads").response
    if filter:
        adList = [x for x in adList if "Brand-neutral" not in x['name'] and "TRACKING" not in x["name"] and x["active"] == True and "AD_SERVING_DEFAULT_AD" not in x["type"] and "AD_SERVING_TRACKING" not in x["type"]]
    return adList

def updateAd(Api, adId, payload):
    Api.generateRequestUrl("ads",listValues={"id":adId}).patch(payload)

def insertEventTag(Api, adId, payload):
    currentAd = getAd(Api, adId)
    try:
        currentAd["eventTagOverrides"].append(payload)
        tagArray = currentAd["eventTagOverrides"]
    except:
        tagArray = [payload]
    eventTagOverrides = {"eventTagOverrides":tagArray}
    Api.generateRequestUrl("ads",listValues={"id":adId}).patch(eventTagOverrides)

def inheritEventTag(Api, adId, payload):
    eventTagProperties = {"defaultClickThroughEventTagProperties":payload}
    Api.generateRequestUrl("ads",listValues={"id":adId}).patch(eventTagProperties)

def disinheritEventTag(Api, adId, payload):
    eventTagProperties = {"defaultClickThroughEventTagProperties":{}}
    Api.generateRequestUrl("ads",listValues={"id":adId}).patch(eventTagProperties)

def removeEventTag(Api, adId, payload):
    currentAd = getAd(Api, adId)
    finalTagArray = [x for x in currentAd["eventTagOverrides"] if x != payload ]
    eventTagOverrides = {"eventTagOverrides":finalTagArray}
    Api.generateRequestUrl("ads",listValues={"id":adId}).patch(eventTagOverrides)
    # eventTagOverrides = {"defaultClickThroughEventTagProperties":None}
    # Api.generateRequestUrl("ads",listValues={"id":adId}).patch(eventTagOverrides)

def activateAd(adId, Api):
    payload = {"active":True}
    Api.generateRequestUrl("ads",listValues={"id":adId}).patch(payload)

def deactivateAd(adId, Api):
    payload = {"active":False, "archived":True}
    Api.generateRequestUrl("ads",listValues={"id":adId}).patch(payload)

def getCreatives(Api, adId):
    creativeList = []
    ad = getAd(Api, adId)
    for creative in ad["creativeRotation"]["creativeAssignments"]:
        currentCreative = creative['creativeId']
        creativeList.append(currentCreative)
    return creativeList

def copy(Api, adId, campaignID):
    from datetime import datetime, timedelta
    from v3modules import CampaignUtils
    ad = getAd(Api, adId)
    startTime = (datetime.now() + timedelta(days=1)).isoformat() + "Z"
    adCopy = {"name": ad['name'],"campaignId":campaignID, 'endTime': ad["endTime"], "startTime": startTime, 'type':  ad["type"],  'kind': ad['kind'], 'creativeRotation': ad['creativeRotation'], "deliverySchedule":ad["deliverySchedule"], 'sslRequired': ad['sslRequired'], 'sslCompliant':ad['sslCompliant'], 'clickThroughUrlSuffixProperties': ad['clickThroughUrlSuffixProperties'], "placementAssignments":[], "active":False} 
    creativeList = getCreatives(Api, adId)
    creativeAssociations = CampaignUtils.getCreativeAssociation(Api, campaignID)
    for element in creativeList:
        if element not in creativeAssociations:
            print("creative with number {0} not found. Inserting into Campaign".format(element))
            CampaignUtils.insertCreativeAssociation(Api, element,campaignID)
    return adCopy

def insertAd(copy, Api):
    Api.generateRequestUrl("ads").insert(copy)

def associatePlacement(ad,placement, Api):
    try:
        ad["placementAssignments"]
    except:
        ad["placementAssignments"] = []
    placementObject = {"active":True, "placementIdDimensionValue":placement["idDimensionValue"], "sslRequired":placement["sslRequired"], "placementId":placement["id"]}
    if placementObject not in ad['placementAssignments']:
        ad['placementAssignments'].append(placementObject)
        payload = {"placementAssignments" : ad['placementAssignments']}
        Api.generateRequestUrl("ads",listValues={"id":ad["id"]}).patch(payload)
        activateAd(ad["id"], Api)



