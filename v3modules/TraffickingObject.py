
from retrying import retry

#Class that imports the requests and json modules for easier access. this will be a parent class for all trafficking objects
#This was changed to a non-abstract class because I ran into many use cases where I needed an object but didn't need it to be a specific trafficking object
#This class will contain the generic "getbody" method that all its children will use. but also other non-specific functions, such as "Get all Campaigns"
token = None
eventLoop = None
class TraffickingObject():
    import json
    import requests
    def __init__(self):
        if token  == None:
            print("getting token")
            self.getToken()
        else:
            self.profile_id, self.auth = token[0],token[1]
            
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)   
    def getToken(self):
        global token
        import os
        import httplib2
        from oauth2client import file as oauthFile
      
        try:
            if "lturner01" in os.getcwd():
                storage = oauthFile.Storage(os.getcwd() + "/modules/dfareporting.dat")
            else:
                storage = oauthFile.Storage("/home/techops/AdOps_Automation/modules/dfareporting.dat")
            credentials = storage.get()
            credentials.refresh(httplib2.Http())
            self.profile_id, self.auth = 2532624 , {'Content-type': 'application/json', "Authorization": "OAuth %s" % credentials.access_token}
            token = (self.profile_id, self.auth)
        except:
            print("dfa file not found")
            
    def handleError(self, response):
        error = self.json.loads(response)['error']['errors'][0]['message']
        print(error)
        if "Invalid" in error:
            print("getting new credentials")
            self.getToken()
        else:
            print(response)
        raise Exception("Throw to retry")

    def get_body(self, searchString):
        searchString = str(searchString).strip()
        className = str(self)
        self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/{className}?searchString={searchString}".format(className=className,profile_id=self.profile_id,searchString=searchString)
        r = self.requests.get(self.url, headers=self.auth)
        text = r.text
        if r.status_code == 200:
            try:
                print("this is a :", className)
                self.body = self.json.loads(text)[className][0]
            except:
                self.handleError(text)
        else:
            print(r.text)
            self.handleError(text)
        return self

    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)           
    def getAllCampaigns(self):
        def get(nextPageToken=None):
            if nextPageToken is None:
                self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/campaigns?subaccountId=23262&archived=false&searchString=2018".format(profile_id=self.profile_id)
            else:
                self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/campaigns?pageToken={pageToken}".format(profile_id=self.profile_id,pageToken = nextPageToken)
            return self.requests
        r = get().get(self.url, headers=self.auth)
        text = r.text
        if r.status_code == 200:
            response = self.json.loads(text)
            campaignList = response["campaigns"]
            while "nextPageToken" in response:
                resp = get(response["nextPageToken"]).get(self.url, headers=self.auth)
                newText = resp.text
                if resp.status_code == 200:
                    print("new set")
                    response = self.json.loads(newText)
                    campaignList.extend(response["campaigns"])
            self.allCampaigns = campaignList
        else:
            self.handleError(text)
            self.allCampaigns = []
        return self

    def getAdsByAdvertiser(self,advertiserID):
        def get(nextPageToken=None):
            import urllib
            import re
            if "pageToken" in self.url:
                pattern = re.compile("&pageToken(.*)")
                self.url = re.sub(pattern,"",self.url)
            nextPageToken = urllib.parse.quote(nextPageToken)
            self.url = self.url + "&pageToken={pageToken}".format(pageToken=nextPageToken)
            return self
        self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/ads?advertiserId={advertiserID}&active=True".format(profile_id=self.profile_id,advertiserID=advertiserID)
        r = self.requests.get(self.url, headers=self.auth)
        text = r.text
        tokenSet = set()
        if r.status_code == 200:
            response = self.json.loads(text)
            ads = response["ads"]
            while "nextPageToken" in response:
                print(response["nextPageToken"])
                # print(tokenSet)
                print(len(ads))
                print(self.url)
                if response["nextPageToken"] in tokenSet:
                    break
                tokenSet.add(response["nextPageToken"])
                resp = get(response["nextPageToken"]).requests.get(self.url, headers=self.auth)
                newText = resp.text
                self.test = resp
                if resp.status_code == 200:
                    response = self.json.loads(newText)
                    ads.extend(response["ads"])
                else:
                    print(newText)
                    break
                    self.handleError(text)
            self.ads = ads
            return self

    def getAllLandingPages(self):
        def get(nextPageToken=None):
            import urllib
            import re
            if "pageToken" in self.url:
                pattern = re.compile("pageToken(.*)")
                self.url = re.sub(pattern,"",self.url)
            nextPageToken = urllib.parse.quote(nextPageToken)
            self.url = self.url + "&pageToken={pageToken}".format(pageToken=nextPageToken)
            return self
        def getFinalList(landingPages):
            idSet = set()
            finalArray = []
            for element in landingPages:
                if element["id"] in idSet:
                    continue
                else:
                    idSet.add(element["id"])
                    finalArray.append(element)
            return finalArray
        self.url = 'https://www.googleapis.com/dfareporting/v3.1/userprofiles/2532624/advertiserLandingPages?advertiserIds=5288214&advertiserIds=5354228&advertiserIds=6015329&advertiserIds=4568611&advertiserIds=3876773&advertiserIds=6198719&advertiserIds=3876774&advertiserIds=3876777&advertiserIds=4569406&advertiserIds=4569405&advertiserIds=3876771&advertiserIds=5361629&advertiserIds=3876780&advertiserIds=4568613&advertiserIds=4635253&advertiserIds=3876782&advertiserIds=4496783&advertiserIds=4852937&advertiserIds=5724659&advertiserIds=4508180&advertiserIds=3876772&advertiserIds=5314814&advertiserIds=3876775&advertiserIds=5139395'
        #self.url = 'https://www.googleapis.com/dfareporting/v3.1/userprofiles/2532624/advertiserLandingPages?advertiserIds=5288214&advertiserIds=5354228&advertiserIds=6015329&advertiserIds=4568611&advertiserIds=3876773&advertiserIds=6198719&advertiserIds=3876774&advertiserIds=3876777&advertiserIds=4569406'
        r = self.requests.get(self.url,headers=self.auth)
        text = r.text
        tokenSet = set()
        if r.status_code == 200:
            response = self.json.loads(text)
            landingpages = response["landingPages"]
            while "nextPageToken" in response:
                if response["nextPageToken"] in tokenSet:
                    break
                tokenSet.add(response["nextPageToken"])
                resp = get(response["nextPageToken"]).requests.get(self.url, headers=self.auth)
                newText = resp.text
                self.test = resp
                if resp.status_code == 200:
                    response = self.json.loads(newText)
                    landingpages.extend(response["landingPages"])
                else:
                    break
                    self.handleError(text)
            self.landingPages =getFinalList(landingpages)
        else:
            self.handleError(text)
            self.landingPages = []
        return self

    def getAllCreatives(self):
        def get(nextPageToken=None):
            if nextPageToken is None:
                self.url = "https://www.googleapis.com/dfareporting/v2.8/userprofiles/{profile_id}/creatives?campaignId={campaign_id}".format(profile_id=self.profile_id,campaign_id=self.body["id"])
            else:
                self.url = "https://www.googleapis.com/dfareporting/v2.8/userprofiles/{profile_id}/creatives?pageToken={pageToken}".format(profile_id=self.profile_id,pageToken = nextPageToken)
            return self.session
        async def wait():
            async with get().get(self.url, headers=self.auth) as r:
                text = await r.text()
                if r.status == 200:
                    response = self.json.loads(text)
                    creativeList = response["creatives"]
                    while "nextPageToken" in response:
                        async with get(response["nextPageToken"]).get(self.url, headers=self.auth) as resp:
                            newText = await resp.text()
                            if resp.status == 200:
                                response = self.json.loads(newText)
                                creativeList.extend(response["creatives"])
                            else:
                                break
                    self.allCreatives = creativeList
                else:
                    self.handleError(text)
                    self.allCreatives = []
                    
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
        else:
            placementEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(placementEvent)
        return self