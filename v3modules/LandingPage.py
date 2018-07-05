from modules.TraffickingObject import TraffickingObject
from retrying import retry

class LandingPage(TraffickingObject):
    
    # @retry(wait_exponential_multiplier=10, wait_exponential_max=100) 
    def __init__(self, searchString="", eventLoop=None, session=None):
        super().__init__()
        self.get_body(searchString)
        
    def __str__(self):
        return "advertiserLandingPages"