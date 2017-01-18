import re
import requests
import json

# site
    # NAT=National
    # PYR=Pacific
    # PNR=Prairies
    # ONT=Ontario
    # QUE=Quebec
    # ATL=Atlantic
    # WUJ=Aldergrove (near Vancouver)
    # XPG=Prince George
    # XSS=Silver Star Mountain (near Vernon)
    # XSI=Victoria
    # XBE=Bethune (near Regina)
    # WHK=Carvel (near Edmonton)
    # XFW=Foxwarren (near Brandon)
    # WHN=Jimmy Lake (near Cold Lake)
    # XRA=Radisson (near Saskatoon)
    # XBU=Schuler (near Medicine Hat)
    # WWW=Spirit River (near Grande Prairie)
    # XSM=Strathmore (near Calgary)
    # XWL=Woodlands (near Winnipeg)
    # WBI=Britt (near Sudbury)
    # XDR=Dryden
    # WSO=Exeter (near London)
    # XFT=Franktown (near Ottawa)
    # WKR=King City (near Toronto)
    # WGJ=Montreal River (near Sault Ste. Marie)
    # XTI=Northeast Ontario (near Timmins)
    # XNI=Superior West (near Thunder Bay)
    # WMB=Lac Castor (near Saguenay)
    # XLA=Landrienne (near Rouyn-Noranda)
    # WMN=McGill (near Montréal)
    # XAM=Val d'Irène (near Mont-Joli)
    # WVY=Villeroy (near Trois-Rivières)
    # XNC=Chipman (near Fredericton)
    # XGO=Halifax
    # WTP=Holyrood (near St. John's)
    # XME=Marble Mountain (near Corner Brook)
    # XMB=Marion Bridge (near Sydney)
#year (2007-)
#month (1-12)
#day (1-31)
#hour (00-23)
#minute (00, 10, 20, 30, 40, 50)
# duration
   # 2=2 hours (1 image every 10 minutes)
   # 6=6 hours (1 image every 30 minutes)
   # 12=12 hours (1 image every hour)
# image_type
   # PRECIPET_SNOW_WEATHEROFFICE=PRECIP-ET - Snow (14 colours) - Default
   # PRECIPET_SNOW_A11Y_WEATHEROFFICE=PRECIP-ET - Snow (8 colours)
   # PRECIPET_RAIN_WEATHEROFFICE=PRECIP-ET - Rain (14 colours)
   # PRECIPET_RAIN_A11Y_WEATHEROFFICE=PRECIP-ET - Rain (8 colours)

SNOW14="PRECIPET_SNOW_WEATHEROFFICE"
SNOW8="PRECIPET_SNOW_A11Y_WEATHEROFFICE"
RAIN14="PRECIPET_RAIN_WEATHEROFFICE"
RAIN8="PRECIPET_RAIN_A11Y_WEATHEROFFICE"

def getArray(page, var):
    prog = re.compile(r"{} = \[([^\[]*),\s*\]".format(var))
    arr = prog.search(page)
    if not arr:
        return ""
    arr = arr.group(1)
    arr = arr.replace("'", '"')
    arr = "[" + arr + "]"
    arr = json.loads(arr)
    return arr    

def getImageList(site, year, month, day, hour, minute, duration, image_type):
    url = "http://climate.weather.gc.ca/radar/index_e.html"
    params = {site: site, year: year, month: month, day: day, hour: hour, minute: minute, duration: duration, image_type: image_type}    
    req = requests.get(url, params=params)
    req.raise_for_status()
    
    page = req.text
    animationInfo = getArray(page, "animationInfo")
    imageArray = getArray(page, "imageArray")
    blobArray = getArray(page, "blobArray")
    return animationInfo, imageArray, blobArray

def main():
    images = getImageList("NAT", 2017, 1, 1, 1, 10, 2, SNOW14)
    for i in images[2]:
        print(i)
    
if __name__ == "__main__":
    main()