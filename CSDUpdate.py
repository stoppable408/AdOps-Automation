import os
import pandas as pd
import numpy as np
import datetime
from v3modules import DCMAPI, CampaignUtils, PlacementUtils, UtilUtils
import re
Api = DCMAPI.DCMAPI()
ChangesArray = []
Evidon = ["EV1","EV2","EV3","EVD","EVG","EVL","EVR","EVS","EVA","EVT","EVC","GAC","LMA","LMR","LMC"]
LMA = ["1LM","2LM","3LM","4LM","5LM","1LG","2LG","3LG","4LG","5LG"]
LMAOverride = False
RemovedPlacements = pd.DataFrame()
fileList = [x for x in os.listdir() if ("csv" in x or "xlsx" in x) and "CSD" in x]
currentDate = datetime.datetime.now()
CampaignName = None

def assignColumns(df, x):
    df[x] = x
    return None
#Sometimes the contact section of a CSD has no information, as such, this function exists in order to turn numpy.nan into an empty string.
def nanToNone(obj):
    try:
        if np.isnan(obj):
            return ""
    except:
        return obj
    return obj

def floatToPercent(fl):
    try:
        if np.isnan(fl):
            return fl
        if fl <= 1:
            return "%.0f%%" % (100 * fl)
        else: 
            return "%.0f%%" % (fl)
    except:
        return fl
def isEvidon(placementName):
    LMAOverride
    if LMAOverride == True:
        return "Y"
    for string in Evidon:
        if string in placementName:
            return "Y"
    return "N"

def checkPlacementEndDate(date):
    today = datetime.datetime.now()
    try:
        placementDate = datetime.datetime.strptime(date, "%m/%d/%Y")
    except:
        placementDate = datetime.datetime.strptime(date, "%Y-%m-%d")
    return today > placementDate

def datetimeToDate(date):
    if type(date) == pd._libs.tslibs.timestamps.Timestamp:
        return date.strftime("%m/%d/%Y")
    if type(date) == datetime.datetime:
        return datetime.datetime.strftime(date, "%m/%d/%Y")
    if type(date) == np.datetime64:
        return pd.to_datetime(str(date)).strftime("%m/%d/%Y")
    return date

#If a placement is "Instream-Video" or is a Site-Served Placement, the dimensions are located in the name of the placement, because DCMAPI has incorrect information. Otherwise, refer to the API for the correct dimensions of the placement. 
def determineDimensions(placement):
    if placement["compatibility"] == 'IN_STREAM_VIDEO' or "_SS_" in placement["name"] or  "»SS»" in placement["name"]:
        try:
            dimensions = str(placement["name"]).split("»")[5]
            dimensions = re.sub("\(NA\)\+|\(NA\+\)|NA\+","",dimensions)
            return dimensions
        except:
            return str(placement["name"]).split("_")[3]
    else:
        return PlacementUtils.sizeToDimension(placement["size"])
        
#This function locates the contact section of a SS Placement sheet, and isolates them, so that the can be appended to the end of the new sheet. 
def sliceContacts(sheet):
    indexofSite = sheet.loc[sheet["Campaign"] == "Site"].index.values[0]
    contactRows = sheet[indexofSite:]
    contactArray = []
    for row in contactRows.iterrows():
        
        contactArray.append([row[1].Campaign, row[1].Site])
    originalSheet = sheet[:indexofSite].dropna(how="all")
    return {"sheet": originalSheet, "contacts":contactArray}

#This function creates a contact object that is iterated through later on in the program, in order to append them to the end of the sheet. The reason why this function is seperate is because
#We have to potentially add placements to the SS Sheet, and we have to have the correct index to know where to start appending. 
def appendContacts(sheet, contacts, contactIndex):
    index = contactIndex
    contactArray = []
    for row in contacts:
        Aindex = "A{index}".format(index=index)
        Bindex = "B{index}".format(index=index)
        contactArray.append([Aindex,nanToNone(row[0])])
        contactArray.append([Bindex,nanToNone(row[1])])
        index += 1
    return {"sheet":sheet, "siteIndex":contactArray}

