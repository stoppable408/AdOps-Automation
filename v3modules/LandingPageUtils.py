

def getAllDisplayLandingPages(Api):
    Landingpages = []
    advertiserSet ={
    "5288214":"GLO»Chevrolet FC»Display»A",
    "5354228":"GLO»Chevrolet Global Advertising»Display»A",
    "6015329":"GLO»Global Content Studio»Display»A",
    "4568611":"US»ACDelco»Display»A",
    "3876773":"US»Buick»Display»A",
    "6198719":"US»Cadillac Certified Pre-Owned»Display»A",
    "3876774":"US»Cadillac»Display»A",
    "3876777":"US»Certified Pre-Owned»Display»A",
    "4569406":"US»Certified Service»Display»A",
    "4569405":"US»Chevrolet Performance»Display»A",
    "3876771":"US»Chevrolet»Display»A",
    "5361629":"US»Factory Pre-Owned Collection»Display»A",
    "3876780":"US»Fleet Commercial Operations»Display»A",
    "4568613":"US»Genuine GM Parts»Display»A",
    "4635253":"US»GM Accessories»Display»A",
    "3876782":"US»GM Card»Display»A",
    "4496783":"US»GM Finance and Insurance»Display»A",
    "4852937":"US»GM Fuels and Lubes»Display»A",
    "5724659":"US»GM Marine»Display»A",
    "4508180":"US»GM Marketing Strategy Support and Recall»Display»A",
    "3876772":"US»GMC»Display»A",
    "5314814":"US»Maven»Display»A",
    "3876775":"US»OnStar»Display»A",
    "5139395":"US»Vehicle Purchase Programs»Display»A"}
    for advertiser in advertiserSet:
        listValues = {"advertiserIds":advertiser,"archived":False}
        print(advertiser, len(Landingpages))
        Landingpages.extend(Api.generateRequestUrl("advertiserLandingPages",listValues=listValues).getlist("landingPages").response)
    return Landingpages

def updateLandingPage(Api, landingPageId,payload):
    Api.generateRequestUrl("advertiserLandingPages",listValues={"id":landingPageId}).patch(payload)