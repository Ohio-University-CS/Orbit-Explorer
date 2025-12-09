from skyfield.api import load, N, S, E, W, Star, wgs84 #directions and World Geodetic system to compare latitude and longitude of viewer to comet right ascension and declinations (positions relative to center of gravity of the solar system)
from skyfield.data import mpc
from skyfield.constants import GM_SUN_Pitjeva_2005_km3_s2 as SUN_GRAV_CENT #center of gravity of the sun (not necessarily the center of the sun)
import datetime #used for dates
import sys #used for command line arguments
from datetime import date, timedelta #used to determine current day
from skyfield.almanac import find_discrete, risings_and_settings
from pytz import timezone #used for timezones
#from zoneinfo import ZoneInfo
with load.open(mpc.COMET_URL, reload = True) as minorplanetcentercometdata: #download and open comet history data, redownload if already found but it has been updated since last download
    cometdatas = mpc.load_comets_dataframe( minorplanetcentercometdata )

numarg = len(sys.argv) 

#if no latitude and longitude are specified, use the baker center coordinates
if numarg == 1:
    observerlatitude = 39.3249
    observerlongitude = -82.1017

#take user latitude and longitude as command line arguments
if numarg == 3 or numarg == 4:
    observerlatitude = sys.argv[1]
    observerlongitude = sys.argv[2]

observerloc = wgs84.latlon(observerlatitude,observerlongitude)

today = datetime.date.today()
begin = today
currentmonth = today.month
currentday = today.day
currentyear = today.year
timescale = load.timescale()
time = timescale.utc(currentyear, currentmonth, currentday)

#check from today through tomorrow, to allow for night viewing near midnight
enddate = begin + timedelta(days=1)

endmonth = enddate.month
endday = enddate.day
endyear = enddate.year

endtime = timescale.utc(endyear, endmonth, endday)

eph = load('de421.bsp')
sun, earth = eph['sun'], eph['earth']
#print('the data for', len( cometdatas ), 'comets have been loaded into the program') #print how many commets have been loaded

# use the last known location for each commet, indexed by designation
cometdatas = (cometdatas.sort_values('reference').groupby('designation', as_index=False).last().set_index('designation', drop=False))

"""
#have to work with comets separately as this point, so picking out ones observable from Earth now/soon
C2025A6 = cometdatas.loc['C/2025 A6 (Lemmon)']
print(C2025A6)
print()
currentcomet = sun + mpc.comet_orbit(C2025A6, timescale, SUN_GRAV_CENT)

rightascension, declination, distance = earth.at( time ).observe( currentcomet ).radec()
print( 'right ascension:', rightascension )
print( 'declination:', declination )
print()

C2O25K1 = cometdatas.loc['C/2025 K1 (ATLAS)']
print(C2O25K1)
print()
currentcomet = sun + mpc.comet_orbit(C2O25K1, timescale, SUN_GRAV_CENT)

rightascension, declination, distance = earth.at( time ).observe( currentcomet ).radec()
print( 'right ascension:', rightascension )
print( 'declination:', declination )
print()


threeIATLAS = cometdatas.loc['3I/ATLAS']
print(threeIATLAS)
print()
currentcomet = sun + mpc.comet_orbit(threeIATLAS, timescale, SUN_GRAV_CENT)

rightascension, declination, distance = earth.at( time ).observe( currentcomet ).radec()
print('right ascension:', rightascension)
print('declination:', declination)
print()

twentyfourpSchaumasse = cometdatas.loc['24P/Schaumasse']
print(twentyfourpSchaumasse)
print()
currentcomet = sun + mpc.comet_orbit(twentyfourpSchaumasse, timescale, SUN_GRAV_CENT)

rightascension, declination, distance = earth.at( time ).observe( currentcomet ).radec()
print('right ascension:', rightascension)
print('declination:', declination)
print()

C2024E1Wierzchos = cometdatas.loc['C/2024 E1 (Wierzchos)']
print(twentyfourpSchaumasse)
currentcomet = sun + mpc.comet_orbit(C2024E1Wierzchos, timescale, SUN_GRAV_CENT)

rightascension, declination, distance = earth.at( time ).observe( currentcomet ).radec()
print('right ascension:', rightascension)
print('declination:', declination)
print()

C2025R2SWAN = cometdatas.loc['C/2025 R2 (SWAN)']
print(C2025R2SWAN)
currentcomet = sun + mpc.comet_orbit(C2025R2SWAN, timescale, SUN_GRAV_CENT)

rightascension, declination, distance = earth.at( time ).observe( currentcomet ).radec()
print('right ascension:', rightascension)
print('declination:', declination)
print()

two40PNEAT = cometdatas.loc['240P/NEAT']
print(two40PNEAT)
currentcomet = sun + mpc.comet_orbit(two40PNEAT, timescale, SUN_GRAV_CENT)

rightascension, declination, distance = earth.at( time ).observe( currentcomet ).radec()
print('right ascension:', rightascension)
print('declination:', declination)
print()

C2025V1Borisov = cometdatas.loc['C/2025 V1 (Borisov)']
print(C2025V1Borisov)
currentcomet = sun + mpc.comet_orbit(C2025V1Borisov, timescale, SUN_GRAV_CENT)

rightascension, declination, distance = earth.at( time ).observe( currentcomet ).radec()
print('right ascension:', rightascension)
print('declination:', declination)
print()

P29SchwassWach = cometdatas.loc['29P/Schwassmann-Wachmann']
print(P29SchwassWach)
currentcomet = sun + mpc.comet_orbit(P29SchwassWach, timescale, SUN_GRAV_CENT)

rightascension, declination, distance = earth.at( time ).observe( currentcomet ).radec()
print('right ascension:', rightascension)
print('declination:', declination)
print()


ascsign, asch,ascm,ascs = rightascension.signed_hms(warn=True) #splits right ascension into sign, hours, minutes, seconds
decsign,decdeg, decmin, decsec = declination.signed_dms(warn=True) #splits declination into sign, degrees, minutes, seconds



#coordinates of the observer
#observerloc = wgs84.latlon(38.5725 * N, 109.54972238 * W)
# right ascension, declination, to see if the object is visible, use the star calculations but with the current comet locations
objectcoord = Star(ra_hours=(ascsign*asch,ascm,ascs), dec_degrees=(decsign*decdeg, decmin, decsec))

f = risings_and_settings(eph, objectcoord, observerloc)
timez = timezone('US/Eastern')

#comet is visible if it has 'risen' above the viewer's sky, until it has 'set' out of view of viewer's sky
hasrisen = False
for riseandfalltimes, riseup in zip(*find_discrete(time, endtime, f)):
    if riseup: 
        print('visible from', riseandfalltimes.astimezone(timez).strftime('%a %d %H:%M'))
        hasrisen = True
    #case, comet was visible and is no longer visible
    if not riseup and hasrisen:
        print('to', riseandfalltimes.astimezone(timez).strftime('%a %d %H:%M'))
#second_elements = cometdatas['designation'].str.split(','.str[1])
#print(second_elements)
#for designation in cometdatas.iloc[x]
#act_datas = []
#act_datas.append(cometdatas.iloc[0,0])
#print(act_datas)"""
timez = timezone('US/Eastern')
cometnames = []
for x in range(930):
    cometnames.append(cometdatas.iloc[x,0])
