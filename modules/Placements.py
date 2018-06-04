from modules.TraffickingObject import TraffickingObject
from retrying import retry

class Placement(TraffickingObject):
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100) 
    def __init__(self, searchString, eventLoop=None, session=None):
        super().__init__()
#        print("getting placement {0}".format(searchString))
        if hasattr(self, "session"):
            session = self.session
        self.get_body(searchString,eventLoop, session).correctDate()
        if eventLoop != None:
             self.eventLoop = eventLoop
        
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)     
    def getAdList(self):
        self.url = "https://www.googleapis.com/dfareporting/v2.8/userprofiles/{profile_id}/ads?placementIds={placementId}".format(profile_id=self.profile_id,placementId=self.body["id"])
        async def wait():
            async with self.session.get(self.url, headers=self.auth) as r:
                text = await r.text()
                if r.status == 200:
                    response = self.json.loads(text)["ads"]
                    self.ads = response
                else:
                    self.handleError(text)
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
            self.eventLoop.close()
            self.eventLoop = None
        else:
            adEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(adEvent)
        return self
        
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)     
    def pushStaticClickTracking(self):
        self.url = "https://www.googleapis.com/dfareporting/v2.8/userprofiles/{profile_id}/placements?id={placementId}".format(profile_id=self.profile_id,placementId=self.body["id"])
        payload = {"tagSetting":{"includeClickThroughUrls": True,}}
        payloadText = '"includeClickThroughUrls": true'
        async def wait():
            async with self.session.patch(self.url, headers=self.auth, data=self.json.dumps(payload)) as r:
                text = await r.text()
                if r.status == 200:
                    response = self.json.loads(text)
                    if payloadText in response:
                        print("{0} updated successfully".format(self.body['name']))
                else:
                    print("%s failed to update.".format(self.body['name']))
                    self.handleError(text)
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
        else:
            changeLogEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(changeLogEvent)
        return self
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)      
    def correctDate(self):
        async def wait():
            async with self.session.get(self.url, headers=self.auth) as r:
                text = await r.text()
                if r.status == 200:
                    placementGroup = self.json.loads(text)
                    self.body["pricingSchedule"]["startDate"] = placementGroup["startDate"]
                    self.body["pricingSchedule"]["endDate"] = placementGroup["endDate"]
                else:
                    self.handleError(text)
        
        try:
            self.body["placementGroupId"]
            self.url = "https://www.googleapis.com/dfareporting/v2.8/userprofiles/{profile_id}/placementGroups/{PGID}".format(profile_id=self.profile_id,PGID=self.body["placementGroupId"])
            if self.eventLoop == None:
                self.eventLoop = self.asyncio.get_event_loop()
                self.eventLoop.run_until_complete(wait())
                self.eventLoop.close()
                self.eventLoop = None
            else:
                adEvent = self.eventLoop.create_task(wait())
                self.eventLoop.run_until_complete(adEvent)
        except:
            pass
        return self
        
        
    def __str__(self):
        return "placements"