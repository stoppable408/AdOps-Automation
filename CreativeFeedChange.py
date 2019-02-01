from v3modules import DCMAPI, CreativeUtils
import pandas,re
multiCreativeList = []
Api = DCMAPI.DCMAPI()
df = pandas.read_csv("Full Placement Report.csv")
df = df[["Campaign_name","Campaign_id","Placement_Name","Placement_id","Planned_Cost","Planned_Impressions","Start_date","End_date","Date of Creation","Placement_Group_Name","Placement_Group_Id"]]
test = 0
def changeNumber(number):
    return number/1000000000
#     finalObject["Planned_Cost"] = int(placement['pricingSchedule']["pricingPeriods"][0]["rateOrCostNanos"])/1000000000

df["Planned_Cost"] = df["Planned_Cost"].apply(changeNumber)
df["Action"] = "Create"
df.to_csv("Full Placement Report2.csv", sep="^")

# def changeCreativeName(row):
#     global multiCreativeList
#     creativeName = re.sub("\\xa0","",row["Current Feed Name in DCM"])
#     listValues = {"searchString":creativeName}
#     creativeList = CreativeUtils.listCreatives(Api, listValues)
#     if len(creativeList) == 1:
#         creative = creativeList[0]
#         creativeId = creative["id"]
#         creativeFeed = row["New 2019 Creative Feed Name"]
#         payload = {"name":creativeFeed}        
#         CreativeUtils.updateCreative(Api,creativeId,payload)
#     elif len(creativeList) > 1:
#         multiCreativeList.append(creativeName)
        


# df.apply(changeCreativeName,axis=1)
# writer = pandas.ExcelWriter('Report.xlsx',engine='xlsxwriter')
# workbook = writer.book
# df.to_excel(writer, sheet_name ="Info", index = False)
# worksheet =  writer.sheets['Info']
# writer.save()
        