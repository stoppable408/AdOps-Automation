

def getCreative(Api, CreativeId):
    creative = Api.generateRequestUrl("creatives",objectId=CreativeId).get().response
    return creative

def listCreatives(Api, listValues=None):
    creativeList = Api.generateRequestUrl("creatives",listValues=listValues).getlist("creatives").response
    return creativeList

def updateCreative(Api, creativeId, payload):
    Api.generateRequestUrl("creatives",listValues={"id":creativeId}).patch(payload)