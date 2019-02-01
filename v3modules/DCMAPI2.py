

class DCMAPI():
    
    def __init__(self):
        import requests
        import json
        self.requests = requests
        self.json = json
        self.getToken()

    #Function that gets the original token to be able to authorize DCM requests, also can be called to refresh token in case of invalid credentials
    def getToken(self):
        import os
        import httplib2
        from oauth2client import file as oauthFile
        try:
            reportingstorage = oauthFile.Storage(os.getcwd() + "\\v3modules\dfareporting.dat")
            traffickingstorage = oauthFile.Storage(os.getcwd() + "\\v3modules\dfatrafficking.dat")
            reportingcredentials = reportingstorage.get()
            traffickingcredentials = traffickingstorage.get()
            reportingcredentials.refresh(httplib2.Http())
            traffickingcredentials.refresh(httplib2.Http())
            self.profile_id, self.reportingauth, self.traffickingauth = 2532624 , {'Content-type': 'application/json', "Authorization": "OAuth %s" % reportingcredentials.access_token}, {'Content-type': 'application/json', "Authorization": "OAuth %s" % traffickingcredentials.access_token}
        except Exception as e:
            print(e)
            print("dfa file not found")

    #Function to generate a request URL for objects in DCM
    def generateRequestUrl(self, objectType,objectId=None,listValues=None,secondaryObjectType=None):
        if objectType == "reports":
            self.auth = self.reportingauth
        else:
            self.auth = self.traffickingauth
        def dictToString(listValues):
            emptyString = ""
            for value in listValues:
                emptyString += "{objectType}={value}&".format(objectType=value,value=listValues[value])
            finalString = emptyString[:-1]
            return finalString
        if secondaryObjectType != None:
            self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profileId}/{objectType}/{objectId}/{secondaryObjectType}".format(objectType=objectType,profileId=self.profile_id,objectId=objectId,secondaryObjectType=secondaryObjectType)
            return self
        if objectId == None and listValues == None:
            self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profileId}/{objectType}/".format(objectType=objectType,profileId=self.profile_id)
        elif objectId != None and listValues == None:
            self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profileId}/{objectType}/{objectId}".format(objectType=objectType,objectId=objectId,profileId=self.profile_id)
        else:
            parameters = dictToString(listValues)
            self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profileId}/{objectType}?{parameters}".format(objectType=objectType,parameters=parameters,profileId=self.profile_id)
        return self
            
    #Function to get one object from DCM
    def get(self):
        r = self.requests.get(self.url, headers=self.auth)
        response = self.json.loads(r.text)
        if r.status_code == 200:
            self.response = response
            return self
        else:
            errormessage = response["error"]["message"]
            if "Invalid" in errormessage:
                print(errormessage)
                print(self.url)
                print("getting new credentials")
                self.getToken()
                return self.get()
            else:
                print(errormessage)

    #function to create a new object in DCM
    def insert(self, body):
        r = self.requests.post(self.url, headers=self.auth, data=self.json.dumps(body))
        response = self.json.loads(r.text)
        if r.status_code == 200:
            print("successfully inserted {objectType}".format(objectType=response["kind"]))
            return self        # Finish function declaration when the need arises to insert. Don't quite know how to do it yet, and I haven't had an opportunity to insert something
        else:
            print("successfully inserted {objectType}".format(objectType=response["kind"]))        # Finish function declaration when the need arises to insert. Don't quite know how to do it yet, and I haven't had an opportunity to insert something


    #Function to get a list of objects, similar to the "get" function above, but with extra functionality for requests that have more than 1000 results
    def getlist(self, objectType,secondaryObjectType=None,objectId=None):
        nextPageSet = set()
        if secondaryObjectType != None:
            key = self.url.split("/")[-1]
        else:
            key = objectType
        def get(nextPageToken=None):
            if nextPageToken is not None:
                if secondaryObjectType == None:
                    self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/{objectType}?pageToken={pageToken}".format(profile_id=self.profile_id,pageToken = nextPageToken,objectType=objectType)
                else:
                    self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/{objectType}/{objectId}/{secondaryObjectType}?pageToken={pageToken}".format(profile_id=self.profile_id,pageToken = nextPageToken,objectType=objectType,objectId=objectId,secondaryObjectType=secondaryObjectType)
            return self.requests        
        r = get().get(self.url, headers=self.auth)
        
        response = self.json.loads(r.text)
        if r.status_code == 200:
            responseList = response[key]
            while "nextPageToken" in response:
                if response['nextPageToken'] in nextPageSet:
                    break
                nextPageSet.add(response['nextPageToken'])
                resp = get(response["nextPageToken"]).get(self.url, headers=self.auth)
                if resp.status_code == 200:
                    response = self.json.loads(resp.text)
                    responseList.extend(response[key])
            self.response = responseList
            return self
        else:
            errormessage = response["error"]["message"]
            if "Invalid" in errormessage:
 
                print("getting new credentials")
                self.getToken()
                return self.getlist(objectType,secondaryObjectType,objectId)
            else:
                print(errormessage)
    
    def patch(self, body):
        r = self.requests.patch(self.url, headers=self.auth, data=self.json.dumps(body))
        response = self.json.loads(r.text)
        if r.status_code == 200:
            print("{0} updated successfully".format(response['name']))
            return self
        else:
            try:
                print("{0} failed to update.".format(response['name']))
            except:
                print(response["error"]["message"])

    def post(self,body):
        r = self.requests.post(self.url, headers=self.auth, data=self.json.dumps(body))
        response = self.json.loads(r.text)
        if r.status_code == 200:
            print("{0} inserted successfully".format(response['name']))
            return self
        else:
            try:
                print("{0} failed to insert.".format(response['name']))
            except Exception as e:
                print(e)
                print("error reached.")


    def delete(self):
        r = self.requests.delete(self.url, headers=self.auth)
        if r.status_code == 200 or r.status_code == 204:
            print("item deleted successfully")
            return self
        else:
            try:
                print("item failed to delete.")

            except Exception as e:
                print("error reached.")