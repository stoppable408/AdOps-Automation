import requests
import json
import pandas
import operator 

sheetList = [348500224436100,2641359925471108,4094980869384068,2335581876316036,6066774585173892,7134009567274884,965852414666628,8492559262607236,3382407173826436,1593364316481412]


def getCSD(sheetID, rowID):
    rowRequest = requests.get("https://api.smartsheet.com/2.0/sheets/{sheetID}/rows/{rowID}?include=discussions,attachments,columns,columnType".format(rowID=rowID,sheetID=sheetID),headers={'Content-type': 'application/json', "Authorization": "Bearer tgpok7w80kjb1hz6sl4t3e073w"})
    # rowRequest = requests.get("https://api.smartsheet.com/2.0/sheets/7134009567274884/rows/813603498551172?include=discussions,attachments,columns,columnType".format(rowID=rowID,sheetID=sheetID),headers={'Content-type': 'application/json', "Authorization": "Bearer tgpok7w80kjb1hz6sl4t3e073w"})
    rowResponse = [x for x in json.loads(rowRequest.text)["discussions"] if "commentAttachments" in x]
    mustBreak = False
    rowResponse = sorted(rowResponse, key=lambda k: k["commentAttachments"][0]['createdAt'], reverse = True) 
    for element in range(0, len(rowResponse)):
        rowAttachments = rowResponse[element]["commentAttachments"]
        rowAttachments = sorted(rowAttachments, key=lambda k: k['createdAt'], reverse = True) 
        for attachment in rowAttachments:
            latestAttachment = attachment
            if ".xlsx" in latestAttachment["name"]:
                latestAttachmentId = attachment["id"]
                mustBreak = True
                break
        if mustBreak == True:
            break
    print(latestAttachment)
    attachmentRequest = requests.get("https://api.smartsheet.com/2.0/sheets/{sheetID}/attachments/{latestAttachmentId}".format(latestAttachmentId=latestAttachmentId,sheetID=sheetID),headers={'Content-type': 'application/json', "Authorization": "Bearer tgpok7w80kjb1hz6sl4t3e073w"})
    attachmentUrl = json.loads(attachmentRequest.text)['url']
    CSD = pandas.read_excel(attachmentUrl)
    return CSD
    
def testCSD():
    def getComments(sheetID, rowID):
        array = []
        commentRequest = requests.get("https://api.smartsheet.com/2.0/sheets/{sheetID}/rows/{rowID}/discussions?include=comments,attachments".format(sheetID=sheetID,rowID=rowID),headers={'Content-type': 'application/json', "Authorization": "Bearer rrxhdlod9326sjrb1hwqzj5prx"},data={"includeAdll":True})
        response = json.loads(commentRequest.text)
        if len(response["data"]) > 0:
            for comment in response["data"]:
                commentInfo = (comment["id"],comment["title"])
                array.append(commentInfo)
            return array
        return [("N/A", "N/A")]
    dfArray = []
    # sheetID = 5042188125005700
    sheetList =  [4531808571287428, 5203750836037508, 5042188125005700, 8453697828087684, 8682121368758148]
    for sheetID in sheetList:
        rowRequest = requests.get("https://api.smartsheet.com/2.0/sheets/{sheetID}?include=rows".format(sheetID=sheetID),headers={'Content-type': 'application/json', "Authorization": "Bearer rrxhdlod9326sjrb1hwqzj5prx"},data={"includeAll":True})
        rows = json.loads(rowRequest.text)["rows"]
        rows = [{"id":x["id"],"columnInfo":x["cells"]} for x in rows]
        for row in rows:
            testRequest = requests.get("https://api.smartsheet.com/2.0/sheets/{sheetID}/rows/{rowID}?include=discussions,comments,attachments,columns,columnType".format(sheetID=sheetID,rowID=row["id"]),headers={'Content-type': 'application/json', "Authorization": "Bearer rrxhdlod9326sjrb1hwqzj5prx"},data={"includeAdll":True})
            response = json.loads(testRequest.text)
            planName = response["cells"][0]["value"]
            productCode = response["cells"][1]["value"]
            mediaType = response["cells"][2]["value"]
            comments = getComments(sheetID,row["id"])
            try:
                MAFamount = response["cells"][3]["value"]
            except:
                MAFamount = "0.0"
            for element in comments:
                arrayObject = {"sheetID":sheetID,"sheetName":json.loads(rowRequest.text)["name"],"rowID":row["id"],"rowNumber":response["rowNumber"],"LMAPlanName":planName,"productCode":productCode,"mediaType":mediaType,"approvedMFAAmount":MAFamount,"commentId":element[0],"commentText":element[1]}
                dfArray.append(arrayObject)    
            print(response["rowNumber"], productCode)
    print(dfArray)
    df = pandas.DataFrame(dfArray)
    df = df[["sheetID","sheetName","rowID","rowNumber","LMAPlanName","productCode","mediaType","approvedMFAAmount","commentId","commentText"]]
    writer = pandas.ExcelWriter('Report.xlsx',engine='xlsxwriter')
    workbook = writer.book
    df.to_excel(writer, sheet_name ="Info", index = False)
    worksheet =  writer.sheets['Info']
    writer.save()


def getSiteContacts():
    rowRequest = requests.get("https://api.smartsheet.com/2.0/sheets/2467787949008772?include=rows",headers={'Content-type': 'application/json', "Authorization": "Bearer rrxhdlod9326sjrb1hwqzj5prx"},data={"includeAll":True})
    rows = json.loads(rowRequest.text)["rows"]
    contactObject = {}
    for row in rows:
        emailArray = []
        for cell in range(0,len(row["cells"])):
            if cell == 0:
                try:
                    siteId = row["cells"][cell]["displayValue"]
                except:
                    siteId = None
                    break
            elif cell != 0:
                try:
                    emailArray.append(row["cells"][cell]["displayValue"])
                except:
                    continue
        
        if siteId != None:
            contactObject[siteId] = [x for x in emailArray if "@" in x]   
    return contactObject

def getLMASiteContacts():
    rowRequest = requests.get("https://api.smartsheet.com/2.0/sheets/8889980606015364?include=rows",headers={'Content-type': 'application/json', "Authorization": "Bearer rrxhdlod9326sjrb1hwqzj5prx"},data={"includeAll":True})
    rows = json.loads(rowRequest.text)["rows"]
    contactObject = {}
    for row in rows:
        emailArray = []
        for cell in range(0,len(row["cells"])):
            if cell == 0:
                try:
                    siteId = row["cells"][cell]["displayValue"]
                except:
                    siteId = None
                    break
            elif cell != 0:
                try:
                    emailArray.append(row["cells"][cell]["displayValue"])
                except:
                    continue
        if siteId != None:
            contactObject[siteId] = [x for x in emailArray if "@" in x]   
    return contactObject
    
            
# testCSD()
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

def completeNonLMACSDDict():
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