# coding=utf-8
import multiprocessing
from modules.Placements import Placement
from modules.Ad import Ad
from modules.Creative import Creative
from modules.AsyncCampaign import AsyncCampaign
from modules.Sites import Sites

array = []
MasterSiteList = {'1375554': 'DO NOT USE»Vibrant Media', '1436933': 'Katz Media Group', '1372920': 'AMNET Canada', '1435512': 'Glam Media 2', '1345326': 'DO NOT USE»AutoTrader.com', '1880986': 'sportingnews.com', '1880941': 'Ebay, Inc – Ebay Enterprise', '1402373': 'Advance Internet', '1410347': 'DoubleClick, Inc.', '1716865': 'AUTOCOSMOS 1', '2374638': 'alphonso.tv', '1602540': 'Medio Tiempo', '1389767': 'Genesis Media', '2394407': 'lifeandstyle.mx', '1479913': 'Lapresse.ca', '1560869': 'Searchautoparts.com', '1419276': 'Glam Media Network', '1536978': 'Google Display Network 1', '1408719': 'Google Display Brand Performance', '1435565': 'discovery.ca', '1641969': 'Shazam', '2734236': 'as.com/mexico', '1379017': 'Real Times Media – Who’s Who Publishing', '1392386': 'Louise Blouin Media – ArtInfo', '1379000': 'US News & World Report LP', '2293625': 'DART Search : MSN : 23263', '2556452': 'Twitter - Official', '1603460': 'CNN Expansion', '1678021': 'Essence Online', '1410504': 'Vibrant Media Inc 2', '2109587': 'El Universal Mexico', '1401178': 'Refinery29.com', '1373002': 'DO NOT USE»*******test45****do not use***', '2127777': 'teads.tv', '1716867': 'Es Mas 2', '1567789': 'V Tele', '1663294': 'Facebook Inc 2', '1389754': 'Glam Media 1', '1420289': 'bing.ca', '2018811': 'instagram.com', '1440474': 'Radio Canada', '1372913': 'AOL - Advertising (Publisher) 1', '2029801': 'Contempo Media, Inc – Sharp Magazine (Canada)', '1604442': 'Publimetro MX', '1562048': 'http://colleges.niche.com', '2068064': 'MTV Latino CO', '1567636': 'Newad FR', '1393512': 'Patch.com', '2703118': 'Adometry, Inc.', '1663868': 'GoGo Network 1', '1372990': 'Msn.ca', '1481580': 'Instructables.com', '2571211': 'dailyfrontrow.com', '2394406': 'revistacodigo.com', '1479522': 'Wired.com', '1379052': 'Casale Media', '2103144': 'Navysports.com', '2518729': 'The FADER', '2354833': 'Redmas', '1360193': 'Autobytel Network', '1533433': 'Digilant', '1476590': 'AOL', '1401180': 'PGATOUR.COM', '2038646': 'We Are The Mighty', '2018629': 'National Hot Rod Association', '1684229': 'scrippsnetworksinteractive.com', '2425109': 'DO NOT USE»Warner Bros. Online', '1861165': 'Quartz', '2661566': 'blacktomato.com', '1575824': 'Salon.com 1', '2067849': 'aquto.com', '1575826': 'Largetail LLC 1', '1375900': 'Google Search_', '1372086': 'Glam Canada', '1481590': 'MLS (Major League Soccer)', '1479417': 'showcase.ca', '2699651': 'DO NOT USE»**testing - not for use**', '1345469': 'Twitter', '2431362': 'In Style', '2030699': 'Autoproyecto', '1591277': 'Eyeview, Inc', '1968508': 'Architzer LLC', '1440460': 'Time, Inc - RealSimple', '1892155': 'zemanta.com', '1960449': 'zemanta.com', '1388034': 'Univision', '1730019': 'mx.linkedin.com', '2563207': 'TrueX Media, Inc', '2151059': 'The Happening', '1576077': 'google.com.mx', '1678022': 'Essence Online', '1995889': 'Matador Ventures, Inc', '1551289': 'Twelvefold Media', '1389160': 'AccuWeather', '2401753': 'Invent', '1436932': 'CBS Interactive – CBS Radio', '1476693': 'SAY Media 1', '1688640': 'Gum Gum, Inc', '2169708': 'Speedway Benefits', '1737670': 'Power Automedia', '1496660': 'autofocus.ca 1', '1345437': 'DO NOT USE»Hearst Corporation - Jumpstart Automotive Media', '1387975': 'Trip Advisor', '1380756': 'Google Display Network', '2208979': 'Philo Broadcasting', '1596748': 'Cinepolis.com.mx', '1499753': 'The Los Angeles Sentinel', '1828201': 'tvasports.ca', '2394000': 'DO NOT USE»Jones Magazine', '2007220': 'InvestmentExecutive.com', '2431903': 'Michigan. com', '1403382': 'Praetorian Group', '1506827': 'Silver Chalice', '1663192': 'Facebook', '1435595': 'bell.ca', '1394235': 'Bright Roll 1', '1647779': 'Autoblog', '2353665': 'variety.com', '1488492': 'Farm Journal Media – AG Web', '1680176': 'Owner IQ', '1479508': 'Walt Disney Internet Group - ESPN Internet Ventures (ESPN Deportes)', '1656483': 'This Old House Ventures, Inc', '1360191': 'AOL - Advertising (Publisher)', '1480797': 'Duproprio', '1375549': 'ESPN', '1345438': 'DO NOT USE»Kelley Blue Book', '2331018': 'VICE Canada', '1505659': 'Live Nation Marketing, Inc', '1462486': 'Admob.com', '1476692': 'Complex', '1454738': 'Apple, Inc 1', '1694572': 'MX Esmas', '1542154': 'globealliance.org', '1668535': 'EbonyJet.com', '1568287': 'vtele.com', '1413834': 'Naylor, LLC', '1429045': 'Google 1', '1529427': 'Primedia Enthusiast Media DBA Source Interlink Media', '1596753': 'Playdom', '1549435': 'Tumblr', '1602562': 'El Financiero', '1375550': 'Federated Media', '1684238': 'Tend', '1435788': 'Atedra.com', '1524074': 'Videology 1', '1372967': 'TSN', '1479413': 'NewYorkTimes', '1676489': 'apco.ca', '1575839': 'Largetail LLC 2', '1423489': 'Hearst Corporation', '1581787': 'Answers.com 1', '1389769': 'WPP PLC - 24/7 Real Media, Inc', '1379044': 'Corus', '2245260': 'Digital Trends', '1547507': 'Commercial Truck Trader', '2728427': 'Kingdom Magazine', '2524533': 'DART Search : Google : 28401', '1449069': 'Urbanspoon', '2161137': 'smartclip.com', '1377168': 'cbc.ca', '1575819': 'Largetail LLC', '2445645': 'Spotify', '2726200': 'actitudfem.com', '1560872': 'Underhood Service', '1477795': 'Yahoo! Inc', '1377548': 'mediative.ca', '1380337': 'Travora Media Group', '1431260': 'GoldSpot Media Inc', '1407938': 'Evidon', '1457384': 'Spotxchange.com', '1541860': 'Experience Project', '1480790': 'Meteomedia.com FR', '1949577': 'Latina Media Ventures LLC', '1385004': 'A Gannett Company – USA Today', '1467701': 'Carlist.com', '1527540': 'DO NOT USE»AMNET', '1345470': 'AlphaBird - DONOTUSE', '2331019': 'Jumpstart Automotive Media', '1405094': 'Local Response, Inc', '1847141': 'Spongecell', '1401010': 'SF Chronicle', '1380888': 'JumpTap', '1481581': 'Randall-Reilly Publishing Co. LLC', '1405891': 'Quebecor Media Inc', '1654927': 'Fender Bender', '1601003': 'MX Reforma', '2409558': 'Fox sports', '1774808': 'rollingout.com', '1862752': 'Thrillist.com', '1714310': '4INFO, Inc', '1552769': 'NBC Universal - CNBC', '1865740': 'CounterMan', '1372327': 'Kelley Blue Book', '2028233': 'parksbynature.com', '1472145': 'Time, Inc – MNI Targeted Media, Inc', '1730053': 'Alto nivel', '1380891': 'National Geographic', '2418303': 'garuyo.com', '1694523': 'PACKERS.COM', '1533653': 'camaro5.com', '2003497': 'Heart and Soul', '1377711': 'Autotrader.ca EN', '1379051': 'Gorilla Nation', '1782667': 'Inadco, Inc', '1418575': 'UrbanDaddy', '1400969': 'The Big Ten Network', '2266361': 'Politico', '1601001': 'mediosmasivos.com.mx', '1550195': 'Weather.com US', '1440452': 'Meredith Corporation', '1666688': 'EbonyJet.com 1', '1533985': 'All Recipes', '2161932': 'TeadsImpact.com', '1404495': 'youtube.ca', '1394237': 'CNN  Network', '1376494': 'The NBC Sports Group - Comcast SportsNet Chicago LP', '1847124': 'Bing Travel', '2597706': 'TEADS', '1379046': 'farmmarketer.com', '1378991': 'Bloomberg.com', '2121146': 'Netsonic', '1400955': 'Complex Media Network', '1602533': 'StarMedia, Mexico', '1380336': 'Expedia', '1393518': 'Entrepreneur Media, Inc - Entrepreneur.com', '1345456': 'DO NOT USE»SIM Automotive Group', '2662442': 'goop.com', '1482216': 'Lighthouse Media Solutions', '1737491': 'NHRARACER.com', '2745566': 'Mercado Libre', '1375861': 'AOL - Advertising (Publisher)_', '1389084': 'GrooveShark', '1345446': 'Walt Disney Internet Group - ESPN Internet Ventures', '1418576': 'Visible Measures Corp', '1432622': 'Time Inc. Network', '1665886': 'thunderclap.it/en', '1716568': 'eikondigital.com 2', '2569259': 'fatherly.com', '2393800': 'Guardian NWS & Media', '1381301': 'Total Traffic Network (formerly Metro Networks)', '2397607': 'Travesias', '1345324': 'DO NOT USE»Autobytel Network', '1651656': 'longhornlifeonline.com', '1401218': 'theloop.ca', '1386870': 'Millennial Media.com', '1518241': 'Evolve Media, LLC – CraveOnline Media', '1488597': 'Expedia Media Solutions', '1372915': '51test.com', '1637108': 'militarytimes.com', '1379001': 'Pandora', '2209705': 'Media Planet', '1392176': 'Premiere Radio Networks', '1475265': 'ValueClick Mobile, Inc. (f/k/a Greystripe, Inc.)', '1470362': 'Cricbuzz', '1345431': 'DO NOT USE»Classified Ventures, LLC - Cars.com', '1391027': 'Celtra', '2393801': 'Jones Magazine', '1601005': 'adsmovil.com', '1389231': 'Uniontrib.com - San Diego Union Tribune', '1377607': 'BBC Canada', '2227754': 'TIME.com', '2403315': 'Nickelodeon', '1378996': 'Disney Online', '1363433': 'GM Test Site', '1865505': 'Fox Broadcasting Network - Fox Television', '1411090': 'AARP', '1526923': 'thecomedynetwork.ca', '1379303': 'postmedia.ca', '1481587': 'Hispanic Business Inc', '1345445': 'DO NOT USE»Google - YouTube', '1385118': 'Advanstar Communications Inc.', '1437355': 'Yahoo! Inc – Genome From Yahoo', '1407713': 'QuantCast', '1601000': 'imagen.com.mx', '1647786': 'thedailybeast.com', '2037457': 'Gizmodo', '1440483': 'Voir.ca FR', '2501771': 'TED', '1472517': 'inpwrd.com', '1526012': 'The Atlantic Monthly', '1426811': 'Scripps Networks – Food Network', '1429616': 'AMC Network Entertainment, LLC – AMCTV', '1576078': 'bing.com 1', '1862722': 'TravelZoo', '2431364': 'Entertainment Weekly', '1606625': 'MX Tvazteca', '1372323': 'AutoTrader.com', '1436391': 'NY Times', '2403309': 'CNN Mexico 1', '1431786': 'Business Information Group', '2319356': 'AdMob Google Inc', '1861741': 'Vice Media Inc', '1615394': 'GQ (Mexico)', '1398790': 'OnTheSnow.com', '1547892': 'Amobee', '2171270': 'Do No Use_Speedway Benefits', '1716567': 'Cinepolis.com.mx 1', '1604439': 'Excelsior by IMS (newspaper)', '1489094': 'Hanley Wood', '1648503': 'MX Milenio', '2660752': 'Logan Media', '1694614': 'PACKERS.COM', '2406113': 'Twitter - Official', '1449192': 'Crain Communications Inc – AutoWeek Media Group 1', '1866942': 'EMS1.com', '1957086': 'US Weekly', '1372959': 'Loud Mouth Entertainment', '1500175': 'Mountain News Corporation', '1596747': 'MX bbmundo', '1596752': 'EnFemenino', '1581637': 'acuityads.com', '1598682': 'districtm.ca', '1418573': 'Protein Ltd', '1716558': 'www.hotwords.com.mx', '1566605': 'hollywoodreporter.com', '2097865': 'Florida Insider Fishing Report 1', '1371942': 'Scripps Networks_US', '1596749': 'eikondigital.com', '2067848': 'Kargo', '1394234': 'Bright Roll', '1581638': 'iqmedia.com', '1890153': 'adcolony.com', '1377725': 'yahoo.ca', '1526921': 'Sportsnet.ca', '2709854': 'Evolve Media LLC', '1740738': 'Ebuzzing, Inc', '1718265': 'levelup.com', '1483997': 'National Cable Communications, LLC (NCC Media)', '2618569': 'Racer.com', '1449269': 'CNN (AM)', '1492281': 'People', '1497554': 'Outbrain, Inc', '1377606': 'BrightRoll', '2457664': 'Twitter - Official', '1570952': 'bodyshopbusiness.com', '1526926': 'History Channel', '2395565': 'Time Out - USA', '1378114': 'The Weather Network EN', '1379009': 'spafax.com', '2513255': 'DART Search : Google : 28435', '1560955': 'Searchautoparts.com 1', '1603272': 'elnorte.com', '1392956': 'The New York Times Company - NYTimes.com', '2399450': 'Ncm.com', '1606201': 'mx.hola.com', '1472518': 'Ziff Davis Media Network', '1381294': 'QuadrantONE', '2617019': 'outlook.com', '1914003': 'thinknear.com', '1695307': 'IMG Worldwide, Inc – IMG College', '1681141': 'Magnetic Media Online', '1684120': 'scrippsnetworksinteractive.com', '1401210': 'tctranscontinental.com', '1714599': 'exelsior.com', '1722742': 'Manta Media Inc', '2316421': 'Televisa.com', '1375561': 'BBC', '1481576': 'aghubmedia.com', '1379262': 'Sister 2 Sister Magazine', '1404498': 'Suite 66', '1377167': 'CTV.ca', '1882703': 'AddThis, Inc', '1782653': 'EPMG', '2397804': 'Condé Nast Digital – Vanity Fair', '1684612': 'wxyz.com', '1600438': 'Social Moms', '1666706': 'EbonyJet.com', '1481589': 'ImpreMedia', '1714322': 'New York Comic Con', '1866943': 'FireRescue1.com', '1604443': 'MX ProdigyMSN', '2394435': 'Donde ir', '2164572': 'Forbes', '1454811': 'Pulpo Media', '1435076': 'Singtao', '2109586': 'ESPN', '1526852': 'OnCampus Advertising', '1423490': 'Hearst Corporation – Esquire Magazine', '2593718': 'Hotbook', '1393519': 'Mansueto Ventures, LLC - Inc.com', '1504495': 'Millward Brown - Dynamic Logic', '1500527': 'Shoptopia', '1603461': 'Televisa : Esmas.com', '1552768': 'Samsung AdHub', '2038613': 'Gilt Groupe', '2556449': 'Twitter - Official', '1560870': 'Brake & Front End', '1452010': 'greystripe.com', '2593717': 'admexico.mx', '1345439': 'Microsoft Online Inc - MSN.com', '1440714': 'NPR Online', '1463844': 'YouTube.com', '1568290': 'Diagnostic News', '2671821': 'Facebook.com', '2035200': 'kiwilimon.com', '1372324': 'Classified Ventures, LLC - Cars.com', '1451575': 'Minority Business Entrepreneur Magazine', '1545693': 'BrightLine Partners', '1431657': 'AdMob Google Inc. [Use only for RM]', '1385011': 'Yelp, Inc', '1529130': 'Who What Wear', '2501300': 'BidManager_DfaSite_516600', '1385010': 'Weather Channel', '2688201': 'AudioAd', '1560867': 'Autocarepronews.com', '1575813': 'Coolhunting.com', '1684844': 'Mode Media', '1345444': 'DO NOT USE»Amnet Group Inc.', '2021058': 'Orange', '2215916': 'soundcloud.com', '1634361': 'MapMyFitness, Inc', '1648510': 'redpineapplemedia.com', '1985220': 'Condé Nast Digital – GQ Magazine', '1693327': 'Soccer United Marketing', '2473203': 'DBM Aegis Media 1019774624-GM_Chevy_Global', '2364948': 'RobbReport.com', '1431784': 'junewarren-nickles.com', '1377753': 'autonet.ca', '1375562': 'Conde Nast – Wired', '1371921': 'Scripps Networks', '1454914': 'CraveOnline', '1389080': 'DO NOT USE»VEVO', '1914805': 'iheart.com', '1582384': 'about.com', '2526750': 'CBS Interactive – CBS News', '1479386': 'CTV News EN', '1828614': 'BON APPETITE', '1479520': 'TopGear', '1716637': 'orange.com', '1601002': 'azteca.com', '1515523': 'buzzfeed.com', '1703911': 'publicationsports.com', '1415268': 'MLB Advanced Media', '1401182': 'canoe.ca', '1481584': 'worldfishingnetwork.com', '1771923': 'Yahoo Ad Manager', '1782687': 'Bravo', '1596750': 'mundonick.com', '1375899': 'Twitter_', '1372326': 'DO NOT USE»Amnet Group Inc.', '1526011': 'Tasting Table', '1375555': 'Yahoo! Inc. (Network Plus-Preemptible)', '2524138': 'DART Search : Yahoo! Gemini : 23263', '1568299': 'Diagnostic New', '2396807': 'gatopardo.com', '1828601': 'Futbol Total MX', '1614221': 'travelandleisure.com 1', '1440349': 'NBC Universal – Telemundo', '2553618': 'Match Media Group, LLC - OKCupid', '1694944': 'glamout.com.mx', '1717267': 'exelsior.com 1', '1379373': 'Walt Disney Internet Group - ESPN Internet Ventures (ESPN Radio)', '1676491': 'apco.ca', '1378113': 'Totally Her', '1568307': 'RocketFuel, Inc 1', '1716561': 'Es Mas', '1479518': 'Protein Ltd 1', '1412648': 'Wow Media Products, Inc', '1827810': 'MX Metroscubicos', '2067800': 'GasBuddy.com', '1360203': 'DO NOT USE»AutoTrader.com', '1603270': 'record.com.mx', '1345462': 'Google Search', '1377760': 'Driving.ca', '1604056': 'Adara Media, Inc.', '1545676': 'Synacor, Inc', '2077535': 'YuMe', '1473319': 'Fast Company', '1440687': 'Facebook Inc', '1512540': 'Nativo', '1614217': 'redmas.com', '2537319': 'snapchat.com', '2401207': 'Carat Programmatic', '1512120': 'FoxSports.com', '2699725': 'autobild', '1376611': 'Time Inc', '1376120': 'Triad Retail Media – eBay', '1596898': 'televisa.com.mx', '1345447': 'DO NOT USE»NFL Enterprises LLC - NFL.com', '2700043': 'DART Search : Google : 28400', '2319080': 'CanalMail', '2393600': 'MIC Network, Inc', '1647791': 'Eater', '1568309': 'Exchange Lab', '1454615': 'Cleveland Plain Dealer', '1735991': 'Cuse.com', '1375858': '140 Proof_', '1405358': 'Linkedin 1', '1534798': 'GQ Magazine Video', '1380338': 'Millennial Media', '1548038': 'Medula LLC', '1449270': 'NBA.com', '1509234': 'WFAA (ABC)', '1385007': 'RocketFuel, Inc', '1704721': 'BellMedia.ca', '1466389': 'Toronto Star', '1573596': 'twitter.com', '1782295': 'EPMG', '1431715': 'Buzz Media', '1575838': 'Salon.com 2', '1969305': 'Architzer LLC', '1435566': 'HGTV EN', '1416878': 'ABC National Television Sales', '2319018': 'Cultura colectiva', '1372325': 'Edmunds.com, Inc', '1512664': 'EA Network', '1595451': 'TubeMogul 1', '2701818': 'MX Batanga', '1377828': 'Outdoor Hub', '1389162': 'WeatherBug', '1377599': 'Vibrant Media Inc 1', '2121185': 'DO NOT USE»BABE WINKELMAN', '1865742': 'PoliceOne.com', '1440513': 'Bankrate, Inc', '2648508': 'The Taunton Press Inc.', '1731375': 'MX El Financiero', '1614220': 'travelandleisure.com', '2319419': 'unocero.com', '1463138': 'Sports Illustrated/SI.com', '2127157': 'Vogue', '1506260': 'Verve Wireless, Inc – Verve Mobile', '1561255': 'Niche Media Holdings, LLC', '2443804': 'redwings.nhl.com', '1608913': 'demotores.com.mx', '1415362': 'Prometheus Global Media LLC - Billboard Online', '1435563': 'A&E Television Networks LLC – History Channel Online', '1379058': 'TheScore.ca EN', '1740578': 'clearstream.tv', '1373643': 'Microsoft Online Inc. (MSN.com Network)', '1537625': 'estrellatv.com', '1410384': 'LA Times', '1647790': 'Vox Media, Inc – SBNation', '2709502': 'Crackle.com', '1345453': 'Hulu.com', '1596899': 'Quién (Mexico)', '1647781': 'menshealth.com', '1984002': 'm.yume.com', '2670618': 'elgourmet.com', '1345440': 'DO NOT USE»Yahoo! Inc. (Display)', '1398953': 'Texas Fish & Game, LLC', '2149071': 'live.xbox.com', '1379056': 'ESPNNewYork.com', '1808843': '8tracks. Inc', '1525980': 'owneriq.com', '1534797': 'Condé Nast Digital – GQ Magazine', '1762408': 'Swoop', '1679563': 'BlogHer Network', '1600998': 'CNNenEspanol.com', '2593111': 'Canal Mail', '1345426': 'Crain Communications Inc – AutoWeek Media Group', '1600999': 'AUTOCOSMOS', '1411036': 'Terra Networks USA 1', '1688639': 'Gum Gum, Inc', '2746127': 'Networld Media Group', '1850411': 'AMNET', '1434281': 'DriverSide Inc.', '2123144': 'skype.com', '2103764': 'Buzzfeed', '1480701': 'Viacom International Inc', '1411035': 'Terra Networks USA', '1387863': 'Time Inc - CNNMoney', '1435584': 'AUTO123 FR', '1665477': 'GoGo Network', '1602701': 'Headway Digital - Masaryk.tv', '1614454': 'Condé Nast Digital – Glamour (Mexico)', '1377603': 'Google', '1730055': 'imscorporate.com', '1436242': 'Autoguide.com', '1378378': 'Astral EN', '1377596': 'SAY Media', '1345464': '140 Proof', '1486330': 'NFIB', '1376528': 'Goodway Group', '1561254': 'Are You a Human', '1507036': 'ufc.ca', '1386977': 'Batanga Network', '1385005': 'Bonnier Active Media, Inc', '1526009': 'InsideHook', '1481579': 'Hearst Corporation – Popular Mechanics', '1400184': 'Specific Media', '1608914': 'exponential.com', '2290508': 'Maxim.com', '2210690': 'theshadowleague.com', '1724870': 'MX Mtvla', '1390019': 'MaxPoint', '1959205': 'enginebuildermag.com\u200b', '1440953': 'Expedia 1', '1407697': 'Goldspot', '1536979': 'AOL Canada', '1481577': 'Agriculture Online', '1530278': 'Vimeo', '1405800': 'Tribecafilmfestival.org', '1375193': 'Walt Disney Internet Group - ESPN Internet Ventures 1', '1389672': 'Washington Post Digital', '1513126': 'nbcmiami.com', '2246025': 'DO NOT USE»Digital Trends', '1391346': 'Tribalfusion', '1404146': 'Hearst Corporation - Motor Magazine', '1415208': 'autohebdo.net', '1549461': 'Tumblr 1', '1386980': 'The Mundial Group, Inc – Mundial Sports Network', '1716662': 'MX Autoplaza 1', '1794543': 'Tumblr', '1345435': 'DO NOT USE»Edmunds.com, Inc', '1372329': 'Microsoft Online Inc - MSN.com 1', '1408681': 'NBC Universal', '1496659': 'autofocus.ca', '2582120': 'Nativ.ly', '1739939': 'mural.com', '1435564': 'cbc.ca/news/business', '1861164': 'Gawker Media', '2398704': 'Outrigger Media', '2425110': 'Warner Bros. Online', '1790517': 'dondeir.com', '1380223': 'ColbertNation.com', '2406162': 'Style Caster', '1604444': 'MX ProdigyMSN 1', '1385009': 'Time Inc Network – People.com', '2552601': '1Motorsport', '2275236': 'VOLTA INDUSTRIES, IN', '1378993': 'NetShelter, Inc.', '1846500': 'Outbrain, Inc', '2068078': 'es.yahoo.com', '1440937': 'PopSugar Media – Sugar Inc', '1717268': 'Publimetro MX 1', '1389502': 'Adconion', '1438962': 'Black Entertainment Television – BET Interactive LLC', '2511231': 'demandbase.com', '1576249': 'Tele-Quebec FR', '1435596': 'Fuel Media', '1386979': 'Microsoft Online Inc - MSN Latino', '1372937': 'Google - YouTube 1', '1808811': 'vessel', '1382350': 'Martha Stewart Living Omnimedia', '1476470': 'DoubleClick', '2556455': 'Twitter - Official', '1367621': 'A&E Television Networks LLC – Lifetime Entertainment Services (myLifetime)', '1378992': 'CafeMom', '1439916': 'Facebook.com', '1379655': 'HotChalk', '1547940': 'University of Texas at Austin', '1714166': 'xAd', '2703700': 'hometeamsports.com', '1860913': 'Eleconomista.com.mx', '1977521': 'esmas.com', '1405819': 'ESPN Dallas', '1722861': 'UConnHuskies', '1387860': 'Active Network', '1502839': 'RGM Alliance', '1472590': 'AOL - Advertising (Publisher) 2', '1820020': 'ShareThis, Inc', '1393821': 'Giant Media', '1377757': 'Kijiji', '1345312': 'DO NOT USE»AOL - Advertising (Publisher)', '1391864': 'ChicagoTribune Interactive or Tribune Interactive', '1847352': 'Spongecell', '2219123': 'Fullscreen, Inc 1', '1647783': 'Racked', '1411007': 'Texas Monthly', '1612337': 'Luminar', '1647778': 'Afar Media, LLC', '2529203': 'demandbase.com', '1801197': 'Newspaper National Network', '1481586': 'Goal.com', '2395564': 'rodaleinc.com', '1479374': 'Andrew John Publishing Inc.', '1408685': 'Walt Disney Internet Group - ABC.com', '1431719': 'Astral Media', '1374175': 'MaxPoint Interactive', '2556450': 'Twitter - Official', '1408680': 'Hulu.com 1', '1435130': 'Break.com', '1526010': 'Pulse', '1389751': 'Glam Media', '1378930': 'Conde Nast', '1389768': 'ValueClick Media', '1408682': 'ABC.com', '1375557': 'Apple, Inc', '1453329': 'Tribune Interactive – Chicago Tribune', '1376935': 'Hearst Corporation - Jumpstart Automotive Media', '2555230': 'DART Search : Other', '1527681': 'Johnson Publishing Company, LLC – Ebony', '1385119': 'Babcox Publishing LLC', '1647782': 'Motor Trend Online', '1415202': 'AutoSphere Canada', '1507525': 'qmiagency.ca', '1637109': 'Military.com', '2745768': 'MobileFuse', '1409435': 'ESPN LA', '1866540': 'PennWell Network', '1391045': 'Viacom International Inc MTV Networks', '1389749': 'cuedigitalmedia.com', '2367925': 'Linkedin', '1381293': 'Centro', '1399626': 'tubemogul.com/company/about_us', '1481583': 'Turner Sports and Entertainment Network – Nascar.com', '2293832': 'DART Search : Google : 23263', '1435077': 'Komli', '2519724': 'VEVO', '2316420': 'Grupo Radio Centro', '1411317': 'juicemobile.ca', '1504715': 'Jumpstart Digital Marketing', '1472594': 'Opera Software – Mobile Theory', '1593242': 'Manchester United Official website 1', '2029515': 'espanol.yahoo.com', '2288594': 'Opera Mediaworks', '2593903': 'Pitchfork Media Inc.', '1431283': 'Bloomberg Businessweek Online', '2443853': 'Media IQ', '1376491': 'Bobit Business Media', '1380754': 'LinkedIn Corporation', '1665479': 'thunderclap.it/en 1', '2209737': 'CBS Local', '1440053': 'nbclosangeles.com', '2216548': 'Conversant, Inc', '1481435': 'Collective Media', '1647787': 'The Week Magazine', '1518998': 'The CW Television Network', '1449287': 'NBC Universal - NBC Sports', '2246486': 'Canal Mail Email', '1541861': 'Experience Project 1', '1440950': 'American Express Publishing - Food & Wine', '1476591': 'theweathernetwork.com', '2484723': 'Telenav, Inc', '1415192': 'American Express Publishing', '1375556': 'CBS Interactive - CBS Sports', '1373723': 'NFL Enterprises LLC - NFL.com', '1456453': 'korrelate.com', '1367571': 'Microsoft Online, Inc (MSN.FoxSports)', '1977501': 'AMNET mobile', '1500524': 'Uptown Ventures Group – Uptown Magazine', '2398752': 'Spotify', '1479517': 'GQ', '1411394': 'Canadian Black Book', '1509678': 'Orange County Register', '1790503': 'TrailerLife', '1389778': 'Microsoft Advertising', '1882257': 'groupeserdy.com', '1525390': 'The Weather Channel', '1596745': 'MX Terra', '1703408': 'und.com', '1479515': 'Condé Nast Digital - Details', '1596751': 'hotwords.com', '1647785': 'Snooth', '1602542': 'appsnack.com', '1380889': 'Martini Media Network', '2417304': 'ratchetandwrench.com', '1575812': 'Salon.com', '2384334': 'Efficient Mobile', '1481582': 'RealTree', '1539629': 'powerTV Media, LLC', '1519945': 'BrightRoll 1', '1404324': 'Gannett LTD', '1375558': 'Bleacher Report', '1401190': 'Linkedin', '2300387': 'Mitu Network', '1676960': 'Mirror Digital, Inc', '1927724': 'Hola', '1377744': 'Auto 123', '1600672': 'Marvel', '1411315': 'Addictive Mobility', '1676761': 'Discovery.com', '1681147': 'Adconion', '2710130': 'Waze, Inc', '1716597': 'Fullscreen, Inc', '1614218': 'impaktu.com', '1602529': 'Deezer', '1561536': 'AddThis, Inc', '1425787': 'Luxury Link LLC – Luxury Link', '1716658': 'eikondigital.com 1', '1373001': 'Yahoo! Inc. (Display)', '1389052': 'AutoTrader.com Access', '1377598': 'oboxmedia.com', '1379055': 'ESPNBoston.com', '2118397': 'Yahoo! Gemini', '1894410': 'ferriz.com.mx', '1440486': 'RDS', '1866944': 'PoliceOne.com', '1648509': 'forbes.com.mx/sites', '2556451': 'Twitter - Official', '1611436': 'excelsior.com.mx', '1392390': 'Chicago Sun Times', '1572250': 'Rogers Digital Media (Canada)', '1345450': 'Vibrant Media Inc', '1513124': 'NBC New York', '1377169': 'shawmedia.ca', '1440959': 'The Wall Street Journal', '2127776': 'teads.tv', '2709339': '#Paid', '1995709': 'Lopez Doriga', '1603271': 'Quiminet', '1526629': 'jumpstart.ca', '2319452': 'El Pais', '2523133': 'UnrulyMedia', '1382607': 'Globeand Mail', '1413144': 'Comscore, Inc', '1649144': 'Fortune.com', '1435562': 'BNN.CA', '1528428': 'Detroit Media Partnership', '2284582': 'Ad Marketplace', '1676962': 'Juan Futbol', '2545345': 'Antevenio', '2331804': 'EstiloDF', '1602535': 'Spotify', '1481578': 'Cygnus Business Media', '1478941': 'okramedia.com', '1430510': 'Nymag.com_', '1439815': 'Emmis Publishing, LP – LA Magazine', '1814223': 'ebay.com', '1504494': 'Sports Media Ventures, Inc.', '1999092': 'AdoTube', '1688342': 'NEA', '1592393': 'Manchester United Official website', '1760520': 'TakePart', '1452149': 'The Wall Street Journal Online', '2219119': 'Fullscreen, Inc', '1680080': 'adconian.com', '1846959': "Bob Redfern's Outdoor Magazine", '1813819': 'PayPal', '1470360': 'CricInfo', '1501082': 'WFAA', '2123107': 'BABE WINKELMAN 1', '1389766': 'AlphaBird', '1606828': 'Songza Media, Inc', '1453618': 'The Root', '1372979': 'Rogers Digital Media', '1527786': 'Tapjoy', '1401196': 'St. Joseph Media', '1995692': 'Matador Ventures, Inc 1', '1900906': 'zombiecorp.com', '1561251': 'AutoTrader', '1379048': 'Owner IQ', '1405605': 'CBS Television Stations', '1520847': 'Scripps Networks – HGTV', '2396806': 'Hyper Animals', '2141134': 'Curbed.com, LLC', '1716559': 'grupoacir.com.mx 1', '1658232': 'jornada.unam.mx', '1481574': '24/7 Real Media', '2062620': 'autos.demotores.com.mx', '1476902': 'Dataxu', '2039430': 'We Are The Mighty', '1380890': 'Millennial Media 1', '1600997': 'grupoacir.com.mx', '2708344': 'eHOW', '1526918': 'NFL Internet Group', '1379049': 'VerticalScope Inc.', '1420290': 'Google Canada', '1372914': 'YuMe', '1602658': 'PennWell Corporation', '1378712': 'CBS Interactive', '1614451': 'Disney Latino', '1378995': 'Turner Network – CNN.com', '1375863': 'bing.com_', '2706145': 'snapchat.com', '1712899': '4INFO, Inc', '1372986': 'Sympatico Canada', '1676762': 'Mirror Digital, Inc', '1345461': 'bing.com', '1386978': 'Es Mas', '1375551': 'Kontera Technologies', '1425786': 'CBS Interactive - CNET', '1534396': 'Internet Brands', '1694946': 'US media Consulting', '1861166': 'Vogue', '1479973': 'tcmedia.ca', '1435567': 'Score Golf', '2259437': 'roku.com', '1387004': 'Zillow Inc', '1399625': 'TubeMogul', '2515234': 'DART Search : MSN : 28435', '1604441': 'headwaydigital.com', '1592375': 'Burst Media', '2370919': 'CNN Mexico', '1615395': 'MasarykTV', '1547709': 'Collective Digital Studio, LLC', '1449232': 'Vox Media, Inc', '1377665': 'Madison Square Garden Media', '1602536': 'MX Chilango', '2369521': 'theSkimm', '1507032': 'postmedia.com', '1384187': 'Clear Channel Media & Entertainment', '1479519': 'Protein Ltd 2', '1375552': 'Slate', '1602543': 'Es Mas 1', '1439648': 'OWN, LLC – Oprah.com', '1606199': 'mexico.cnn.com', '2149105': 'wobi.com', '1441184': 'b101radio.com', '1684138': 'Mode Media', '1602541': 'adman.com', '1664009': 'MTVLA.COM', '1387861': 'Demand Media', '1440956': 'Interactive One, A  Radio One Co', '2447279': 'Mode Media', '1381304': 'Tribune Interactive Markets', '2556454': 'Twitter - Official', '1608879': 'Trulia, Inc.', '1660454': 'ZEFR', '1680384': 'pinterest.com', '1545113': 'Genesis Media 1', '2096926': 'HSM', '1624537': 'MX Autoplaza', '1534397': 'Internet Brands 1', '1601004': 'Quién (Mexico) 1', '1891206': 'NHL.com', '1710385': 'enfilme.com', '1556954': 'placeiq.com', '2097474': 'DO NOT USE»Florida Insider Fishing Report', '2217204': 'dtravelconnection.com', '1540483': 'Notre Dame Sports Properties', '1381363': 'vibrantmedia.com', '2445427': 'Lotlinx', '1391339': 'Cineplex', '1815017': 'PayPal', '1482246': 'nhl.com/fr', '1536041': 'Strategic Value Media', '1394239': 'Tremor Video', '1881414': 'sportingnews.com', '1694613': 'webzodes.com', '2709465': 'CMA', '1614340': 'Outside Online', '1391384': 'CFBF.com', '1581788': 'About, Inc.', '1380886': 'AdGent Digital', '1387862': 'Liberty Advertising – Evite', '1380887': 'InterActiveCorp (IAC) – CityGrid Media', '1389671': 'FlightAware', '1716862': 'terra.com.mx', '1785420': 'Mybestoption.it', '2454119': 'Twitter - Official (NEW)', '1415335': 'Compete', '1936150': 'Terra', '1596754': 'marvel.la', '2556453': 'Twitter - Official', '1377759': 'Wheels.ca', '1995693': 'Matador Ventures, Inc', '1394238': 'Rhythm New Media, Inc', '1592370': 'thegazette.com', '1372322': 'AOL - Advertising', '1663749': 'tripadvisor.com', '1375915': 'Google - YouTube_', '1722430': 'StumbleUpon, Inc', '1602703': 'El Universal MX', '1449265': 'Chow.com', '2627626': 'CarGurus, LLC', '1382613': 'Microsoft Online, Inc - MSN Network', '1504513': 'People En Espanol', '1407690': 'Undertone Networks', '1393822': 'Jun Group Productions LLC', '1676490': 'Discovery.com', '1604440': 'skype.com/es', '1691811': 'Research Now', '1566703': 'Hollywood Reporter', '1481575': 'A&E Television Networks LLC – A&E Online', '1435587': 'Force Radio', '1647788': 'trendland.net', '1405123': 'Mashable', '1418568': 'GearPatrol', '1513526': 'Break Media', '1865741': 'ImportCar', '1415200': 'fleetbusiness.com', '1374273': 'Here Media Network', '2309585': 'RMEF', '1881308': 'Samba TV', '1404728': 'Bizo', '1377594': 'Olive Media', '1440506': 'The Huffington Post', '1378379': 'Crucial Interactive EN', '1729982': 'Adsmovil.com', '1423795': 'skype.com', '1378994': 'She Knows', '1525389': 'Active Interest Media', '1376645': 'Turner Sports and Entertainment Network', '1666638': 'thunderclap.it/en', '1387532': 'CottageLife.com EN', '1345457': 'DO NOT USE»Weather Channel', '1483299': "Men's Journal.com", '1379047': 'Tribal Fusion EN', '2071026': 'Prodigy MSN', '1494638': 'Solve Media', '1523724': 'Tapad, Inc', '1602702': 'Yahoo', '1407730': 'AdMob Google Inc', '1372330': 'SIM Automotive Group', '1606207': 'MX Mediotiempo', '1481437': 'Sharethrough', '1556938': 'Facebook Inc 1', '1710484': 'Invite Media', '1740739': 'Onion Inc', '1534398': 'Internet Brands 2', '1372941': 'Videology', '1435181': 'Monster Worldwide', '1740286': 'plus.lapresse.ca', '1581786': 'Answers.com', '1663695': 'Delta.com', '1716861': 'Grupo Expansion – CNN Expansion (Mexico)', '1376608': 'Amazon Media Group LLC.', '1376944': 'Google - YouTube', '1979134': 'whosay.com'}
MasterAdList = {}
MasterCreativeList = {}
def secondsToHours(seconds):
        import math
        seconds = math.floor(seconds)
        minutes = math.floor(seconds/60)
        hours = 0
        plural = "s"
        minuteString = "minute"
        hourString = "hours"
        while minutes > 60:
            hours += 1
            minutes -= 60
        if hours > 1:
            hourString = hourString + plural
        if minutes > 1:
            minuteString = minuteString + plural
        return "{0} {1} and {2} {3}".format(hours, hourString, minutes, minuteString)
