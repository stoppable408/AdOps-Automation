from v3modules import DCMAPI, ChangeLogUtils, UtilUtils, PlacementUtils, CampaignUtils
import re,pandas
Api = DCMAPI.DCMAPI()
listValues = {"objectType":"OBJECT_AD", "minChangeTime":UtilUtils.getBeginningofWeek()}
logs = ChangeLogUtils.getChangeLog(Api, listValues)
logs = [re.sub(", active: true|id: ","",x["newValue"]) for x in logs if x["fieldName"] == 'Placement assignment']
logs = [x for x in logs if x != ""]
logs = list(set(logs))

def analyzePlacements(placementId):
    placement = PlacementUtils.getPlacement(Api, placementId)
    if "»SS»" not in placement["name"]:
        return None
    campaignId = placement["campaignId"]
    campaign = CampaignUtils.getCampaign(Api, campaignId)
    regex = re.compile("[1-5]L(M|G)")
    if regex.search(campaign["name"]): 
        return {"Campaign Name":campaign["name"], "Placement Id": placement["id"], "Placement Name":placement["name"]}
    else:
        return None

logs = [analyzePlacements(x) for x in logs]
logs = [x for x in logs if x != None]

df = pandas.DataFrame(data=logs)
df = df[["Campaign Name","Placement Id","Placement Name"]]
writer = pandas.ExcelWriter('Placement Report.xlsx',engine='xlsxwriter')
df.to_excel(writer, sheet_name ="Info", index = False)
writer.save()
