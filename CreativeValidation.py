from v3modules import Smartsheets, PlacementUtils, CampaignUtils, DCMAPI, CreativeUtils, AdvertiserUtils


Api = DCMAPI.DCMAPI()
finalCreativeList = []
advertiserSet = AdvertiserUtils.getAdvertiserSet()
acceptableYears = set("2014","2015","2016","2017","2018","2019")
acceptableMessageProducts = set("Avalanche","Bolt EV","Camaro","Camaro Convertible","Camaro Coupe","Camaro ZL1 Convertible","Camaro ZL1 Coupe","City Express","Colorado","Corvette","Corvette 427","Corvette Convertible","Corvette Coupe","Corvette Grand Sport Convertible","Corvette Grand Sport Coupe","Corvette Z06","Corvette ZR1","Corvette Stingray","Cruze","Equinox","Express","Impala","Malibu","Monte Carlo","Silverado 1500","Silverado 2500HD","Silverado 3500HD","Silverado HD","Silverado Hybrid","Sonic Hatchback","Sonic Sedan","Spark","SS","Suburban","Suburban 3/4 Ton","Tahoe","Tahoe Hybrid","Traverse","Trax","Volt","Chevrolet Multi-line","Chevrolet Brand","Sonic","Small Car","Cheyenne","Aveo","ATS","ATS V","ATS-V Coupe","ATS-V Sedan","CT6","CTS","CTS Coupe","CTS V","CTS-V Coupe","CTS Sedan","CTS-V Sedan","Deville","Escala","Escalade","Escalade Hybrid","Escalade ESV","Escalade EXT","ELR","SRX","XTS","XT5","Cadillac Multi-line","Cadillac Brand","ATS Sedan","ATS Coupe","V Series","Enclave","Encore","Envision","Lacrosse","Regal","Verano","Buick Multi-Line","Buick Brand","Cascada","Acadia","Acadia Denali","Canyon","Savana","Savana Passenger","Savana Cargo","Sierra 1500","Sierra 1500 Denali","Sierra 1500 Hybrid","Sierra 2500HD","Sierra 2500HD Denali","Sierra 3500HD","Sierra 3500HD Denali","Sierra 3500 Chassis Cab","Terrain","Terrain Denali","Yukon","Yukon XL","Yukon Hybrid","Yukon Denali","Yukon XL Denali","Yukon Denali Hybrid","GMC Multi-line","GMC Brand","CPO Brand","Avalanche","Camaro","Camaro Convertible","Camaro Coupe","Camaro ZL1 Convertible","Camaro ZL1 Coupe","Colorado","Corvette","Corvette 427","Corvette Convertible","Corvette Coupe","Corvette Grand Sport Convertible","Corvette Grand Sport Coupe","Corvette Z06","Corvette ZR1","Corvette Stingray","Cruze","Equinox","Express","Impala","Malibu","Silverado 1500","Silverado 2500HD","Silverado 3500HD","Silverado HD","Silverado Hybrid","Sonic Hatchback","Sonic Sedan","Spark","Suburban","CTS Wagon","CTS-V Wagon","FCO Brand","GM Card Brand","OnStar Brand","OnStar Business Driver","VPP Brand","Chevy Certified Service","Buick Certified Service","GMC Certified Service","Cadillac Certified Service","My Certified Service","ACDelco","Chevy Performance","Genuine GM Parts","Alero","Intrigue","Powertrain","Finance & Insurance","Solstice","G5","Grand Am","Grand Prix","Sky","Ion","SUV","Car","Truck","GM Fules and Lubes","GM Brand","Global Brand","Chevrolet Global","Maven","FPOC Brand")
acceptableCreativeAgencies = set("Agency 720","Aimia","Carol H Williams","Casanova","Commonwealth","DAN Creative","Digitas","Fuisz Media","Gyro","Jack Morton","Isobar","Leo Burnett","Lowe CE","Martin Agency","Martin Retail","McCann","MRM","Publicis","Rogue","Spike","Cosette","Red Lion","Rokkan","Engage M1","One 10","Jack Morton","Cosette")


def checkCreativeName(creative):
    name = creative["name"]

    test = 0



for advertiser in advertiserSet:
    listvalues = {"searchString":"2018","active":True,"archived":False,"advertiserId":advertiser}
    creativeList = CreativeUtils.listCreatives(Api, listvalues)
    finalCreativeList.extend(creativeList)
    test =0 

for creative in finalCreativeList:
    checkCreativeName(creative)
test = 0
