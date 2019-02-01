from v3modules import DCMAPI, RemarketingUtils

def modifyRules(listPopulationRule):
    for clause in listPopulationRule["listPopulationClauses"]:
        for term in clause["terms"]:
            if term["value"] == "ua" or term["value"] == "ue":
                term["value"] = "ae"
    return {"listPopulationRule":listPopulationRule}
Api = DCMAPI.DCMAPI()

advertiserId = 3969705

listValues = {"advertiserId": advertiserId, "name": "- UA -"}

audiences = RemarketingUtils.getRemarketingList(Api, listValues)
for audience in audiences:
    print("reading {audience}".format(audience=audience["name"]))
    audienceId = audience["id"]
    listPopulationRule = modifyRules(audience['listPopulationRule'])
    RemarketingUtils.updateRemarketingList(Api, audienceId, listPopulationRule)
