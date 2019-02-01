from v3modules import DCMAPI, RemarketingUtils
import pandas

Api = DCMAPI.DCMAPI()
Api.profile_id = 2706989
dfaList = []
columnSet = set()
listValues = {"advertiserId":"3856619","active":True}
audienceList = RemarketingUtils.getRemarketingList(Api, listValues,requiredParameter="advertiserId=3856619")
def sortList(columnList):
    numSet = set()
    def testNum(name):
        return any(char.isdigit() for char in name)
    def sortVariables(variableList, numList):
        finalList = []
        for num in numList:
            varList = [c for c in variableList if num in c]
            name = varList[varList.index("variableName"+num)]
            value = varList[varList.index("value"+num)]
            operator = varList[varList.index("operator"+num)]
            varListCopy = [name, operator, value]
            finalList = finalList + varListCopy
        return finalList
    baseList = ["id","name","description","listSize","listSource"]
    varElements = [x for x in columnList if testNum(x)]
    [numSet.add(x[-1]) for x in varElements]
    numList = sorted(list(numSet))
    varElements = sortVariables(varElements, numList)
    return baseList + varElements
for audience in audienceList:
    audienceobj = {
        "name":audience["name"],
        "id":audience["id"],
        "description":audience["description"],
        "listSize":audience["listSize"],
        "listSource":audience["listSource"]
    }
    try:
        audienceobj["lifespan"]:audience["lifespan"]
    except:
        pass        
    try:
        terms = audience["listPopulationRule"]["listPopulationClauses"]
        count = 1
        for term in terms:
            variableName = "variableName" + str(count)
            value = "value" + str(count)
            operator = "operator" + str(count)
            audienceobj[variableName] = term["terms"][0]["variableName"]
            audienceobj[operator] = term["terms"][0]["operator"]
            audienceobj[value] = term["terms"][0]["value"]
            count += 1
    except:
        pass
    dfaList.append(audienceobj)

for obj in dfaList:
    for key in obj:
        columnSet.add(key)
columnList = sortList(list(columnSet))

df = pandas.DataFrame(dfaList)
df = df[columnList]
writer = pandas.ExcelWriter('Argentina Report.xlsx',engine='xlsxwriter')
workbook = writer.book
df.to_excel(writer, sheet_name ="Info", index = False)
worksheet =  writer.sheets['Info']
writer.save()   