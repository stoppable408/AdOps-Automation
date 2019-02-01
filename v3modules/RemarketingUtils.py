def getRemarketingAudience(Api, audienceId):
    aud = Api.generateRequestUrl("remarketingLists", objectId = audienceId).get.response
    return aud

def getRemarketingList(Api, listValues, requiredParameter=None):
    if requiredParameter == None:
        rmktList = Api.generateRequestUrl("remarketingLists", listValues = listValues).getlist("remarketingLists").response
    else: 
        rmktList = Api.generateRequestUrl("remarketingLists", listValues = listValues).getlist("remarketingLists", requiredParameter=requiredParameter).response
    return rmktList

def updateRemarketingList(Api, audienceId, payload):
    payload = payload
    Api.generateRequestUrl("remarketingLists",listValues={"id":audienceId}).patch(payload)