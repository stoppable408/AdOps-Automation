from v3modules import DCMAPI, ReportUtils
import requests
import shutil
import urllib
import pandas as pd
import re
import json
import googleapiclient.http as http
Api = DCMAPI.DCMAPI()
reportId = 59304806
report = ReportUtils.getReportFiles(Api, reportId) 
requestURL = report["urls"]["apiUrl"]
bearer = {"Authorization": "Bearer {token}".format(token=re.sub("OAuth ","",Api.auth["Authorization"]))}
p = requests.get(requestURL,allow_redirects=True, headers=bearer)
p = requests.get(p.url, verify=True,stream=True)
p.raw.decode_content = True
with open("{fileName}.csv".format(fileName=report['fileName']), 'wb') as f:
    shutil.copyfileobj(p.raw, f)
# response = pd.read_csv("{fileName}.xlsx".format(fileName=report['fileName']), engine="c")
header_flag = False
for index,chunk in enumerate(pd.read_csv("{fileName}.csv".format(fileName=report['fileName']), engine='python',iterator=True, chunksize=1024, header=None, names=list(range(100)))):
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
# response = pd.read_excel("Test_Sequencing.xlsx")

# downloader = http.MediaIoBaseDownload("test.xlsx", p)

# print(response.iloc/)
test = 0