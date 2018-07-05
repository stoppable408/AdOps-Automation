from modules.TraffickingObject import TraffickingObject
from retrying import retry

class Placement(TraffickingObject):
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100) 
    def __init__(self, searchString, eventLoop=None, session=None):
        super().__init__()
#        print("getting placement {0}".format(searchString))
        if hasattr(self, "session"):
            session = self.session
        if eventLoop != None:
             self.eventLoop = eventLoop
        self.get_body(searchString,eventLoop, session).correctDate()        
    
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
                    print("{0} failed to update.".format(self.body['name']))
                    self.handleError(text)
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
        else:
            changeLogEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(changeLogEvent)
        return self

    def correctDate(self):
        async def wait():
            async with self.session.get(self.url, headers=self.auth) as r:
                text = await r.text()
                if r.status == 200:
                    
                    placementGroup = self.json.loads(text)
                    self.body["pricingSchedule"]["startDate"] = placementGroup["pricingSchedule"]["startDate"]
                    self.body["pricingSchedule"]["endDate"] = placementGroup["pricingSchedule"]["endDate"]
                else:
                    self.handleError(text)
        
        try:
            PGID = self.body["placementGroupId"]
            self.url = "https://www.googleapis.com/dfareporting/v2.8/userprofiles/{profile_id}/placementGroups/{PGID}".format(profile_id=self.profile_id,PGID=PGID)
            if self.eventLoop == None:
                self.eventLoop = self.asyncio.get_event_loop()
                self.eventLoop.run_until_complete(wait())
                self.eventLoop.close()
                self.eventLoop = None
            else:
                adEvent = self.eventLoop.create_task(wait())
                self.eventLoop.run_until_complete(adEvent)
        except Exception as e:
            print(e)
            print("placementGroup failed for {ID}".format(ID=self.body["id"]))
        return self
    
    def listByCampaign(self, campaignID,separateByDimension=None):
        self.url = "https://www.googleapis.com/dfareporting/v3.0/userprofiles/{profileId}/placements?campaignId={campaignID}".format(profileId=self.profile_id,campaignID=str(campaignID))
        async def wait():
            async with self.session.get(self.url, headers=self.auth) as r:
                text = await r.text()
                if r.status == 200:
                    if separateByDimension != None:
                        response = [x for x in self.json.loads(text)["placements"] if separateByDimension in x["name"]]
                    else:
                        response = self.json.loads(text)["placements"]
                        
                    self.placementList = response
                else:
                    self.handleError(text)
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
            self.eventLoop.close()
            self.eventLoop = None
        else:
            placementEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(placementEvent)
        return self
        
    def isTrafficked(self):
        import datetime
        from modules.Ad import Ad
        from modules.Creative import Creative
        currentMonth = datetime.datetime.now().strftime("%B").lower()
        currentDate = datetime.datetime.now()
        def formatDateTime(datetimeString):
            import datetime
            date = datetimeString.split('T')[0]
            time = datetimeString.split('T')[1]
            year = int(date.split('-')[0])
            month = int(date.split('-')[1])
            day = int(date.split('-')[2])
            date = datetime.date(year,month,day)
            date = date.strftime("%m/%d/%y")
            hour = int(time.split(':')[0])
            minute = int(time.split(':')[1])
            time = datetime.time(hour,minute)
            time = time.strftime("%I:%M %p")
            return (date + " " +  time)
        def checkDate(dateString):
            try:
                date = datetime.datetime.strptime(dateString, "%Y-%m-%dT%H:%M:%S.000Z") > currentDate
            except:
                date = datetime.datetime.strptime(dateString, "%Y-%m-%dT%H:%M:%S.999Z") > currentDate
            return date
        def checkSession(session, initialSession):
            if initialSession != session:
                return session
            else:
                return initialSession
        initialSession = self.session
        initialEventLoop = self.eventLoop
        self.getAdList()
        self.testAds = self.ads
        response = [x for x in self.ads if "Brand-neutral" not in x['name'] and "TRACKING" not in x["name"] and x["active"] == True and "AD_SERVING_DEFAULT_AD" not in x["type"] and checkDate(x["endTime"])]
        self.response = response
        self.ads = [{"id":x["id"]} for x in response]
        if not self.ads:
            self.trafficked = False
            self.creativeName = "Not Trafficked"
            self.creativeDate = "Not Trafficked"
            self.adStart = "Not Trafficked"
            self.adEnd= "Not Trafficked"
            return self
        for adBody in self.ads:
            ad = Ad(adBody["id"],initialEventLoop, initialSession)
            initialSession = checkSession(ad.session, initialSession)
            try:
                creativeAssignments = ad.body["creativeRotation"]["creativeAssignments"]
            except:
                continue
            for creative in creativeAssignments:
                creativeID = creative["creativeId"]
                creativeElement = Creative(creativeID,initialEventLoop, initialSession)
                initialSession = checkSession(creativeElement.session, initialSession)
                creativeName = creativeElement.body["name"]

                if currentMonth in creativeName.lower():
                    self.trafficked = True
                    self.creativeName = creativeName
                    self.adStart = formatDateTime(ad.body["startTime"])
                    self.adEnd= formatDateTime(ad.body["endTime"])
                    timestamp = int(creativeElement.body["lastModifiedInfo"]["time"]) / 1e3
                    self.creativeDate = datetime.datetime.fromtimestamp(timestamp).strftime('%m/%d/%y %I:%M %p')
                    return self
                else:
                    self.trafficked = False
                    self.creativeName = creativeName
                    self.adStart = formatDateTime(ad.body["startTime"])
                    self.adEnd= formatDateTime(ad.body["endTime"])
                    timestamp = int(creativeElement.body["lastModifiedInfo"]["time"]) / 1e3
                    self.creativeDate = datetime.datetime.fromtimestamp(timestamp).strftime('%m/%d/%y %I:%M %p')

        return self
    def __str__(self):
        return "placements"