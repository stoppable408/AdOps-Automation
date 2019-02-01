import pandas
import numpy
import time
import os
from v3modules import Smartsheets, PlacementUtils, CampaignUtils, DCMAPI, MailUtils

Api = DCMAPI.DCMAPI()
csvpath = "https://drive.google.com/uc?export=download&id=1_qaMXaX8TlI6-v8cBuI0XDZ5zDKqOoxF"
fileList = []
import requests
import shutil
import pandas
import os
p = requests.get(csvpath, verify=True,stream=True)
p.raw.decode_content = True
with open("placement info.csv", 'wb') as f:
            shutil.copyfileobj(p.raw, f)
print("done")

csdDict = Smartsheets.completeCSDDict()
