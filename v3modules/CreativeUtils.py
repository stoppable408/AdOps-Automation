

def getCreative(Api, CreativeId):
    print(Api)
    creative = Api.generateRequestUrl("creatives",objectId=CreativeId).get().response
    return creative

def listCreatives(Api, listValues=None):
    creativeList = Api.generateRequestUrl("creatives",listValues=listValues).getlist("creatives").response
    return creativeList
