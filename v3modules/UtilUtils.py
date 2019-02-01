

def printResult(array,headerObject,fileName):
    import pandas as pd
    df = pd.DataFrame(data=array)
    writer = pd.ExcelWriter('{filename}.xlsx'.format(filename=fileName),engine='xlsxwriter')
    workbook = writer.book
    # headerObject = {"A1":"Campaign Name", "B1":"Placement ID", "C1":"Placement Name"}
    format1 =  workbook.add_format({'bg_color': '#0AADE9'})
    df.to_excel(writer, sheet_name ="sheet", index = False)
    worksheet =  writer.sheets['sheet']
    for obj in headerObject:
        worksheet.write(obj, headerObject[obj], format1) 
    writer.save()


def formatDateTime(datetimeString):
    import datetime
    date = datetimeString.split('T')[0]
    time = datetimeString.split('T')[1]
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = int(date.split('-')[2])
    date = datetime.date(year,month,day)
    date = date.strftime("%m/%d/%y")
    hour = int(time.split(':')[0])
    minute = int(time.split(':')[1])
    time = datetime.time(hour,minute)
    time = time.strftime("%I:%M %p")
    return (date + " " +  time)


def formatPlacementDate(placementDate):
    import datetime
    return datetime.datetime.strptime(placementDate, "%Y-%m-%d").strftime("%m/%d/%Y")

def placementDateToDatetime(placementDate):
    import datetime
    return datetime.datetime.strptime(placementDate, "%Y-%m-%d")


def TimestampToPlacementDate(placementDate):
    return placementDate.strftime("%m/%d/%Y")

def getBeginningofWeek():
    from datetime import datetime, timedelta
    currentdate = (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return currentdate

def getBeginningofYear():
    from datetime import datetime
    beginningOfYear = datetime(2018, 1,1).strftime("%Y-%m-%dT%H:%M:%SZ")
    return beginningOfYear

def getYesterday():
    from datetime import datetime, timedelta
    currentdate = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
    return currentdate

def datetimeToString(dt):
    import datetime
    timeZoneCorrection =  datetime.timedelta(hours = 3)
    dt = dt + timeZoneCorrection
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def datetimeToStringNoCorrection(dt):
    import datetime
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def stringToDateTimeObject(string):
    import datetime
    return datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%S.%fZ")

