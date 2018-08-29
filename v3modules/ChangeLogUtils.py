from v3modules.DCMAPI import DCMAPI

def getChangeLog(listValues=None):
    Api = DCMAPI()
    changeLog = Api.generateRequestUrl("changeLogs",listValues=listValues).getlist("changeLogs")
    return changeLog



