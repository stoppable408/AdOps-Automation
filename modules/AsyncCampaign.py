from modules.TraffickingObject import TraffickingObject
from modules.Placements import Placement
from retrying import retry

class AsyncCampaign(TraffickingObject):
    
    # @retry(wait_exponential_multiplier=10, wait_exponential_max=100) 
    def __init__(self, searchString, eventLoop = None, session = None):
         super().__init__()
         if hasattr(self, "session"):
            session = self.session
         self.get_body(searchString, eventLoop, session)
         if eventLoop != None:
             self.eventLoop = eventLoop
        
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)     
    def getLandingPages(self):
        self.url = "https://www.googleapis.com/dfareporting/v.30/userprofiles/{profile_id}/campaigns/{campaignId}/landingPages".format(profile_id=self.profile_id,campaignId=self.body["id"])
        async def wait():
            async with self.session.get(self.url, headers=self.auth) as r:
                text = await r.text()
                if r.status == 200:
                    response = self.json.loads(text)
                    self.landingPages = response["landingPages"]
                else:
                    self.handleError(text)
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
        else:
            placementEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(placementEvent)
        return self
        
        
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)     
    def getPlacementList(self):
        self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/placements?campaignIds={campaignId}".format(profile_id=self.profile_id,campaignId=self.body["id"])
        async def wait():
            async with self.session.get(self.url, headers=self.auth) as r:
                text = await r.text()
                if r.status == 200:
                    response = self.json.loads(text)
                    placementList = [{"id":x["id"]} for x in response["placements"]]
#                    placementList = [Placement(x["id"], self.eventLoop, self.session) for x in placementList]
                    self.placements = placementList
                else:
                    self.handleError(text)
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
        else:
            placementEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(placementEvent)
        return self
        
        
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)           
    def getAllCampaigns(self):
        def get(nextPageToken=None):
            if nextPageToken is None:
                self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/campaigns?subaccountId=23262&archived=false&searchString=2018".format(profile_id=self.profile_id)
            else:
                self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/campaigns?pageToken={pageToken}".format(profile_id=self.profile_id,pageToken = nextPageToken)
            return self.session
        async def wait():
            async with get().get(self.url, headers=self.auth) as r:
                text = await r.text()
                if r.status == 200:
                    response = self.json.loads(text)
                    campaignList = response["campaigns"]
                    while "nextPageToken" in response:
                        async with get(response["nextPageToken"]).get(self.url, headers=self.auth) as resp:
                            newText = await resp.text()
                            if resp.status == 200:
                                response = self.json.loads(newText)
                                campaignList.extend(response["campaigns"])
                    self.allCampaigns = campaignList
                else:
                    self.handleError(text)
                    self.allCampaigns = []
                    
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
        else:
            placementEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(placementEvent)
        return self
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)           
    def getAllCreatives(self):
        def get(nextPageToken=None):
            if nextPageToken is None:
                self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/creatives?campaignId={campaign_id}".format(profile_id=self.profile_id,campaign_id=self.body["id"])
            else:
                self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/creatives?pageToken={pageToken}".format(profile_id=self.profile_id,pageToken = nextPageToken)
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
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)           
    def getAllLMA(self):
        def get(nextPageToken=None):
            if nextPageToken is None:
                self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/campaigns?searchString=*LM".format(profile_id=self.profile_id)
            else:
                self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/campaigns?pageToken={pageToken}".format(profile_id=self.profile_id,pageToken = nextPageToken)
            return self.session
        async def wait():
            async with get().get(self.url, headers=self.auth) as r:
                text = await r.text()
                if r.status == 200:
                    response = self.json.loads(text)
                    campaignList = response["campaigns"]
                    while "nextPageToken" in response:
                        async with get(response["nextPageToken"]).get(self.url, headers=self.auth) as resp:
                            newText = await resp.text()
                           
                            if resp.status == 200:
                                response = self.json.loads(newText)
                                campaignList.extend(response["campaigns"])
                    self.LMACampaigns = campaignList
                else:
                    self.handleError(text)
                    self.LMACampaigns = []
                    
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
        else:
            placementEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(placementEvent)
        return self
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)     
    def modifyVerification(self):
        self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/campaigns?id={campaign_id}".format(profile_id=self.profile_id, campaign_id=self.body['id'])
        requestBody = {"adBlockingConfiguration": {"enabled": True,"overrideClickThroughUrl": True,"clickThroughUrl": "https://smokeybear.com/en"}}
        async def wait():
            async with self.session.patch(self.url, headers=self.auth, data=self.json.dumps(requestBody)) as r:
                text = await r.text()
                if r.status == 200:
                    print("{0} updated successfully".format(self.body['name']))
                else:
                    print("{0} failed to update.".format(self.body['name']))
                    self.handleError(text)
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
#            self.eventLoop.close()
#            self.eventLoop = None
        else:
            changeLogEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(changeLogEvent)
        return self
   
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)
    def insertCreativeAssociation(self, creativeID):
        requestBody = {"kind": "dfareporting#campaignCreativeAssociation",
                      "creativeId": creativeID}
        campaignID = self.body["id"]
        self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{0}/campaigns/{1}/campaignCreativeAssociations".format(self.profile_id, campaignID)
        async def wait():
            async with self.session.post(self.url, headers=self.auth, data=self.json.dumps(requestBody)) as r:
                text = await r.text()
                if r.status == 200:
                    print("sucessfully associated {0} with the current Campaign".format(creativeID))
                else:
                    print("{0} failed to associate with the current Campaign.".format(creativeID))
                    self.handleError(text)
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
        else:
            changeLogEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(changeLogEvent)
        return self
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)
    def getCreativeAssociation(self):
        campaignID = self.body["id"]
        self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{0}/campaigns/{1}/campaignCreativeAssociations".format(self.profile_id, campaignID)
        async def wait():
            async with self.session.get(self.url, headers=self.auth) as r:
                text = await r.text()
                if r.status == 200:
                    associations = self.json.loads(text)["campaignCreativeAssociations"]
                    self.associations = ({x["creativeId"] for x in associations}) 
                else:
                    print("{0} failed to get creatives.".format(self.body['name']))
                    self.handleError(text)
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
#            self.eventLoop.close()
#            self.eventLoop = None
        else:
            changeLogEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(changeLogEvent)
        return self     
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)
    def getAds(self):
        self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/ads?campaignIds={campaignID}".format(profile_id=self.profile_id,campaignID=self.body["id"])
        async def wait():
            async with self.session.get(self.url, headers=self.auth) as r:
                text = await r.text()
                if r.status == 200:
                    response = self.json.loads(text)["ads"]
                    self.adList = response
                else:
                    self.handleError(text)
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
        else:
            adEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(adEvent)
        return self
        
    def __str__(self):
        return "campaigns"
        
    
        