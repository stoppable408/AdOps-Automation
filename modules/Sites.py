from modules.TraffickingObject import TraffickingObject
from retrying import retry

class Sites(TraffickingObject):
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)   
    def __init__(self, siteID, eventLoop=None, session=None):
        super().__init__()
        if hasattr(self, "session"):
            session = self.session
        self.get_body(siteID,eventLoop, session)
        if eventLoop != None:
             self.eventLoop = eventLoop
        
    def __str__(self):
        return "sites"