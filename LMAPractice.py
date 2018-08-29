import pandas
import numpy
import time
import os
from v3modules import Smartsheets, PlacementUtils, CampaignUtils, DCMAPI

Api = DCMAPI.DCMAPI()
def filterPlacementInfo():
    currentDate = pandas.Timestamp.now()
    beginningOfYear = pandas.Timestamp(2018, 1, 3)
    path = os.getcwd()+"\\placement info.csv"
    print("reading csv")
    parse_dates = ['start_date', 'end_date']
    df = pandas.read_csv(path, parse_dates=parse_dates)
    print("done")
    tpsCond = df["placement_name"].str.contains("_TPS_")
    startdateCond = df["start_date"].apply(lambda x: x >= beginningOfYear)
    enddateCond = df["end_date"].apply(lambda x: currentDate <= x)
    campaignCond = df["campaign_name"].str.contains("LMA")
    monthCond = (df["end_date"] - df["start_date"]).apply(lambda x: x.days > 30)
    notGoodwayCond = (-df["placement_name"].str.contains("Goodway"))
    notGoodwayDisplayCond =  (df["placement_name"].str.contains("Goodway") & df["placement_name"].str.contains("Video"))
    notGoodwayVideo =  (df["placement_dimensions"].str.contains("0x0"))
    filter = tpsCond & startdateCond & enddateCond &campaignCond & monthCond & (notGoodwayCond | (notGoodwayDisplayCond & notGoodwayVideo))
    df = df[filter]
    return df



def analyzeSite(series):
    global currentCSDList
    def getPlacement(placement_id):
        global currentCSDList
        placement = PlacementUtils.getPlacement(Api,placement_id)
        campaignName = CampaignUtils.getCampaign(Api, placement["campaignId"])["name"].strip()
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
        # series.loc[series.placement_id==int(placement.body["id"]), "Trafficked"] = placement.trafficked
        # series.loc[series.placement_id==int(placement.body["id"]), "placement_start_date"] = placement.body["pricingSchedule"]["startDate"]
        # series.loc[series.placement_id==int(placement.body["id"]), "placement_end_date"] = placement.body["pricingSchedule"]["endDate"]
        # series.loc[series.placement_id==int(placement.body["id"]), "creative_name"] = placement.creativeName
        # series.loc[series.placement_id==int(placement.body["id"]), "creative_date"] = placement.creativeDate
        # series.loc[series.placement_id==int(placement.body["id"]), "ad_Start_Time"] = placement.adStart
        # series.loc[series.placement_id==int(placement.body["id"]), "ad_End_Time"] = placement.adEnd
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
    # if site == "YuMe":
        # continue
    # if site != "Goodway Group":
        # continue
    temp = df[df["site_name"]==site]
    analyzeSite(temp)
    temp["PAUSE/SET LIVE"] = numpy.nan
    testseries = temp[["campaign_name","campaign_id","placement_name","placement_id","start_date","end_date","PAUSE/SET LIVE","ad_Start_Time","ad_End_Time","CSD","DCM","creative_date"]]
    writer = pandas.ExcelWriter('{site} Report.xlsx'.format(site=site),engine='xlsxwriter')
    workbook = writer.book
    testseries.to_excel(writer, sheet_name ="Info", index = False)
    worksheet =  writer.sheets['Info']
    writer.save()
        
