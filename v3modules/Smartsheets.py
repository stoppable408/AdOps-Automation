import requests
import json
import pandas

sheetList = [7134009567274884,965852414666628,8492559262607236,3382407173826436,1593364316481412]


def getCSD(sheetID, rowID):
    rowRequest = requests.get("https://api.smartsheet.com/2.0/sheets/{sheetID}/rows/{rowID}?include=discussions,attachments,columns,columnType".format(rowID=rowID,sheetID=sheetID),headers={'Content-type': 'application/json', "Authorization": "Bearer tgpok7w80kjb1hz6sl4t3e073w"})
    # rowRequest = requests.get("https://api.smartsheet.com/2.0/sheets/3382407173826436/rows/3033875265939332?include=discussions,attachments,columns,columnType".format(rowID=rowID,sheetID=sheetID),headers={'Content-type': 'application/json', "Authorization": "Bearer tgpok7w80kjb1hz6sl4t3e073w"})
    rowResponse = [x for x in json.loads(rowRequest.text)["discussions"] if "commentAttachments" in x]
    mustBreak = False
    for element in range(len(rowResponse)-1,-1,-1):
        for attachment in rowResponse[element]["commentAttachments"]:
            latestAttachment = attachment
            print(latestAttachment)
            if ".xlsx" in latestAttachment["name"]:
                latestAttachmentId = attachment["id"]
                mustBreak = True
                break
        if mustBreak == True:
            break
    print(latestAttachmentId)
    attachmentRequest = requests.get("https://api.smartsheet.com/2.0/sheets/{sheetID}/attachments/{latestAttachmentId}".format(latestAttachmentId=latestAttachmentId,sheetID=sheetID),headers={'Content-type': 'application/json', "Authorization": "Bearer tgpok7w80kjb1hz6sl4t3e073w"})
    attachmentUrl = json.loads(attachmentRequest.text)['url']
    CSD = pandas.read_excel(attachmentUrl)
    return CSD
    

# def completeCSDDict():
#     global csdDict
#     for sheet in sheetList:
#         print("reading {sheet}".format(sheet=sheet))
#         sheetRequest = requests.get("https://api.smartsheet.com/2.0/sheets/{sheet}".format(sheet=sheet),headers={'Content-type': 'application/json', "Authorization": "Bearer tgpok7w80kjb1hz6sl4t3e073w"})
#         sheetResponse = json.loads(sheetRequest.text)
#         rows = sheetResponse["rows"]
#         currentCampaignRow = None
#         for row in rows:
#             try:
#                 rowName = row["cells"][0]["displayValue"]   
#             except:
#                 continue
#             if "LMA" not in rowName:
#                 currentCampaignRow = rowName
#             if "SS" in currentCampaignRow or "Site Served" in currentCampaignRow:
#                 continue
#             if "LMA" in rowName:
#                 print("reading {rowname}".format(rowname=rowName))
#                 getCSD(row["id"],rowName,sheet)
            
#             if "Ended" in currentCampaignRow:
#                 break
#     return csdDict

def completeCSDDict():
    csdDict = {}
    for sheet in sheetList:
        print("reading {sheet}".format(sheet=sheet))
        sheetRequest = requests.get("https://api.smartsheet.com/2.0/sheets/{sheet}".format(sheet=sheet),headers={'Content-type': 'application/json', "Authorization": "Bearer tgpok7w80kjb1hz6sl4t3e073w"})
        sheetResponse = json.loads(sheetRequest.text)
        rows = sheetResponse["rows"]
        currentCampaignRow = None
        for row in rows:
            try:
                rowName = row["cells"][0]["displayValue"]
                
                rowId = row["id"]
            except:
                continue
            if "LMA" in rowName:
                print("reading {rowname}".format(rowname=rowName))
                csdDict[rowName] = [sheet,rowId]
                continue
            if "LMA" not in rowName:
                currentCampaignRow = rowName
            if "SS" in currentCampaignRow or "Site Served" in currentCampaignRow:
                continue

            
            if "Ended" in currentCampaignRow:
                break
    return csdDict
