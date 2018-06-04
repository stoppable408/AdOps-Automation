from modules.ChangeLogs import ChangeLogs


def getBeginningofWeek():
    from datetime import datetime, timedelta
    currentdate = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return currentdate


currentDate = getBeginningofWeek()
changeLog = ChangeLogs().getNewPlacements(currentDate).activateTrackingAds().modifySSPlacements().getNewCampaigns(currentDate).verifyCampaigns()


