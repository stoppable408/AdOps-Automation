from v3modules.DCMAPI import DCMAPI
counters = 0
Api = DCMAPI()
def analyzeFile(file_name):
    
    import pandas as pd
    from v3modules import CampaignUtils, PlacementUtils
    import numpy as np
    import openpyxl
    import re

    if ".csv" in file_name:
        csv = pd.read_csv(file_name)
        file_name = re.sub('.csv','.xlsx',file_name)

    else:
        csv = pd.read_excel(file_name,sheetname=0)
    #for item in file_name


    csv.fillna('N/A',inplace=True)
    
    
    def nameChange(name, site):
        global counters
        
        import re
        site = site.loc[counters]
        if "Carat_" in name:
            site = re.sub(r'\(\d+\)',"", site).strip() + "_"
            name = re.sub("Carat_", site, name)
        counters += 1
        return name
        
        
    def dateTimetoDate(value):
        import datetime
        import re
        if isinstance(value, datetime.date):
                    value = value.strftime("%m"+"/"+"%d"+"/"+"%Y")
                    month = value.split('/')[0]
                    if month.startswith('0'):
                        month = re.sub('0',"",month)
                    day = value.split('/')[1]
                    if day.startswith('0'):
                        day = re.sub('0',"",day)
                    year = value.split('/')[2]
                    date = month + "/" + day + "/" + year
                    value = date
        return value
    
    
    csv["Start date"] = csv["Start date"].apply(dateTimetoDate)
    csv["End date"] = csv["End date"].apply(dateTimetoDate)
    csv["Name"] = csv["Name"].apply(nameChange, args=(csv["Site"],))
    csv = csv[csv['Compatibility'] != 'N/A']
    try:
        placementID = csv["Id"].iloc[0]
    except:
        placementID = csv_ss_placement["Id"].iloc[0]
    placement = PlacementUtils.getPlacement(Api, placementID)
    campaignID = placement['campaignId']
    campaign = CampaignUtils.getCampaign(Api, campaignID)["name"]
    #campaign = campaignName
    csv['Campaign'] = campaign
    csv['Creative Rotation'] = np.nan
    csv['Creative File 1'] = np.nan
    csv['Creative File 2'] = np.nan
    csv['Creative File 3'] = np.nan
    csv['Creative File 4'] = np.nan
    csv['Creative File 5'] = np.nan
    del csv['Object type']
    del csv['Status']
    # REORDER COLUMNS
    csv = csv[['Campaign','Site','Id',
              'Name','Start date','End date',
              'Compatibility','Dimensions','Creative Rotation',
              'Creative File 1','Creative File 2','Creative File 3',
              'Creative File 4','Creative File 5']]
    csv_ss_placement = csv[csv['Dimensions'] == '1x1']
    csv = csv[csv['Dimensions'] != '1x1']
    site_list = csv_ss_placement['Site'].unique().tolist()
    
    def getDimensions(placement):
        if type(placement) is str:
            return str(placement).split("_")[3]
    
        
    csv_ss_placement["Dimensions"] = csv_ss_placement["Name"].apply(getDimensions)
    csv["Dimensions"] = csv["Name"].apply(getDimensions)


    for i in range(3):
        csv_ss_placement = csv_ss_placement.append(
            pd.Series(
                [np.nan,np.nan,np.nan,np.nan,np.nan,
                 np.nan,np.nan,np.nan,np.nan,np.nan,
                 np.nan,np.nan,np.nan,np.nan,],
                index=csv_ss_placement.columns.tolist()),ignore_index=True)

    csv_ss_placement = csv_ss_placement.append(
        pd.Series(
            ['Site','Contact',np.nan,np.nan,np.nan,
             np.nan,np.nan,np.nan,np.nan,np.nan,
             np.nan,np.nan,np.nan,np.nan,],
            index=csv_ss_placement.columns.tolist()),ignore_index=True)
    siteRow = len(csv_ss_placement) + 1

    for site in site_list:
        csv_ss_placement = csv_ss_placement.append(
            pd.Series(
                [site,np.nan,np.nan,np.nan,np.nan,
                 np.nan,np.nan,np.nan,np.nan,np.nan,
                 np.nan,np.nan,np.nan,np.nan,],
                index=csv_ss_placement.columns.tolist()),ignore_index=True)

  
    urls = pd.DataFrame(data={'Creative File':[],'Creative URL':[]})

    writer = pd.ExcelWriter('Output/%s' % (file_name),engine='xlsxwriter')
    workbook = writer.book
    
    headerObject = {"A1":"Campaign", "B1":"Site", "C1":"Id", "D1":"Name","E1":"Start Date","F1":"End Date","G1":"Compatibility","H1":"Dimensions","I1":"Creative Rotation","J1":"Creative File 1","K1":"Creative File 2","L1":"Creative File 3","M1":"Creative File 4","N1":"Creative File 5"}
    urlObject = {'A1':"Creative File", "B1":"Creative URL"}
    siteObject = {'A' + str(siteRow):"Site", 'B' + str(siteRow):"Contact"}
    format1 =  workbook.add_format({'bg_color': '#0AADE9'})

    if len(csv) != 0:
        csv.to_excel(writer, sheet_name='TPS Placements',index=False)
        worksheet_csv = writer.sheets['TPS Placements']
        for obj in headerObject:
            worksheet_csv.write(obj, headerObject[obj], format1) 
    
    if len(csv_ss_placement) > 4:
            print(len(csv_ss_placement))
            csv_ss_placement.to_excel(writer, sheet_name='SS Placements',index=False)
            worksheet_csv_ss_placements = writer.sheets['SS Placements']
            for obj in headerObject:
                worksheet_csv_ss_placements.write(obj, headerObject[obj], format1)
            for obj in siteObject:
                worksheet_csv_ss_placements.write(obj, siteObject[obj], format1)
                
    urls.to_excel(writer, sheet_name='URLs',index=False)
    worksheet_URLs = writer.sheets['URLs']
    for obj in urlObject:
        worksheet_URLs.write(obj, urlObject[obj], format1)
    
    writer.save()
    
import os

fileList = [x for x in os.listdir() if ("csv" in x or "xlsx" in x) and "CSD" in x]



for file in range(0, len(fileList)):
    print("Reading file "+ str(file + 1) + " of " + str(len(fileList))+".")
    #campaignName = input("please enter Camapaign Name that goes with {0}:".format(fileList[file]))
    analyzeFile(fileList[file])
    print(str(fileList[file]) + " has been successfully run\n")
    counters = 0
print("All files have been successfully run")
