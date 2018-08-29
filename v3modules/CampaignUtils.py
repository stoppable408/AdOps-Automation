

def getCampaign(Api,campaignID):
    campaign = Api.generateRequestUrl("campaigns",objectId=campaignID).get().response
    return campaign

def getCampaignByName(Api, listValues):
    campaignList = Api.generateRequestUrl("campaigns",listValues=listValues).getlist("campaigns").response
    return campaignList[0]

def getAllLMA(Api):
    listValues =[{"searchString":"1LM*","active":True,"archived":False},{"searchString":"2LM*","active":True,"archived":False},{"searchString":"3LM*","active":True,"archived":False},{"searchString":"4LM*","active":True,"archived":False},{"searchString":"5LM*","active":True,"archived":False}]
    campaignList = []
    for obj in listValues:
        campaignList.extend(Api.generateRequestUrl("campaigns",listValues=obj).getlist("campaigns").response)
    return campaignList

def getAllCampaigns(Api):
    campaignList = Api.generateRequestUrl("campaigns",listValues={"searchString":"2018","active":True,"subaccountId":23262}).getlist("campaigns").response
    return campaignList

def verifyCampaign(Api, campaignId):
    requestBody = {"adBlockingConfiguration": {"enabled": True,"overrideClickThroughUrl": True,"clickThroughUrl": "https://smokeybear.com/en"}}
    Api.generateRequestUrl("campaigns",listValues={"id":campaignId}).patch(requestBody)

def insertCreativeAssociation(Api, creativeID,campaignId):
    objectType = "campaigns"
    objectId = campaignId
    secondaryObjectType= "campaignCreativeAssociations"
    requestBody = {"kind": "dfareporting#campaignCreativeAssociation","creativeId": creativeID}
    Api.generateRequestUrl(objectType,objectId=objectId,secondaryObjectType=secondaryObjectType).insert(requestBody)

def getCreativeAssociation(Api, campaignId):
    def stripArray(array):
        newArray = []
        for element in array:
            newArray.append(element["creativeId"])
        return newArray
    objectType = "campaigns"
    objectId = campaignId
    secondaryObjectType= "campaignCreativeAssociations"
   
    creativeAssociations = Api.generateRequestUrl(objectType,objectId=objectId,secondaryObjectType=secondaryObjectType).getlist(objectType,secondaryObjectType=secondaryObjectType,objectId=objectId).response
    return stripArray(creativeAssociations)