#Main function, for each placement in the sheet, it compares the relevant information of that placement to the information in DCM, if it's different
#the correct information will be appended to an array, with a yellow or red color depending on whether ot not a placement was added or excluded or updated
def updateSheet(sheet, placementList):
    global RemovedPlacements
    global CampaignName
    try:
        sheet['Creative\n Rotation'] = sheet['Creative\n Rotation'].apply(floatToPercent)
    except:
        sheet['Creative Rotation'] = sheet['Creative Rotation'].apply(floatToPercent)
    sheet["Start Date"] = sheet["Start Date"].apply(datetimeToDate)
    sheet["End Date"] = sheet["End Date"].apply(datetimeToDate)
    DCMidList = set([int(x["id"]) for x in placementList])
    CSDidList = set(sheet["Id"].tolist())
    CSDidList = {x for x in CSDidList if x==x}

    placementsToAdd = DCMidList.difference(CSDidList)
    # placementsToRemove = CSDidList.difference(DCMidList)
    for placement in CSDidList.copy():
        print(placement)
        currentPlacement = PlacementUtils.getPlacement(Api, placement)
        CSDPlacement = sheet[sheet.Id == placement]
        if checkPlacementEndDate(currentPlacement["pricingSchedule"]["endDate"]) or currentPlacement["archived"] == True:
            CSDPlacement["End Date"] = UtilUtils.formatPlacementDate(currentPlacement["pricingSchedule"]["endDate"])
            RemovedPlacements=RemovedPlacements.append(CSDPlacement)
            sheet = sheet[sheet.Id != placement]
    CSDidList = set(sheet["Id"].tolist())
    CSDidList = {x for x in CSDidList if x==x}
    sheet = sheet.reset_index(drop=True)
    for placement in CSDidList.copy():
        CSDPlacement = sheet[sheet.Id == placement]
        currentPlacement = PlacementUtils.getPlacement(Api, placement)
        indexOfPlacement = sheet[sheet.Id == placement].index[0] + 2
        if placement in DCMidList:
            if checkPlacementEndDate(currentPlacement["pricingSchedule"]["endDate"]):
                CSDPlacement["End Date"] = UtilUtils.formatPlacementDate(currentPlacement["pricingSchedule"]["endDate"])
                RemovedPlacements=RemovedPlacements.append(CSDPlacement)
                sheet = sheet[sheet.Id != placement]
                sheet = sheet.reset_index(drop=True)
                continue
            DCMidList.remove(placement)
            CSDidList.remove(placement)
            print(CSDPlacement["Id"])
            CSDPlacementInfo = {"D":CSDPlacement["Name"].values[0], "E":CSDPlacement["Start Date"].values[0], "F":CSDPlacement["End Date"].values[0], "H":CSDPlacement["Dimensions"].values[0]}
            DCMPlacementInfo = {"D":currentPlacement["name"], "E":UtilUtils.formatPlacementDate(currentPlacement["pricingSchedule"]["startDate"]), "F":UtilUtils.formatPlacementDate(currentPlacement["pricingSchedule"]["endDate"]), "H":determineDimensions(currentPlacement)}
            for column in CSDPlacementInfo:
                #Sometimes Placement dates can come in as strings, or Datetimes, so we have to convert them just in case. 
                if type(CSDPlacementInfo[column]) == datetime.datetime:
                    CSDPlacementInfo[column] = datetime.datetime.strftime(CSDPlacementInfo[column], "%m/%d/%Y")
                if type(CSDPlacementInfo[column]) == np.datetime64 or (type(CSDPlacementInfo[column]) == str and (column == "E" or column == "F")):
                    CSDPlacementInfo[column] = pd.to_datetime(str(CSDPlacementInfo[column])).strftime("%m/%d/%Y")
                if CSDPlacementInfo[column] != DCMPlacementInfo[column]:
                    rowColumn = "{column}{indexOfPlacement}".format(column=column,indexOfPlacement=indexOfPlacement)
                    ChangesArray.append({"column":rowColumn,"data":DCMPlacementInfo[column],"format":yellow})
                print(column, CSDPlacementInfo[column])
                print(column, DCMPlacementInfo[column])
    if placementsToAdd:
        #RowNum accounts for the fact that the Dataframe is 0-indexed, and the Headers are removed. 
        rowNum = len(sheet) + 2 
        for placement in placementsToAdd:
            currentPlacement = PlacementUtils.getPlacement(Api, placement)
            if checkPlacementEndDate(currentPlacement["pricingSchedule"]["endDate"]):
                continue
            DCMPlacementInfo = {"A":CampaignName,"B":PlacementUtils.getAndFormatSite(Api,currentPlacement),"C":placement,"D":currentPlacement["name"], "E":UtilUtils.formatPlacementDate(currentPlacement["pricingSchedule"]["startDate"]), "F":UtilUtils.formatPlacementDate(currentPlacement["pricingSchedule"]["endDate"]),"G":currentPlacement["compatibility"].capitalize(), "H":determineDimensions(currentPlacement), "I":isEvidon(currentPlacement["name"])}
            for column in DCMPlacementInfo:
                rowColumn = "{column}{indexOfPlacement}".format(column=column,indexOfPlacement=rowNum)
                ChangesArray.append({"column":rowColumn,"data":DCMPlacementInfo[column],"format":yellow})
            rowNum += 1
    # if placementsToRemove:
    #     for placement in placementsToRemove:
    #         #the two functions in the same way as the RowNum in the previous "if" statement
    #         indexOfPlacement = sheet[sheet.Id == placement].index[0] + 2
    #         CSDPlacement = sheet[sheet.Id == placement]
    #         CSDPlacementInfo = {"A":CSDPlacement["Campaign"].values[0],"B":CSDPlacement["Site"].values[0],"C":CSDPlacement["Id"].values[0],"D":CSDPlacement["Name"].values[0], "E":CSDPlacement["Start Date"].values[0], "F":CSDPlacement["End Date"].values[0],"G":CSDPlacement["Compatibility"].values[0], "H":CSDPlacement["Dimensions"].values[0]}
    #         for column in CSDPlacementInfo:
    #             rowColumn = "{column}{indexOfPlacement}".format(column=column,indexOfPlacement=indexOfPlacement)
    #             ChangesArray.append({"column":rowColumn,"data":CSDPlacementInfo[column],"format":red})
           


    return sheet


