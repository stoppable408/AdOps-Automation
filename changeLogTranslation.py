

def getBeginningofWeek():
    from datetime import datetime, timedelta
    currentdate = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return currentdate

    
ChangeLogObjects = ["OBJECT_AD","OBJECT_CREATIVE","OBJECT_PLACEMENT","OBJECT_CAMPAIGN"]