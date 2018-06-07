# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 13:51:33 2018

@author: lturner01
"""

from modules.TraffickingObject import TraffickingObject
from retrying import retry

class ChangeLogs(TraffickingObject):
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=10) 
    def __init__(self):
        super().__init__()
        self.eventLoop = None
        
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)     
    def getNewPlacements(self, changeTime):
        def get(nextPageToken=None):
            if nextPageToken is None:
                self.url = "https://www.googleapis.com/dfareporting/v2.8/userprofiles/{profile_id}/changeLogs?action=action_create&objectType=OBJECT_PLACEMENT&minChangeTime={changeTime}".format(profile_id=self.profile_id, changeTime=changeTime)
            else:
                self.url = "https://www.googleapis.com/dfareporting/v2.8/userprofiles/{profile_id}/changeLogs?action=action_create&objectType=OBJECT_PLACEMENT&minChangeTime={changeTime}&pageToken={pageToken}".format(profile_id=self.profile_id, changeTime=changeTime,pageToken=nextPageToken)
            return self.session
        async def wait():
            async with get().get(self.url, headers=self.auth) as r:
                text = await r.text()
                if r.status == 200:
                    response = self.json.loads(text)
                    changeLog = response["changeLogs"]
                    while "nextPageToken" in response:
                        async with get(response["nextPageToken"]).get(self.url, headers=self.auth) as resp:
                            newText = await resp.text()
                            if resp.status == 200:
                                response = self.json.loads(newText)
                                changeLog.extend(response["changeLogs"])
                            if resp.status == 500:
                                break
                    changeLog = [x for x in changeLog if "subaccountId" in x.keys()]
                    changeLog = [x["objectId"] for x in changeLog if x['subaccountId'] == '23262' and "_SS_" in x['newValue']] 
                    self.logs = changeLog   
                    print("%s total number of placements found created after %s" % (len(changeLog), changeTime))
                else:
                    self.handleError(text)
                    self.logs = []
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
        else:
            changeLogEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(changeLogEvent)
        return self
        
    def verifyCampaigns(self):
        def printResult(campaignArray):
            import pandas as pd
            from modules import send_mail
            df = pd.DataFrame(data=campaignArray)
            
            writer = pd.ExcelWriter('Campaign.xlsx',engine='xlsxwriter')
            workbook = writer.book
            headerObject = {"A1":"Campaign Name"}
            format1 =  workbook.add_format({'bg_color': '#0AADE9'})
            
            df.to_excel(writer, sheet_name ="Campaigns", index = False)
            worksheet =  writer.sheets['Campaigns']
            for obj in headerObject:
                worksheet.write(obj, headerObject[obj], format1) 
            print("Done!")    
            writer.save()
            import os
            directories = os.listdir()
            reports = [x for x in directories if "Campaign.xlsx" in x]
            for report in reports:
                send_mail.send_email(report, title="Verified Campaigns",recipients=["Lennon.Turner@amnetgroup.com","Kristine.Gillette@carat.com","Mackenzie.VanSteenkiste@carat.com","Holly.Champoux@carat.com"])
        if len(self.logs) > 0:
            campaignArray = []
            from modules.AsyncCampaign import AsyncCampaign
            for campaign in self.logs:
                currentCampaign = AsyncCampaign(campaign, self.eventLoop, self.session).modifyVerification()
                campaignArray.append(currentCampaign.body["name"])
            printResult(campaignArray)
        return self
        
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)
    def getNewCampaigns(self, changeTime):
        def get(nextPageToken=None):
            if nextPageToken is None:
                self.url = "https://www.googleapis.com/dfareporting/v2.8/userprofiles/{profile_id}/changeLogs?action=action_create&objectType=OBJECT_CAMPAIGN&minChangeTime={changeTime}".format(profile_id=self.profile_id, changeTime=changeTime)
            else:
                self.url = "https://www.googleapis.com/dfareporting/v2.8/userprofiles/{profile_id}/changeLogs?action=action_create&objectType=OBJECT_CAMPAIGN&minChangeTime={changeTime}&pageToken={pageToken}".format(profile_id=self.profile_id, changeTime=changeTime,pageToken=nextPageToken)
            return self.session
        
        async def wait():
            async with get().get(self.url, headers=self.auth) as r:
                text = await r.text()
                if r.status == 200:
                    response = self.json.loads(text)
                    changeLog = response["changeLogs"]
                    while "nextPageToken" in response:
                        async with get(response["nextPageToken"]).get(self.url, headers=self.auth) as resp:
                            newText = await resp.text()
                            if resp.status == 200:
                                response = self.json.loads(newText)
                                changeLog.extend(response["changeLogs"])
                            if resp.status == 500:
                                break
                    changeLog = [x for x in changeLog if "subaccountId" in x.keys()]
                    changeLog = [x["objectId"] for x in changeLog if x['subaccountId'] == '23262'] 
                    self.logs = changeLog   
                    print("%s total number of campaigns found created after %s" % (len(changeLog), changeTime))
                else:
                    self.handleError(text)
                    self.logs = []
                print(self.logs)
                
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
        else:
            changeLogEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(changeLogEvent)
        return self
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)   
    def activateTrackingAds(self):
        from modules.Ad import Ad
        from modules.AsyncCampaign import AsyncCampaign
        from modules.Placements import Placement
        import re
        # async def wait(payload, placementObject):
        #     async with self.session.patch(self.url, headers=self.auth, data=self.json.dumps(payload)) as r:
        #         text = await r.text()
        #         if r.status == 200:
        #             response = self.json.loads(text)['placementAssignments']
        #             if placementObject in response:
        #                 print("{0} updated successfully".format(self.body['name']))
        #         else:
        #             print("{0} failed to update.".format(self.body['name']))
        #             self.handleError(text)
        def getModifiedAds(adsToUse,existingads):
            modifiedAds = []
            existingads = [x["name"].strip() for x in existingads]
            for ad in adsToUse:
                currentAd = Ad(ad, self.eventLoop,self.session)
                adName = currentAd.body["name"]
                if adName.strip() not in existingads:
                    modifiedAds.append(ad)
            return modifiedAds
        def pullAdsIntoCampaign(campaign, modifiedAds=None):
            englishAds = ["411816686","411815576", "411848029", "411816665"]
            spanishAds = ["409389455", "409389461","410964991", "409389458"]
            adsToUse = None
            if "Hispanic" in campaign.body["name"]:
                adsToUse = spanishAds
            else:
                adsToUse = englishAds
            if modifiedAds != None or len(modifiedAds) == 0:
                adsToUse = getModifiedAds(adsToUse, modifiedAds)
            for ads in adsToUse:
                currentAd = Ad(ads, self.eventLoop,self.session).copy(campaign.body["id"])
                currentAd.insertAd()

        def associatePlacement(ad, placement):
            try:
                ad.body['placementAssignments']
            except:
                ad.body['placementAssignments'] = []
            placementObject = {"active":True, "placementIdDimensionValue":placement.body["idDimensionValue"], "sslRequired":placement.body["sslRequired"], "placementId":placement.body["id"]}
            if placementObject not in ad.body['placementAssignments']:
                ad.body['placementAssignments'].append(placementObject)
                ad.url = "https://www.googleapis.com/dfareporting/v2.8/userprofiles/{profile_id}/ads?id={adId}".format(profile_id=self.profile_id,adId=ad.body["id"])
                payload = {"placementAssignments" : ad.body['placementAssignments']}
                ad.insertPlacement(payload,placementObject, placement.body["campaignId"]).activateAd()

        regex = re.compile(r'(\d+)LM\/')
        for placmentID in range(0, len(self.logs)): 
            print("checking placement %s of %s" % (str(placmentID + 1), len(self.logs)))
            placement = Placement(self.logs[placmentID], self.eventLoop, self.session).getAdList()
            print(placement.body["name"])
            campaign = AsyncCampaign(placement.body['campaignId'], self.eventLoop, self.session)
            campaignName = campaign.body["name"]
            if "_SS_" in placement.body["name"] and regex.search(campaignName):
                placement.getAdList()
                placement.ads = [x for x in placement.ads if "TRACKING" in x["name"]]
                campaign.getAds()
                trackingAdList = [x for x in campaign.adList if "TRACKING" in x["name"]]
                print(len(trackingAdList))
                if len(trackingAdList) > 4:
                    BonusAd = [x for x in campaign.adList if "TRACKING" in x["name"] and "Bonus" in x["name"]][0]
                    FirstAd = [x for x in campaign.adList if "TRACKING" in x["name"] and "First" in x["name"]][0]
                    HolidayAd = [x for x in campaign.adList if "TRACKING" in x["name"] and "Holiday" in x["name"]][0]
                    GeneralAd = [x for x in campaign.adList if "TRACKING" in x["name"] and "General" in x["name"]][0]
                    trackingAdList = [BonusAd, HolidayAd, FirstAd, GeneralAd]
                if len(trackingAdList) < 4:
                    pullAdsIntoCampaign(campaign, trackingAdList)
                    campaign.getAds()
                    trackingAdList = [x for x in campaign.adList if "TRACKING" in x["name"]]
                numberOfAds = len(placement.ads)
                print(numberOfAds)
                if numberOfAds < 4:
                    for ad in trackingAdList:
                        adObject = Ad(ad["id"], self.eventLoop,self.session)
                        associatePlacement(adObject, placement)
        return self
#                if numberOfAds == 4:
#                   for ad in placement.ads:
#                       Ad(ad["id"], self.eventLoop,self.session).activateAd()
            
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)       
    def modifySSPlacements(self):
        def printResult(placementArray):
            import pandas as pd
            from modules import send_mail
            df = pd.DataFrame(data=placementArray)
            
            writer = pd.ExcelWriter('Placement.xlsx',engine='xlsxwriter')
            workbook = writer.book
            headerObject = {"A1":"Campaign Name", "B1":"Placement Name"}
            format1 =  workbook.add_format({'bg_color': '#0AADE9'})
            
            df.to_excel(writer, sheet_name ="Placements", index = False)
            worksheet =  writer.sheets['Placements']
            for obj in headerObject:
                worksheet.write(obj, headerObject[obj], format1) 
            print("Done!")    
            writer.save()
            import os
            directories = os.listdir()
            reports = [x for x in directories if "Placement" in x]
            for report in reports:
                send_mail.send_email(report, title="LMA SS Placements",recipients=["Lennon.Turner@amnetgroup.com","Kristine.Gillette@carat.com","Holly.Champoux@carat.com","Ali.Ciaffone@carat.com"])
        from modules.Placements import Placement
        from modules.AsyncCampaign import AsyncCampaign
        changedPlacementsArray = []
        import re
        regex = re.compile(r'(\d+)LM\/')
        for placmentID in range(0, len(self.logs)): 
            print("checking placement %s of %s" % (str(placmentID + 1), len(self.logs)))
            placement = Placement(self.logs[placmentID], self.eventLoop, self.session)
            if placement.body['tagSetting']['includeClickThroughUrls'] == False:
                campaign = AsyncCampaign(placement.body['campaignId'], self.eventLoop, self.session)
                campaignName = campaign.body["name"]
                if regex.search(campaignName):
                    changedPlacementsArray.append({"placementName":placement.body["name"],"campaignName":campaign.body['name']})
                    print("%s in %s is currently being updated." % (placement.body["name"],campaign.body['name']))
                    placement.pushStaticClickTracking()
        if len(changedPlacementsArray) > 0:
            printResult(changedPlacementsArray)
        return self
                
        
    # @retry(wait_exponential_multiplier=10, wait_exponential_max=100)     
    def getCurrentObject(self, changeTime,objectType):
        import re
        actualObject = re.sub("OBJECT_","",objectType).lower()
        print(actualObject)
        def get(nextPageToken=None):
            if nextPageToken is None:
                self.url = "https://www.googleapis.com/dfareporting/v2.8/userprofiles/{profile_id}/changeLogs?objectType={objectType}&minChangeTime={changeTime}".format(profile_id=self.profile_id, changeTime=changeTime, objectType=objectType)
            else:
                self.url = "https://www.googleapis.com/dfareporting/v2.8/userprofiles/{profile_id}/changeLogs?&objectType={objectType}&minChangeTime={changeTime}&pageToken={pageToken}".format(profile_id=self.profile_id, changeTime=changeTime,pageToken=nextPageToken,objectType=objectType)
            return self.session
        async def wait():
            async with get().get(self.url, headers=self.auth) as r:
                text = await r.text()
                if r.status == 200:
                    response = self.json.loads(text)
                    changeLog = response["changeLogs"]
                    while "nextPageToken" in response:
                        async with get(response["nextPageToken"]).get(self.url, headers=self.auth) as resp:
                            newText = await resp.text()
                            if resp.status == 200:
                                response = self.json.loads(newText)
                                changeLog.extend(response["changeLogs"])
                            if resp.status == 500:
                                break
                    changeLog = [x for x in changeLog if "subaccountId" in x.keys()]
                    changeLog = [x for x in changeLog if x['subaccountId'] == '23262']
                    setattr(self,actualObject,changeLog)
                    # self.logs = changeLog  
                    print("%s total number of %s found created after %s" % (len(changeLog), actualObject, changeTime))
                else:
                    self.handleError(text)
                    setattr(self,objectType,[])
        if self.eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
        else:
            changeLogEvent = self.eventLoop.create_task(wait())
            self.eventLoop.run_until_complete(changeLogEvent)
        return self   
    def __str__(self):
        return "changeLogs"