

def getSite(Api, siteId):
    site = Api.generateRequestUrl("sites",objectId=siteId).get().response
    return site