import pandas
import numpy
import time
import os
from v3modules import Smartsheets, PlacementUtils, CampaignUtils, DCMAPI, MailUtils, UtilUtils

Api = DCMAPI.DCMAPI()
csvpath = "https://drive.google.com/uc?export=download&id=1_qaMXaX8TlI6-v8cBuI0XDZ5zDKqOoxF"
fileList = []
import requests
import shutil
import pandas
import os
p = requests.get(csvpath, verify=True,stream=True)
p.raw.decode_content = True
with open("placement info.csv", 'wb') as f:
            shutil.copyfileobj(p.raw, f)
print("done")


def filterPlacementInfo():
    today = pandas.Timestamp.today()
    path = os.getcwd()+"\\placement info.csv"
    print("reading csv")
    parse_dates = ['start_date', 'end_date']
    df = pandas.read_csv(path, parse_dates=parse_dates)
    print("done")
    tpsCond = (df["placement_name"].str.contains("_TPS_") | df["placement_name"].str.contains("»TPÂ»") | df["placement_name"].str.contains("»TP»") )
    cancelledCond = -(df["placement_name"].str.contains("CANCELLED"))
    campaignCond = df["campaign_name"].str.contains("LMA")
    startDateBeforeCond = df["start_date"].apply(lambda x: x < today)
    endDateAfterCond =  df["end_date"].apply(lambda x: x > today)
    filter = tpsCond & campaignCond & startDateBeforeCond & endDateAfterCond & cancelledCond
    df = df[filter]
    return df

def analyzeReport(series):
    global currentCSDList
    def analyzeRow(row):
        def getCSDCreatives(placementId, campaignSheet):
            if type(campaignSheet) == str :
                placementObject = {"campaignName": campaignName, "placementName":row["placement_name"], "placementId":placementId, "start_date": UtilUtils.TimestampToPlacementDate(row["start_date"]), "end_date":UtilUtils.TimestampToPlacementDate(row["end_date"]), "error": "Campaign Missing or Mispelled on CSD"}
                return placementObject
            try:
                creativeArray = campaignSheet.loc[campaignSheet["Id"] == numpy.int64(placementId)].iloc[0].values.tolist()
            except:
                placementObject = {"campaignName": campaignName, "placementName":row["placement_name"], "placementId":placementId, "start_date": UtilUtils.TimestampToPlacementDate(row["start_date"]), "end_date":UtilUtils.TimestampToPlacementDate(row["end_date"]),"error": "Placement Not on CSD"}
                return placementObject
            creativeArray = creativeArray[9:len(creativeArray)]
            creativeArray = [x for x in creativeArray if isinstance(x,str)]
            if len(creativeArray) == 0:
                placementObject = {"campaignName": campaignName, "placementName":row["placement_name"], "placementId":placementId, "start_date": UtilUtils.TimestampToPlacementDate(row["start_date"]), "end_date":UtilUtils.TimestampToPlacementDate(row["end_date"]), "error": "No creative direction on CSD"}
                return placementObject
            return None
        campaignName = row["campaign_name"].strip()
        if campaignName not in currentCSDList:
            try:
                rowID = csdDict[campaignName][1]
                sheetID = csdDict[campaignName][0]
                currentCSDList[campaignName] = Smartsheets.getCSD(sheetID,rowID)
            except:
                print("cannot find " + campaignName)
        try:
            campaignCSD = currentCSDList[campaignName]
        except:
            print(campaignName)
            campaignCSD = "None"
        finalPlacementArray.append(getCSDCreatives(row["placement_id"], campaignCSD))

    series.apply(analyzeRow, axis=1)
    # def getPlacement(placement_id):
    #     global currentCSDList
    #     placement = PlacementUtils.getPlacement(Api,placement_id)
    #     campaignName = CampaignUtils.getCampaign(Api, placement["campaignId"])["name"].strip()
    #     if "CANCELLED" in placement["name"]:
    #         return
    #     print(campaignName)
    #     if campaignName not in currentCSDList:
    #         rowID = csdDict[campaignName][1]
    #         sheetID = csdDict[campaignName][0]
    #         currentCSDList[campaignName] = Smartsheets.getCSD(sheetID,rowID)
    #     isTrafficked = PlacementUtils.checkIfTrafficked(Api, placement,currentCSDList[campaignName])
    #     for key in isTrafficked:
    #         series.loc[series.placement_id==int(placement_id), key] = isTrafficked[key]
    #     series.loc[series.placement_id==int(placement_id), "start_date"] = placement["pricingSchedule"]["startDate"]
    #     series.loc[series.placement_id==int(placement_id), "end_date"] = placement["pricingSchedule"]["endDate"]
    # placementList = series["placement_id"]
    # print(len(placementList))
    # placementList.apply(getPlacement)

finalPlacementArray = []
csdDict = Smartsheets.completeCSDDict()
currentCSDList = {}
df = filterPlacementInfo()


print(type(df))
analyzeReport(df)
finalPlacementArray = [x for x in finalPlacementArray if x != None]
df = pandas.DataFrame(data=finalPlacementArray)
df = df[["campaignName","placementName","placementId","start_date","end_date","error"]]
writer = pandas.ExcelWriter('Empty Creative Report.xlsx',engine='xlsxwriter')
df.to_excel(writer, sheet_name ="Info", index = False)
writer.save()