def TrueToYes(boolean):
    if boolean == True:
        return "Yes"
    else:
        return "No"
    
def formatDateTime(datetimeString):
    import datetime
    date = datetimeString.split('T')[0]
    time = datetimeString.split('T')[1]
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = int(date.split('-')[2])
    date = datetime.date(year,month,day)
    date = date.strftime("%m/%d/%y")
    hour = int(time.split(':')[0])
    minute = int(time.split(':')[1])
    time = datetime.time(hour,minute)
    time = time.strftime("%I:%M %p")
    return (date + " " +  time)
    
def checkSession(session, initialSession):
    if initialSession != session:
        return session
    else:
        return initialSession
        
def analyzeCampaignList(campaignList, process, queue, p1Num, p2Num):
    import datetime
    campaignObject = AsyncCampaign(20124958)
    initialSession = campaignObject.session
    initialEventLoop = campaignObject.eventLoop
    rowArray = []
    length = len(campaignList)
    print(length)
    if process == "One":
        campaignRange = range(0,length,1)
        step = 1
        number = p1Num
    else:
        campaignRange = range(length - 1,0,-1)
        step = -1
        number = p2Num
    length = len(campaignList)
    for campaign in campaignRange:
        print("analyzing campaign {2} out of {3}: {0} Process:{1}".format(campaignList[campaign]["name"], process, campaign + 1, length))
        number.value += step
        print("P1 = {0}, P2 = {1}".format(p1Num.value, p2Num.value))
        if p1Num.value > p2Num.value:
            print("Process: {0} exiting".format(process))
            queue.put(rowArray)
            return
        campaignBody = AsyncCampaign(campaignList[campaign]["id"], initialEventLoop, initialSession).getPlacementList()
        initialSession = checkSession(campaignBody.session, initialSession)
        for placementObject in campaignBody.placements:
            placement = Placement(placementObject["id"], initialEventLoop, initialSession).getAdList()
            response = [x for x in placement.ads if "Brand-neutral" not in x['name'] and "TRACKING" not in x["name"] and x["active"] == True and "AD_SERVING_DEFAULT_AD" not in x["type"]]
            placement.ads = [{"id":x["id"]} for x in response]
            initialSession = checkSession(placement.session, initialSession)
            if placement.body["siteId"] not in MasterSiteList:
                site = Sites(placement.body["siteId"], initialEventLoop, initialSession).body
                MasterSiteList[site["id"]] = site["name"]
            else:
                siteBody = {"id": placement.body["siteId"], "name":MasterSiteList[placement.body["siteId"]]}
                site = siteBody
                MasterSiteList[site["id"]] = site["name"]
            siteName = "{0} ({1})".format(site["name"], site["id"])
            for adBody in placement.ads:
                if adBody["id"] not in MasterAdList:
                    ad = Ad(adBody["id"],initialEventLoop, initialSession)
                    initialSession = checkSession(ad.session, initialSession)
                    MasterAdList[adBody["id"]] = ad
                else:
                    ad = MasterAdList[adBody["id"]]
                try:
                    hardCutoff = ad.body["deliverySchedule"]["hardCutoff"]
                except:
                    hardCutoff = True
                try:
                    creativeAssignments = ad.body["creativeRotation"]["creativeAssignments"]
                except:
                    pass
                for creative in creativeAssignments:
                    clickThroughURL = creative["clickThroughUrl"]["computedClickThroughUrl"]
                    creativeID = creative["creativeId"]
                    if creativeID not in MasterCreativeList:
                        creativeElement = Creative(creativeID,initialEventLoop, initialSession)
                        initialSession = checkSession(creativeElement.session, initialSession)
                        MasterCreativeList[creativeID] = creativeElement
                    else:
                        creativeElement = MasterCreativeList[creativeID]
                    creativeName = creativeElement.body["name"]
                    creativeType = creativeElement.body["type"]
                    adObject = {"Campaign Name": campaignBody.body['name']} 
                    adObject["Campaign ID"] = campaignBody.body["id"]
                    adObject["Site"] = siteName
                    adObject["Placement ID"] = placement.body["id"]
                    adObject["Placement Name"] = placement.body['name']
                    adObject["Start Date"] = placement.body["pricingSchedule"]["startDate"]
                    adObject["End Date"] = placement.body["pricingSchedule"]["endDate"]
                    adObject["Ad ID"] = ad.body['id']
                    adObject["Ad Name"] = ad.body['name'] 
                    adObject["Ad Type"] = ad.body["type"]
                    adObject["Ad is Active"] = TrueToYes(ad.body['active'])
                    adObject["Ad Start Time"] =formatDateTime(ad.body["startTime"])
                    adObject["Ad End Time"] =formatDateTime(ad.body["endTime"])
                    adObject["Hard Cut-Off"] = TrueToYes(hardCutoff)
                    adObject["Creative ID"] = creativeID
                    timestamp = int(creativeElement.body["lastModifiedInfo"]["time"]) / 1e3
                    adObject["Creative Date"] = datetime.datetime.fromtimestamp(timestamp).strftime('%m/%d/%y %I:%M %p')
                    adObject["Creative Name"] = creativeName
                    adObject["Creative Type"] = creativeType
                    adObject["Creative Click-Through URL"] = clickThroughURL
                    rowArray.append(adObject)
                    print("appending %s Process: %s" % (creativeID, process))

    
