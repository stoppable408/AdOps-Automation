from abc import ABCMeta, abstractmethod
from retrying import retry

# Abstract class that imports the json and requests modules, which is used heavily throughout the application
# Also contains the methods that all children will use. 
token = None
eventLoop = None
counter = 0
class TraffickingObject(metaclass=ABCMeta):
    __metaclass__ = ABCMeta
    import json
    import requests
    import asyncio
    import aiohttp
    
    def __init__(self):
        if token  == None:
            print("getting token")
            self.getToken()
        else:
            self.profile_id, self.auth = token[0],token[1]
            
    @retry(wait_exponential_multiplier=10, wait_exponential_max=100)   
    def getToken(self):
        global token
        global counter
        import os
        import httplib2
        from oauth2client import file as oauthFile
      
        try:
            
            storage = oauthFile.Storage(os.getcwd() + "/modules/dfareporting.dat")
            credentials = storage.get()
            credentials.refresh(httplib2.Http())
            self.profile_id, self.auth = 2532624 , {'Content-type': 'application/json', "Authorization": "OAuth %s" % credentials.access_token}
            
            self.session = self.aiohttp.ClientSession()
            token = (self.profile_id, self.auth)
        except:
            print("dfa file not found")
            
    def handleError(self, response):
        error = self.json.loads(response)['error']['errors'][0]['message']
        print(error)
        if "Invalid" in error:
            print("getting new credentials")
            print(self.session._default_headers)
            self.getToken()
            print(self.session._default_headers)
        else:
            print(response)
        raise Exception("Throw to retry")

    def get_body(self, searchString, eventLoop=None, session=None):
        searchString = str(searchString).strip()
        className = str(self)
        if session != None:
            self.session = session
        else:
            self.getToken()
        self.url = "https://www.googleapis.com/dfareporting/v3.1/userprofiles/{profile_id}/{className}?searchString={searchString}".format(className=className,profile_id=self.profile_id,searchString=searchString)
        async def wait():
            async with self.session.get(self.url, headers=self.auth) as r:
                text = await r.text()
                if r.status == 200:
                    try:
                        print("this is a :", className)
                        self.body = self.json.loads(text)[className][0]
                    except:
                        self.handleError(text)
                else:
                    self.handleError(text)
        if eventLoop == None:
            self.eventLoop = self.asyncio.get_event_loop()
            self.eventLoop.run_until_complete(wait())
        else:
            eventLoop.run_until_complete(eventLoop.create_task(wait()))
        return self
        
    @abstractmethod
    def __str__(self):
        pass