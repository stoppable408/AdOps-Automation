
def getFloodlight(Api, flid):
    fl = Api.generateRequestUrl("floodlightActivities", objectId = flid).get().response
    return fl