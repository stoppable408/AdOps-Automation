
def getChangeLog(Api,listValues=None):
    changeLog = Api.generateRequestUrl("changeLogs",listValues=listValues).getlist("changeLogs").response
    return changeLog