#for each commet (takes a long time, so also have other version that checks only last 50 commets)
if numarg == 4:
    for x in cometnames:
        currentname = cometdatas.loc[x]  
        #determine the location of the current commet (right ascension, declination) from the gravitational center of the galaxy
        currentcomet = sun + mpc.comet_orbit(currentname, timescale, SUN_GRAV_CENT)
        rightascension, declination, distance = earth.at( time ).observe( currentcomet ).radec()
        #splits right ascension into sign, hours, minutes, seconds
        ascsign, asch,ascm,ascs = rightascension.signed_hms(warn=True)
        #splits declination into sign, degrees, minutes, seconds
        decsign,decdeg, decmin, decsec = declination.signed_dms(warn=True)

        objectcoord = Star(ra_hours=(ascsign*asch,ascm,ascs), dec_degrees=(decsign*decdeg, decmin, decsec))
        f = risings_and_settings(eph, objectcoord, observerloc)
        hasrisen = False
        for riseandfalltimes, riseup in zip(*find_discrete(time, endtime, f)):
            #if the commet becomes visible
            if riseup: 
                #print the commet name
                print(x)
                print('visible from', riseandfalltimes.astimezone(timez).strftime('%a %d %H:%M'))
                hasrisen = True
            #comet was visible and is no longer visible
            if not riseup and hasrisen:
                print('to', riseandfalltimes.astimezone(timez).strftime('%a %d %H:%M'))
        if hasrisen:
            #print a blank line before the next commet
            print()

#abridged version that only checks 50 recent commets (much faster)
if numarg == 3 or numarg == 1:
    start_index = 880
    end_index = 930
    #for x in cometnames:
    for x in range(start_index, end_index):
        currentname = cometdatas.loc[cometnames[x]]  
        #determine the location of the current commet (right ascension, declination) from the gravitational center of the galaxy
        currentcomet = sun + mpc.comet_orbit(currentname, timescale, SUN_GRAV_CENT)
        rightascension, declination, distance = earth.at( time ).observe( currentcomet ).radec()
        #splits right ascension into sign, hours, minutes, seconds
        ascsign, asch,ascm,ascs = rightascension.signed_hms(warn=True)
        #splits declination into sign, degrees, minutes, seconds
        decsign,decdeg, decmin, decsec = declination.signed_dms(warn=True)

        objectcoord = Star(ra_hours=(ascsign*asch,ascm,ascs), dec_degrees=(decsign*decdeg, decmin, decsec))
        f = risings_and_settings(eph, objectcoord, observerloc)
        hasrisen = False
        for riseandfalltimes, riseup in zip(*find_discrete(time, endtime, f)):
            #if the commet becomes visible
            if riseup: 
                #print the commet name
                print(cometnames[x])
                print('visible from', riseandfalltimes.astimezone(timez).strftime('%a %d %H:%M'))
                hasrisen = True
            #comet was visible and is no longer visible
            if not riseup and hasrisen:
                print('to', riseandfalltimes.astimezone(timez).strftime('%a %d %H:%M'))
        if hasrisen:
            #print a blank line before the next commet
            print()