if __name__ == "__main__":
    import time
    start_time = time.time()

    campaignObject = AsyncCampaign(20124958)
    campaignList = [{"name":x["name"], "id":x["id"]} for x in campaignObject.getAllLMA().LMACampaigns if "2018" in x["name"]]
    p1Num  = multiprocessing.Value('i', 0)
    p2Num = multiprocessing.Value('i', len(campaignList))
    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=analyzeCampaignList, args=(campaignList,"One",q1, p1Num, p2Num))
    p2 = multiprocessing.Process(target=analyzeCampaignList, args=(campaignList,"Two",q2, p1Num, p2Num))
    p1.start()
    p2.start()
    q1arr = q1.get()
    q2arr = q2.get()
    array = q1arr + q2arr

    print("Finishing up!")
    p1.join()
    p2.join()
    import pandas as pd
    df = pd.DataFrame(data=array)
    df = df[['Campaign Name','Campaign ID','Site','Placement ID','Placement Name','Start Date','End Date','Ad ID','Ad Name','Ad Type','Ad is Active','Ad Start Time','Ad End Time','Hard Cut-Off','Creative ID','Creative Name','Creative Type','Creative Date','Creative Click-Through URL']]

    writer = pd.ExcelWriter('Full Report.xlsx',engine='xlsxwriter')
    workbook = writer.book
    headerObject = {"A1":"Campaign Name",
            "B1":"Campaign ID",
            "C1":"Site",
            "D1":"Placement ID", 
            "E1":"Placement Name", 
            "F1":"Start Date", 
            "G1":"End Date",
            "H1":"Ad Id",
            "I1":"Ad Name",
            "J1":"Ad Type",
            "K1":"Ad is Active",
            "L1":"Ad Start Time",
            "M1":"Ad End Time",
            "N1":"Hard Cut-Off",
            "O1":"Creative ID",
            "P1":"Creative Name",
            "Q1":"Creative Type",
            "R1":"Creative Date",
            "S1":"Creative Click-Through URL"}

    df.to_excel(writer, sheet_name ="Info", index = False)
    worksheet =  writer.sheets['Info']
    format1 =  workbook.add_format({'bg_color': '#0AADE9'})

    for obj in headerObject:
        worksheet.write(obj, headerObject[obj], format1) 

    writer.save()
    elapsed_time = secondsToHours(time.time() - start_time)
    print("Done!")
    import os
    import modules.send_mail as send_mail
    directories = os.listdir()
    reports = [x for x in directories if "Report" in x]
    for report in reports:
        send_mail.send_email(report, elapsed_time, recipients=["Lennon.Turner@amnetgroup.com","Kristine.Gillette@carat.com"])