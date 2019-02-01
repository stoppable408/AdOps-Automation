import pandas
import numpy
import time
import os
from v3modules import Smartsheets, PlacementUtils, CampaignUtils, DCMAPI, MailUtils

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
    currentDate = pandas.Timestamp.now()
    beginningOfYear = pandas.Timestamp(2018, 1, 3)
    path = os.getcwd()+"\\placement info.csv"
    print("reading csv")
    parse_dates = ['start_date', 'end_date']
    df = pandas.read_csv(path, parse_dates=parse_dates)
    print("done")
    tpsCond = (df["placement_name"].str.contains("_TPS_") | df["placement_name"].str.contains("»TPÂ»") | df["placement_name"].str.contains("»TP»") )
    startdateCond = df["start_date"].apply(lambda x: x >= beginningOfYear)
    enddateCond = df["end_date"].apply(lambda x: currentDate <= x)
    campaignCond = df["campaign_name"].str.contains("LMA")
    monthCond = (df["end_date"] - df["start_date"]).apply(lambda x: x.days > 30)
    notGoodwayCond = (-df["placement_name"].str.contains("Goodway"))
    goodwayVideo =  (df["placement_name"].str.contains("»FP»") | df["placement_name"].str.contains("»NC»") | df["placement_name"].str.contains("»TV»") | df["placement_name"].str.contains("»VP»") | df["placement_name"].str.contains("»VO»") | df["placement_name"].str.contains("»VS»")|df["placement_name"].str.contains("»RC»") )
    notGoodwayDisplayCond =  (df["placement_name"].str.contains("Goodway") & goodwayVideo)
    notGoodwayVideo =  (df["placement_dimensions"].str.contains("0x0"))
    filter = tpsCond & startdateCond & enddateCond & campaignCond & monthCond & (notGoodwayCond | (notGoodwayDisplayCond & notGoodwayVideo))
    df = df[filter]
    return df



def analyzeSite(series):
    global currentCSDList
    def getPlacement(placement_id):
        global currentCSDList
        placement = PlacementUtils.getPlacement(Api,placement_id)
        campaignName = CampaignUtils.getCampaign(Api, placement["campaignId"])["name"].strip()
        if "CANCELLED" in placement["name"]:
            return
        print(campaignName)
        if campaignName not in currentCSDList:
            rowID = csdDict[campaignName][1]
            sheetID = csdDict[campaignName][0]
            currentCSDList[campaignName] = Smartsheets.getCSD(sheetID,rowID)
        isTrafficked = PlacementUtils.checkIfTrafficked(Api, placement,currentCSDList[campaignName])
        for key in isTrafficked:
            series.loc[series.placement_id==int(placement_id), key] = isTrafficked[key]
        series.loc[series.placement_id==int(placement_id), "start_date"] = placement["pricingSchedule"]["startDate"]
        series.loc[series.placement_id==int(placement_id), "end_date"] = placement["pricingSchedule"]["endDate"]
    placementList = series["placement_id"]
    print(len(placementList))
    placementList.apply(getPlacement)

csdDict = Smartsheets.completeCSDDict()
currentCSDList = {}
df = filterPlacementInfo()
siteList = list(set(df["site_name"].tolist()))

print(siteList)
for site in siteList:
    print(site)
    temp = df[df["site_name"]==site]
    try:
        analyzeSite(temp)
    except Exception as e:
        errorFile = open("error.txt","a")
        errorFile.write(str(site) + ": " + str(e) + "\n")
        errorFile.close()
    temp["PAUSE/SET LIVE"] = numpy.nan
    try:
        testseries = temp[["campaign_name","campaign_id","placement_name","placement_id","start_date","end_date","PAUSE/SET LIVE","ad_Start_Time","ad_End_Time","CSD","DCM","creative_date"]]
    except:
        testseries = temp[["campaign_name","campaign_id","placement_name","placement_id","start_date","end_date","PAUSE/SET LIVE"]]
    writer = pandas.ExcelWriter('{site} Report.xlsx'.format(site=site),engine='xlsxwriter')
    fileList.append('{site} Report.xlsx'.format(site=site))
    workbook = writer.book
    testseries.to_excel(writer, sheet_name ="Info", index = False)
    worksheet =  writer.sheets['Info']
    writer.save()
        
MailUtils.send_email(fileList, "LMA Reports", "Attached are the LMA Reports for today", ["Lennon.Turner@carat.com", "Kristine.Gillette@carat.com", "Mike.DOrazio@carat.com","Holly.Champoux@carat.com"])
