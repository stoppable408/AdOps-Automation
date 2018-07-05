import pandas
import time
import os
from modules.Placements import Placement

currentDate = pandas.Timestamp.now()
beginningOfYear = pandas.Timestamp(2018, 1, 3)
start_time = time.time()
path = os.getcwd()+"\\placement_info.csv.xlsx"
print("reading csv")
df = pandas.read_excel(path)
tpsCond = df["placement_name"].str.contains("_TPS_")
startdateCond = df["start_date"].apply(lambda x: x >= beginningOfYear)
enddateCond = df["end_date"].apply(lambda x: currentDate <= x)
campaignCond = df["campaign_name"].str.contains("LMA")
monthCond = (df["end_date"] - df["start_date"]).apply(lambda x: x.days > 30)
notGoodwayCond = (-df["placement_name"].str.contains("Goodway"))
notGoodwayDisplayCond =  (df["placement_name"].str.contains("Goodway") & df["placement_name"].str.contains("Video")) 
filter = tpsCond & startdateCond & enddateCond &campaignCond & monthCond & (notGoodwayCond | notGoodwayDisplayCond)
df = df[filter]
siteList = list(set(df["site_name"].tolist()))
test=df.iloc[0]["placement_id"]
placement = Placement(test)
initialSession = placement.session
initialEventLoop = placement.eventLoop

def checkSession(obj):
    global initialSession
    if obj.session != initialSession:
        initialSession = obj.session
    return obj
def analyzeSite(series):
    def getPlacement(placement_id):
        placement = checkSession(Placement(placement_id,initialEventLoop,initialSession).isTrafficked())
        series.loc[series.placement_id==int(placement.body["id"]), "Trafficked"] = placement.trafficked
        series.loc[series.placement_id==int(placement.body["id"]), "placement_start_date"] = placement.body["pricingSchedule"]["startDate"]
        series.loc[series.placement_id==int(placement.body["id"]), "placement_end_date"] = placement.body["pricingSchedule"]["endDate"]
        series.loc[series.placement_id==int(placement.body["id"]), "creative_name"] = placement.creativeName
        series.loc[series.placement_id==int(placement.body["id"]), "creative_date"] = placement.creativeDate
        series.loc[series.placement_id==int(placement.body["id"]), "ad_Start_Time"] = placement.adStart
        series.loc[series.placement_id==int(placement.body["id"]), "ad_End_Time"] = placement.adEnd
    placementList = series["placement_id"]
    print(len(placementList))
    placementList.apply(getPlacement)
for site in siteList:
    if site == "Goodway Group":
        continue
    temp = df[df["site_name"]==site]
    analyzeSite(temp)
    import pandas as pd
    testseries = temp[["campaign_name","campaign_id","placement_name","placement_id","placement_start_date","placement_end_date","ad_Start_Time","ad_End_Time","Trafficked","creative_name","creative_date"]]
    writer = pd.ExcelWriter('{site} Report.xlsx'.format(site=site),engine='xlsxwriter')
    workbook = writer.book
    testseries.to_excel(writer, sheet_name ="Info", index = False)
    worksheet =  writer.sheets['Info']
    writer.save()
        

