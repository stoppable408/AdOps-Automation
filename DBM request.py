import requests
import os
from oauth2client.client import flow_from_clientsecrets
from oauth2client import file as oauthFile
import httplib2
import json
import urllib
import csv
import shutil
import threading

currentDirectory = os.getcwd()
# flow = flow_from_clientsecrets(currentDirectory+ '\\client_secrets.json',
#                                scope='https://www.googleapis.com/auth/doubleclickbidmanager',
#                                redirect_uri='urn:ietf:wg:oauth:2.0:oob')
# Visit the below auth_uri and sign in to get the authorization code
# auth_uri = flow.step1_get_authorize_url()
# Example Authorization code
# authorization = "4/AAAdaVg9dWHrQosCq0HitnOI-FVXrD8mHxS0Cgls3v3tnS7UTBIqZ-I"
# credentials = flow.step2_exchange(authorization)
# store credentials in a file object
# storage = Storage('dbmreporting.dat')
# storage.put(credentials)
# auth = {'Content-type': 'application/json', "Authorization": "OAuth %s" % credentials.access_token}
#import httplib2
#credentials.refresh(httplib2.Http())
#r = requests.get(url, headers=auth)
test =0 
storage = oauthFile.Storage(os.getcwd() + "\\dbmreporting.dat")
credentials = storage.get()
credentials.refresh(httplib2.Http())
auth = {'Content-type': 'application/json', "Authorization": "OAuth %s" % credentials.access_token}
queries = [
    {"queryID":"136369641","name":"AMNET_Chevrolet_InMarket_Today","today":True},
    {"queryID":"136189668","name":"AMNET_Chevrolet_InMarket_14Days","today":False},
    {"queryID":"136166179","name":"AMNET_Buick_14Days","today":False},
    {"queryID":"136369299","name":"AMNET_Buick_Today","today":True}
]
def analyzeTodayReport(report):
    test = 1
    pass
for report in queries:
    if report["today"] == True:
        thread = threading.Thread(name=report["name"],target=analyzeTodayReport,args=(report,))
        thread.start()

url = "https://www.googleapis.com/doubleclickbidmanager/v1/query/136166179"

r = requests.get(url, headers=auth)
csvpath = json.loads(r.text)["metadata"]["googleCloudStoragePathForLatestReport"]
print("getting response")
p = requests.get(csvpath, verify=False,stream=True)
print("response received, writiting to file")
p.raw.decode_content = True
with open("file1.csv", 'wb') as f:
            shutil.copyfileobj(p.raw, f)
print("file copied")



test = 0