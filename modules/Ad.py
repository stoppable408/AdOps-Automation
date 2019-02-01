from modules.TraffickingObject import TraffickingObject
from retrying import retry

class Ad(TraffickingObject):
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100) 
    def __init__(self, searchString, eventLoop=None, session=None):
        super().__init__()
        if hasattr(self, "session"):
            session = self.session
        self.get_body(searchString,eventLoop, session)
        if eventLoop != None:
             self.eventLoop = eventLoop
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100) 
    def insertPlacement(self, payload, placementObject, campaignID):
        async def wait(payload, placementObject):
            async with self.session.patch(self.url, headers=self.auth, data=self.json.dumps(payload)) as r:
                text = await r.text()
                if r.status == 200:
                    response = self.json.loads(text)['placementAssignments']
                    if placementObject in response:
                        print("{0} updated successfully into placement association".format(self.body['name']))
                    else:
                        print("%s failed to update, but returned a status of 200. Please check the data JSON you're sending in the request".format(self.body['name']))
                else:
                    print("%s failed to update.".format(self.body['name']))
                    self.handleError(text)
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait(payload, placementObject))
        else:
            changeLogEvent = self.eventLoop.create_task(wait(payload, placementObject))
            self.eventLoop.run_until_complete(changeLogEvent)
        return self
        
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100) 
    def insertAd(self):
        async def wait():
            async with self.session.post(self.url, headers=self.auth, data=self.json.dumps(self.copy)) as r:
                text = await r.text()
                if r.status == 200:
                    response = self.json.loads(text)
                    response['placementAssignments'] = []
                    self.copy = response
                    print("{0} inserted successfully".format(self.body['name']))
                else:
#                    print(self.copy)
                    print("{0} failed to insert ad.".format(self.body['name']))
                    self.handleError(text)
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
        else:
            changeLogEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(changeLogEvent)
        return self
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100) 
    def activateAd(self):
        payload = {"active":True}
        self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/ads?id={adId}".format(profile_id=self.profile_id,adId=self.body["id"])
        async def wait():
            async with self.session.patch(self.url, headers=self.auth, data=self.json.dumps(payload)) as r:
                text = await r.text()
                if r.status == 200:
                    print("{0} activated successfully".format(self.body['name']))
                else:
                    print("{0} failed to activate ad.".format(self.body['name']))
                    self.handleError(text)
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
        else:
            changeLogEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(changeLogEvent)
        return self
        

    @retry(wait_exponential_multiplier=10, wait_exponential_max=100) 
    def getCreatives(self):
        creativeList = []
        for creative in self.body["creativeRotation"]["creativeAssignments"]:
            currentCreative = creative['creativeId']
            creativeList.append(currentCreative)
        return creativeList
        
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100) 
    def copy(self, campaignID):
        from modules.AsyncCampaign import AsyncCampaign
        from datetime import datetime, timedelta
        ad = self.body
        startTime = (datetime.now() + timedelta(days=1)).isoformat() + "Z"
        adCopy = {"name": ad['name'],"campaignId":campaignID, 'endTime': ad["endTime"], "startTime": startTime, 'type':  ad["type"],  'kind': ad['kind'], 'creativeRotation': ad['creativeRotation'], "deliverySchedule":ad["deliverySchedule"], 'sslRequired': ad['sslRequired'], 'sslCompliant':ad['sslCompliant'], 'clickThroughUrlSuffixProperties': ad['clickThroughUrlSuffixProperties'], "placementAssignments":[], "active":False} 
        creativeList = self.getCreatives()
        campaignObject = AsyncCampaign(campaignID).getCreativeAssociation()
        creativeAssociations = campaignObject.associations
        for element in creativeList:
            if element not in creativeAssociations:
                print("creative with number {0} not found. Inserting into Campaign".format(element))
                campaignObject.insertCreativeAssociation(element)
        self.copy = adCopy
        return self
    def __str__(self):
        return "ads"