import requests
import json
import pandas    
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
    # sheetID = 4531808571287428, 5203750836037508, 5042188125005700, 8453697828087684, 8682121368758148
    sheetList =  [4531808571287428, 5203750836037508, 5042188125005700, 8453697828087684, 8682121368758148]
    for sheetID in sheetList:
        rowRequest = requests.get("https://api.smartsheet.com/2.0/sheets/{sheetID}?include=rows".format(sheetID=sheetID),headers={'Content-type': 'application/json', "Authorization": "Bearer rrxhdlod9326sjrb1hwqzj5prx"},data={"includeAll":True})
        rows = json.loads(rowRequest.text)["rows"]
        rows = [{"id":x["id"],"columnInfo":x["cells"]} for x in rows]
        for row in rows:
            testRequest = requests.get("https://api.smartsheet.com/2.0/sheets/{sheetID}/rows/{rowID}?include=discussions,comments,attachments,columns,columnType".format(sheetID=sheetID,rowID=row["id"]),headers={'Content-type': 'application/json', "Authorization": "Bearer rrxhdlod9326sjrb1hwqzj5prx"},data={"includeAdll":True})
            response = json.loads(testRequest.text)
            try:
                planName = response["cells"][0]["value"]
            except:
                planName = "No Plan Name"
            try:
                productCode = response["cells"][1]["value"]
            except:
                productCode = "No Product Code"
            try:
                mediaType = response["cells"][2]["value"]
            except:
                mediaType = "No Media Type"
            try:
                comments = getComments(sheetID,row["id"])
            except:
                comments = [("N/A", "N/A")]
            try:
                MAFamount = response["cells"][3]["value"]
            except:
                MAFamount = "0.0"
            for element in comments:
                arrayObject = {"sheetID":sheetID,"sheetName":json.loads(rowRequest.text)["name"],"rowID":row["id"],"rowNumber":response["rowNumber"],"LMAPlanName":planName,"productCode":productCode,"mediaType":mediaType,"approvedMFAAmount":MAFamount,"commentId":element[0],"commentText":element[1]}
                dfArray.append(arrayObject)    
            print(response["rowNumber"], productCode)
        df = pandas.DataFrame(dfArray)
        df = df[["sheetID","sheetName","rowID","rowNumber","LMAPlanName","productCode","mediaType","approvedMFAAmount","commentId","commentText"]]
        writer = pandas.ExcelWriter(str(sheetID)+'.xlsx',engine='xlsxwriter')
        workbook = writer.book
        df.to_excel(writer, sheet_name ="Info", index = False)
        worksheet =  writer.sheets['Info']
        writer.save()

testCSD()