for file in fileList:
    print(file)
    excel = pd.read_excel(file, sheet_name=None)
    writer = pd.ExcelWriter('Merged_%s' % (file),engine='xlsxwriter')
    workbook = writer.book
    headerBlue =  workbook.add_format({'bg_color': '#0AADE9'})
    yellow = workbook.add_format({'bg_color': '#ffff00'})
    red = workbook.add_format({'bg_color': '#ff0000'})
    white = workbook.add_format({'bg_color': '#ffffff'})
    headerObject = {"A1":"Campaign", "B1":"Site", "C1":"Id", "D1":"Name","E1":"Start Date","F1":"End Date","G1":"Compatibility","H1":"Dimensions","I1":"Evidon","J1":"Creative Rotation","K1":"Creative File 1","L1":"Creative File 2","M1":"Creative File 3","N1":"Creative File 4","O1":"Creative File 5"}
    urlObject = {'A1':"Creative File", "B1":"Creative URL"}

    try:
        CampaignName = excel["TPS Placements"].iloc[0]["Campaign"]
    except:
        CampaignName = excel["SS Placements"].iloc[0]["Campaign"]
    for code in LMA:
        if code in CampaignName:
            LMAOverride = True
    try:
        RemovedPlacements = excel["Ended Placements"]
    except:
        pass

    listValues = {"searchString":CampaignName, "archived":False}
    campaign = CampaignUtils.getCampaignByName(Api, listValues)
    listValules = {"campaignIds":campaign["id"]}
    placementList = [x for x in PlacementUtils.listPlacement(Api, listValules) if x["archived"] == False ] 
    TPSPlacements = [x for x in placementList if "_TPS_" in x["name"] or "»TP»" in x["name"]]
    SSPlacements = [x for x in placementList if "_SS_" in x["name"] or "»SS»" in x["name"]]
    if len(TPSPlacements) > 0:
        try:
            TPSsheet = updateSheet(excel["TPS Placements"], TPSPlacements)
        except:
            excel["TPS Placements"] = pd.DataFrame(columns=["Campaign", "Site", "Id", "Name", "Start Date", "End Date", "Compatibility", "Dimensions", "Evidon", "Creative Rotation", "Creative File 1", "Creative File 2", "Creative File 3", "Creative File 4", "Creative File 5"])
            TPSsheet = updateSheet(excel["TPS Placements"], TPSPlacements)
        excel["TPS Placements"] = TPSsheet
        TPSsheet.to_excel(writer, sheet_name="TPS Placements",index=False)
        TPSworksheet = writer.sheets['TPS Placements']
        for obj in headerObject:
            TPSworksheet.write(obj, headerObject[obj], headerBlue) 
        for obj in ChangesArray:
            TPSworksheet.write(obj["column"],obj["data"],obj["format"])
        ChangesArray = []

    if len(SSPlacements) > 0:
        try:
            excel["SS Placements"]
        except:
            columnHeaders = excel["TPS Placements"].columns.tolist()
            df = pd.DataFrame()
            [assignColumns(df,x) for x in columnHeaders]
            excel["SS Placements"] = df
        try:
            sheetObject = sliceContacts(excel["SS Placements"])
            SSsheet = updateSheet(sheetObject["sheet"], SSPlacements)
            if len(ChangesArray) > 0:
                ChangesArray.sort(key=lambda x: x["column"])
                contactIndex = int(re.search("\d+",ChangesArray[len(ChangesArray)-1]["column"]).group()) + 3
            else:
                contactIndex = len(SSsheet) + 3
            SSsheet = appendContacts(SSsheet, sheetObject["contacts"], contactIndex)
            siteObject = SSsheet["siteIndex"]
        except:
            SSsheet = {}
            SSsheet["sheet"] = updateSheet(excel["SS Placements"], SSPlacements)
            index =  len(SSPlacements) + 3 
            siteObject = [["A"+str(index),"Site"],["B"+str(index),"Contact"]]
        excel["SS Placements"] = SSsheet["sheet"]
        SSsheet["sheet"].to_excel(writer, sheet_name="SS Placements",index=False)
        SSworksheet = writer.sheets['SS Placements']
        for obj in headerObject:
            SSworksheet.write(obj, headerObject[obj], headerBlue)
        if siteObject:
            for obj in siteObject:
                fmt = white
                if obj[1] == "Site" or obj[1] == "Contact":
                    fmt = headerBlue
                SSworksheet.write(obj[0], obj[1], fmt)
        for obj in ChangesArray:
            SSworksheet.write(obj["column"],obj["data"],obj["format"])

    if len(RemovedPlacements) > 0:
        RemovedPlacements = RemovedPlacements[['Campaign', 'Site', 'Id', 'Name', 'Start Date', 'End Date', 'Compatibility', 'Dimensions', 'Creative Rotation', 'Creative File 1', 'Creative File 2', 'Creative File 3', 'Creative File 4', 'Creative File 5']]
        RemovedPlacements.to_excel(writer, sheet_name="Ended Placements",index=False)
        RemovedPlacementsheet = writer.sheets['Ended Placements']
        for obj in headerObject:
            RemovedPlacementsheet.write(obj, headerObject[obj], headerBlue)

    excel["URLs"].to_excel(writer, sheet_name="URLs",index=False)
    worksheet_URLs = writer.sheets['URLs']
    for obj in urlObject:
        worksheet_URLs.write(obj, urlObject[obj], headerBlue)

    writer.save()
    RemovedPlacements = pd.DataFrame()
    ChangesArray = []