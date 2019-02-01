from v3modules import DCMAPI, CampaignUtils, ChangeLogUtils, UtilUtils, PlacementUtils, SiteUtils, Smartsheets, sFTPConnector, MailUtils
import pandas, datetime, re
import numpy as np
missingContacts = []
ProgrammaticSites = ["2401207"]
Evidon = ["EV1","EV2","EV3","EVD","EVG","EVL","EVR","EVS","EVA","EVT","EVC","GAC","LMA","LMR","LMC"]
headerObject = {"A1":"Campaign", "B1":"Site", "C1":"Id", "D1":"Name","E1":"Start Date","F1":"End Date","G1":"Compatibility","H1":"Dimensions","I1":"Evidon","J1":"Creative Rotation","K1":"Creative File 1","L1":"Creative File 2","M1":"Creative File 3","N1":"Creative File 4","O1":"Creative File 5"}
urlObject = {'A1':"Creative File", "B1":"Creative URL"}
advertiserObject = {"5288214":"GM Global",
"5354228":"GM Global",
"6015329":"GM Global",
"3876773":"Buick",
"6198719":"Cadillac",
"3876774":"Cadillac",
"3876771":"Chevrolet",
"3876772":"GMC",
"5314814":"Maven"
}
SiteContacts = Smartsheets.getSiteContacts()
LMASiteContacts = Smartsheets.getLMASiteContacts()

finalSiteContacts = None
LMAOverride = False
def getFolderName(advertiserId):
    if advertiserId in advertiserObject:
        return advertiserObject[advertiserId]
    else:
        return "Corporate Brands"
def isEvidon(placementName):
    global LMAOverride
    if LMAOverride == True:
        return "Y"
    for string in Evidon:
        if string in placementName:
            return "Y"
    return "N"
def getContacts(campaignName):
    global finalSiteContacts
    global LMAOverride
    if isLMA(campaignName):
        finalSiteContacts = LMASiteContacts
        LMAOverride = True
    else:
        finalSiteContacts = SiteContacts

def determineDimensions(placement):
    if placement["compatibility"] == 'IN_STREAM_VIDEO' or "_SS_" in placement["name"] or  "»SS»" in placement["name"]:
        try:
            return str(placement["name"]).split("_")[3]
        except:
            dimensions = str(placement["name"]).split("»")[5]
            if "T1" in dimensions:
                dimensions = "120+N/A"
            else:
                dimensions = re.sub("\(NA\)\+","",dimensions)
            
            return dimensions
    else:
        return PlacementUtils.sizeToDimension(placement["size"])

def createFileName(fileName):
    dateForToday = datetime.datetime.today().strftime("%m.%d.%y")
    return "_".join(fileName.split("_")[1:]) + " " + dateForToday + ".xlsx"

def isLMA(campaignName):
    lmaPattern = re.compile("[1-5]L(M|G)")
    if re.match(lmaPattern,campaignName):
        return True
    return False
def addSiteContacts(siteSet,contacts):
    siteContactList = []
    def listify(contactList):
        string = ""
        for contact in contactList:
            string += contact + ", "
        string = string[:-2]
        return string
    siteList = list(siteSet)
    for site in siteList:
        if site in ProgrammaticSites:
            continue
        siteObject = SiteUtils.getSite(Api,site)
        siteName = "{0} ({1})".format(siteObject["name"], siteObject["id"])
        try:
            contactList = listify(contacts[site])
        except:
            contactList = " "
            missingContacts.append(siteName)

        siteContactList.append([siteName, contactList])
    return siteContactList
def appendSiteInfo(df, finalSiteAddition):
    for i in range(3):
        df = df.append(
        pandas.Series(
            [np.nan,np.nan,np.nan,np.nan,np.nan,
                np.nan,np.nan,np.nan,np.nan,np.nan,
                np.nan,np.nan,np.nan,np.nan,np.nan,],
            index=df.columns.tolist()),ignore_index=True)
    
    df = df.append(
        pandas.Series(
            ['Site','Contact',np.nan,np.nan,np.nan,
             np.nan,np.nan,np.nan,np.nan,np.nan,
             np.nan,np.nan,np.nan,np.nan,np.nan,],
            index=df.columns.tolist()),ignore_index=True)
    for site in finalSiteAddition:
        df = df.append(
        pandas.Series(
            [site[0],site[1],np.nan,np.nan,np.nan,
             np.nan,np.nan,np.nan,np.nan,np.nan,
             np.nan,np.nan,np.nan,np.nan,np.nan,],
            index=df.columns.tolist()),ignore_index=True)

    return df
    
