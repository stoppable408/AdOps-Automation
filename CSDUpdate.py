import os
import pandas as pd
import numpy as np
import datetime
from v3modules import DCMAPI, CampaignUtils, PlacementUtils
Api = DCMAPI.DCMAPI()
fileList = [x for x in os.listdir() if ("csv" in x or "xlsx" in x) and "CSD" in x]

def determineDimensions(placement):
    if placement["compatibility"] == 'IN_STREAM_VIDEO' or "_SS_" in placement["name"]:
        return str(placement["name"]).split("_")[3]
    else:
        return PlacementUtils.sizeToDimension(placement["size"])
        

def sliceContacts(sheet):
    indexofSite = sheet.loc[sheet["Campaign"] == "Site"].index.values[0]
    contactRows = sheet[indexofSite:]
    originalSheet = sheet[:indexofSite].dropna(how="all")
    return {"sheet": originalSheet, "contacts":contactRows}

def appendContacts(sheet, contacts):
    for i in range(3):
        sheet = sheet.append(
        pd.Series(
            [np.nan,np.nan,np.nan,np.nan,np.nan,
             np.nan,np.nan,np.nan,np.nan,np.nan,
             np.nan,np.nan,np.nan,np.nan,],
            index=sheet.columns.tolist()),ignore_index=True)
    index = len(sheet) + 2
    sheet = sheet.append(contacts, ignore_index=True)
    return {"sheet":sheet, "siteIndex":index}

def updateSheet(sheet, placementList):
    DCMidList = set([int(x["id"]) for x in placementList])
    CSDidList = set(sheet["Id"].tolist())
    for placement in DCMidList.copy():
        if placement in CSDidList:
            DCMidList.remove(placement)
            CSDidList.remove(placement)
            currentPlacement = PlacementUtils.getPlacement(Api, placement)
            placementData = {"Name": currentPlacement["name"], "Start Date": currentPlacement["pricingSchedule"]["startDate"], "End Date":currentPlacement["pricingSchedule"]["endDate"], "Dimensions":determineDimensions(currentPlacement)}
            for key in placementData:
                sheet.loc[sheet.Id==placement, key] = placementData[key]
    if len(DCMidList) > 0:
        campaignName = sheet.iloc[0]["Campaign"]
        siteName = sheet.iloc[0]["Site"]
        for placement in DCMidList:
            currentPlacement = PlacementUtils.getPlacement(Api, placement)

            placementData = {"Campaign":campaignName, "Site": siteName,"Id": placement ,"Name": currentPlacement["name"], "Start Date": datetime.datetime.strptime(currentPlacement['pricingSchedule']['startDate'], '%Y-%m-%d').strftime('%m/%d/%Y'), "End Date":datetime.datetime.strptime(currentPlacement['pricingSchedule']['endDate'], '%Y-%m-%d').strftime('%m/%d/%Y'), "Compatibility":currentPlacement["compatibility"].capitalize(), "Dimensions":determineDimensions(currentPlacement)}
            sheet = sheet.append(placementData, ignore_index=True)
    if len(CSDidList) > 0:
         for placement in CSDidList:
             sheet = sheet[sheet.Id != placement]

    return sheet


for file in fileList:
    excel = pd.read_excel(file, sheet_name=None)
    writer = pd.ExcelWriter('Merged_%s' % (file),engine='xlsxwriter')
    workbook = writer.book
    format1 =  workbook.add_format({'bg_color': '#0AADE9'})

    campaignName = excel["TPS Placements"].iloc[0]["Campaign"]
    listValues = {"searchString":campaignName}
    campaign = CampaignUtils.getCampaignByName(Api, listValues)
    listValules = {"campaignIds":campaign["id"]}
    placementList = [x for x in PlacementUtils.listPlacement(Api, listValules) if x["archived"] == False ] 
    TPSPlacements = [x for x in placementList if "_TPS_" in x["name"]]
    SSPlacements = [x for x in placementList if "_SS_" in x["name"]]
    TPSsheet = updateSheet(excel["TPS Placements"], TPSPlacements)
    excel["TPS Placements"] = TPSsheet
    if len(SSPlacements) > 0:
        sheetObject = sliceContacts(excel["SS Placements"])
        SSsheet = updateSheet(sheetObject["sheet"], SSPlacements)
        SSsheet = appendContacts(SSsheet, sheetObject["contacts"])
        excel["SS Placements"] = SSsheet["sheet"]


    headerObject = {"A1":"Campaign", "B1":"Site", "C1":"Id", "D1":"Name","E1":"Start Date","F1":"End Date","G1":"Compatibility","H1":"Dimensions","I1":"Creative Rotation","J1":"Creative File 1","K1":"Creative File 2","L1":"Creative File 3","M1":"Creative File 4","N1":"Creative File 5"}
    urlObject = {'A1':"Creative File", "B1":"Creative URL"}
    siteObject = {'A' + str(SSsheet["siteIndex"]):"Site", 'B' + str(SSsheet["siteIndex"]):"Contact"}
    TPSsheet.to_excel(writer, sheet_name="TPS Placements",index=False)
    TPSworksheet = writer.sheets['TPS Placements']
    for obj in headerObject:
        TPSworksheet.write(obj, headerObject[obj], format1) 


    SSsheet["sheet"].to_excel(writer, sheet_name="SS Placements",index=False)
    SSworksheet = writer.sheets['SS Placements']
    for obj in headerObject:
        SSworksheet.write(obj, headerObject[obj], format1)
    for obj in siteObject:
        SSworksheet.write(obj, siteObject[obj], format1)
    excel["URLs"].to_excel(writer, sheet_name="URLs",index=False)
    worksheet_URLs = writer.sheets['URLs']
    for obj in urlObject:
        worksheet_URLs.write(obj, urlObject[obj], format1)

    writer.save()
