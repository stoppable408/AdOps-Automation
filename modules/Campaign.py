from modules.TraffickingObject import TraffickingObject
from modules.Placements import Placement
from retrying import retry

class Campaign(TraffickingObject):
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100) 
    def __init__(self, searchString):
        super().__init__()
        self.get_body(searchString)
        
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)     
    def getAllLMA(self):
        self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/campaigns?searchString=*LM/".format(profile_id=self.profile_id)
        r = self.requests.get(self.url, headers=self.auth)
        if r.status_code == 200:
            response = self.json.loads(r.text)
            campaignList = response["campaigns"]
            while "nextPageToken" in response:
                self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/campaigns?pageToken={pageToken}".format(profile_id=self.profile_id,pageToken = response["nextPageToken"])
                r = self.requests.get(self.url, headers=self.auth)
                if r.status_code == 200:
                    response = self.json.loads(r.text)
                    campaignList.extend(self.json.loads(r.text)["campaigns"])
                self.LMACampaigns = campaignList
        else:
            error = self.json.loads(r.text)['error']['errors'][0]['message']
            print(error)
            self.handleError(error)
            raise Exception("Throw to retry")
        return self
     
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)     
    def getPlacementList(self):
        print("start")
        self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/placements?campaignIds={campaignId}".format(profile_id=self.profile_id,campaignId=self.body["id"])
        r = self.requests.get(self.url, headers=self.auth)
        print(r)
        if r.status_code == 200:
            placementList = self.json.loads(r.text)["placements"]
            placementList = [Placement(x["id"]) for x in placementList]
            self.placements = placementList
        else:
            error = self.json.loads(r.text)['error']['errors'][0]['message']
            print(error)
            self.handleError(error)
            raise Exception("Throw to retry")
        return self
        
    def __str__(self):
        return "campaigns"