#creating instance of Api
Api = DCMAPI.DCMAPI()
connector = sFTPConnector.sFTPConntector()
beginningOfWeek = UtilUtils.getYesterday()
campaignListValues = {"action":"action_create","objectType":"OBJECT_CAMPAIGN","minChangeTime":beginningOfWeek}
newCampaigns = ChangeLogUtils.getChangeLog(Api, campaignListValues)
newCampaigns = [x for x in newCampaigns if x["subaccountId"] == "23262"]
finalPlacementList = []
for campaignObject in newCampaigns:
    siteSet = set()
    campaignId = campaignObject["objectId"]
    campaign = CampaignUtils.getCampaign(Api,campaignId)
    getContacts(campaign["name"])
    advertiserId = campaign["advertiserId"]
    listValues = {"campaignIds":campaignId, "archived":False}
    placementList = PlacementUtils.listPlacement(Api,listValues)
    for placement in placementList:
        print(placement["name"])
        site = SiteUtils.getSite(Api, placement["siteId"])
        siteSet.add(site["id"])
        siteName = "{0} ({1})".format(site["name"], site["id"])
        placementObject = {
            "Campaign":campaign["name"],
            "Site":siteName,
            "Id":placement["id"],
            "Name":placement["name"],
            "Start Date":UtilUtils.formatPlacementDate(placement['pricingSchedule']['startDate']),
            "End Date":UtilUtils.formatPlacementDate(placement['pricingSchedule']['endDate']),
            "Compatibility":placement["compatibility"].capitalize(),
            "Dimensions":determineDimensions(placement),
            "Evidon": isEvidon(placement["name"]),
            "Creative Rotation":" ",
            "Creative File 1":" ",
            "Creative File 2":" ",
            "Creative File 3":" ",
            "Creative File 4":" ",
            "Creative File 5":" "
        }
        finalPlacementList.append(placementObject)
    finalTPSPlacements = [x for x in finalPlacementList if "»TP»" in x["Name"]]
    finalSSPlacements = [x for x in finalPlacementList if "»SS»" in x["Name"]]
    
    
    fileName = createFileName(re.sub("\/","_",campaign["name"]))
    print(fileName)
    writer = pandas.ExcelWriter('%s' % (fileName),engine='xlsxwriter')
    workbook = writer.book
    headerBlue =  workbook.add_format({'bg_color': '#0AADE9'})
    if len(finalTPSPlacements) > 0: 
        df = pandas.DataFrame(finalTPSPlacements)
        df =  df[['Campaign', 'Site', 'Id', 'Name', 'Start Date', 'End Date', 'Compatibility', 'Dimensions', "Evidon", 'Creative Rotation', 'Creative File 1', 'Creative File 2', 'Creative File 3', 'Creative File 4', 'Creative File 5']]
        df.to_excel(writer, sheet_name="TPS Placements",index=False)
        TPSSheet = writer.sheets['TPS Placements']
        for obj in headerObject:
                TPSSheet.write(obj, headerObject[obj], headerBlue)

    if len(finalSSPlacements) > 0: 
        df = pandas.DataFrame(finalSSPlacements)
        df =  df[['Campaign', 'Site', 'Id', 'Name', 'Start Date', 'End Date', 'Compatibility', 'Dimensions',"Evidon", 'Creative Rotation', 'Creative File 1', 'Creative File 2', 'Creative File 3', 'Creative File 4', 'Creative File 5']]
        df = appendSiteInfo(df, addSiteContacts(siteSet,finalSiteContacts))
        df.to_excel(writer, sheet_name="SS Placements",index=False)
        SSheet = writer.sheets['SS Placements']
        for obj in headerObject:
                SSheet.write(obj, headerObject[obj], headerBlue)
    urls = pandas.DataFrame(data={'Creative File':[],'Creative URL':[]})
    urls.to_excel(writer, sheet_name='URLs',index=False)
    worksheet_URLs = writer.sheets['URLs']
    for obj in urlObject:
        worksheet_URLs.write(obj, urlObject[obj], headerBlue)
    writer.save()
    connector.uploadFile(fileName,getFolderName(advertiserId))

if len(missingContacts) > 0:
    contacts = ",".join(missingContacts)
    subject = "Here's a list of missing contacts from today's CSD Pull"
    message = contacts
    recipients = ["Lennon.Turner@carat.com"]
    MailUtils.send_message(subject,message,recipients)