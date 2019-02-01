from v3modules.DCMAPI import DCMAPI
import pandas as pd

def printResult(array, header, fileName):
    df = pd.DataFrame(data=array)
    headerArray = list(header.values())      
    df = df[headerArray]
    writer = pd.ExcelWriter('{name} Report.xlsx'.format(name=fileName),engine='xlsxwriter')
    workbook = writer.book
    df.to_excel(writer, sheet_name ="Info", index = False)
    worksheet =  writer.sheets['Info']
    writer.save()
    # from modules import send_mail
    # import os
    # directories = os.listdir()
    # reports = [x for x in directories if "Placement" in x]
    # for report in reports:
    #     send_mail.send_email(report, title="LMA SS Placements",recipients=["Lennon.Turner@amnetgroup.com","Kristine.Gillette@carat.com","Holly.Champoux@carat.com","Ali.Ciaffone@carat.com"])
def reportList():
    reportList = {
        "US_GMC_CustomEventData":59286195,
        "US_Buick_CustomEventData":59304806,
        "US_Chevrolet_CustomEventData": 59282491,
        "US_Cadillac_CustomEventData": 59271489
    }
    return reportList
def getReport(Api, reportId):
    report = Api.generateRequestUrl("reports",objectId=reportId).get().response
    return report

def getReportFiles(Api, reportId):
    listValues = {"sortField":"LAST_MODIFIED_TIME"}
    report = Api.generateRequestUrl("reports",objectId=reportId, listValues=listValues, secondaryObjectType="files").get().response
    return report["items"][0]

def sliceHeaders(fileName):
    header_flag = False
    for index,chunk in enumerate(pd.read_csv(fileName+".csv", engine='python',iterator=True, chunksize=1024, header=None, names=list(range(100)))):
        if len(chunk) > 0:
            chunk.fillna('',inplace=True)
            if index == 0 or header_flag == False:
                for i,row in chunk.iterrows():
                    if 'Report Fields' in str(row[0]):
                        cols = chunk.iloc[i+1]
                        chunk.drop(chunk.index[:i+2],inplace=True)
                        if len(chunk) ==0:
                            pass
                        header_flag = True
                        break
            chunk.columns = cols
            del chunk['']
            if chunk.iloc[-1][0] == 'Grand Total:':
                chunk.drop(chunk.index[-1],inplace=True)
    
