
def getEvent(Api,EventId):
    eventTag = Api.generateRequestUrl("eventTags",objectId=EventId).get().response
    return eventTag

def listEvents(Api, listValues=None):
    EventList = Api.generateRequestUrl("eventTags",listValues=listValues).getlist("eventTags").response
    return EventList

def insertEvent(Api, eventBody):
    Api.generateRequestUrl("eventTags").post(eventBody)