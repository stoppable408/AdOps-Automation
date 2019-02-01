# #weekly, every monday
from v3modules import LandingPageUtils, DCMAPI

Api = DCMAPI.DCMAPI()
test = LandingPageUtils.getAllDisplayLandingPages(Api)
temp = 0
# from v3modules.TraffickingObject import TraffickingObject
# from v3modules.Campaign import Campaign
# import time
# #practice file for getting placement info for tag generation report.
# landingPageArray = []
# advertiserSet ={
#     "5288214":"GLO»Chevrolet FC»Display»A",
#     "5354228":"GLO»Chevrolet Global Advertising»Display»A",
#     "6015329":"GLO»Global Content Studio»Display»A",
#     "4568611":"US»ACDelco»Display»A",
#     "3876773":"US»Buick»Display»A",
#     "6198719":"US»Cadillac Certified Pre-Owned»Display»A",
#     "3876774":"US»Cadillac»Display»A",
#     "3876777":"US»Certified Pre-Owned»Display»A",
#     "4569406":"US»Certified Service»Display»A",
#     "4569405":"US»Chevrolet Performance»Display»A",
#     "3876771":"US»Chevrolet»Display»A",
#     "5361629":"US»Factory Pre-Owned Collection»Display»A",
#     "3876780":"US»Fleet Commercial Operations»Display»A",
#     "4568613":"US»Genuine GM Parts»Display»A",
#     "4635253":"US»GM Accessories»Display»A",
#     "3876782":"US»GM Card»Display»A",
#     "4496783":"US»GM Finance and Insurance»Display»A",
#     "4852937":"US»GM Fuels and Lubes»Display»A",
#     "5724659":"US»GM Marine»Display»A",
#     "4508180":"US»GM Marketing Strategy Support and Recall»Display»A",
#     "3876772":"US»GMC»Display»A",
#     "5314814":"US»Maven»Display»A",
#     "3876775":"US»OnStar»Display»A",
#     "5139395":"US»Vehicle Purchase Programs»Display»A"
# }
# traffickingObject = TraffickingObject()
# landingpages = traffickingObject.getAllLandingPages().landingPages

# for element in range(0,len(landingpages)):
#     print("reading element {number} out of {maxi}".format(number=element,maxi=len(landingpages)))
#     page = landingpages[element]

#     advertiserName = advertiserSet[page["advertiserId"]]
#     # if advertiserName != "US»Chevrolet»Display»A":
#     #     continue
#     pageName = page["name"]
#     pageID = page["id"]
#     url = page["url"]
#     print(url)
#     try:
#         r = traffickingObject.requests.get(url)
#         status_code = r.status_code
#     except Exception as e:
#         status_code = e
#         print(url)
#     landingpageObject = {
#             "Advertiser":advertiserName,
#             "Name":pageName,
#             "Landing Page ID":pageID,
#             "Url":url,
#             "Status Code":status_code
#     }
#     landingPageArray.append(landingpageObject)
# import pandas as pd
# df = pd.DataFrame(data=landingPageArray)
# writer = pd.ExcelWriter('Landing Page Report.xlsx',engine='xlsxwriter')
# workbook = writer.book
# df.to_excel(writer, sheet_name ="Info", index = False)
# worksheet =  writer.sheets['Info']
# writer.save()
    