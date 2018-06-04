from modules.TraffickingObject import TraffickingObject
from retrying import retry

class Creative(TraffickingObject):
    
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100) 
    def __init__(self, searchString, eventLoop=None, session=None):
        super().__init__()
        if hasattr(self, "session"):
            session = self.session
        self.get_body(searchString,eventLoop, session)
        if eventLoop != None:
             self.eventLoop = eventLoop
        
    def __str__(self):
        return "creatives"