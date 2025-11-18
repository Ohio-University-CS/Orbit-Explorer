from skyfield.api import load
from skyfield.data import mpc
from skyfield.constants import GM_SUN_Pitjeva_2005_km3_s2 as SUN_GRAV_CENT #center of gravity of the sun (not necessarily the center of the sun)
import datetime
from datetime import date
with load.open(mpc.COMET_URL, reload = True) as minorplanetcentercometdata: #download and open comet history data
    cometdatas = mpc.load_comets_dataframe( minorplanetcentercometdata )

today = datetime.date.today()
currentmonth = today.month
currentday = today.day
currentyear = today.year
timescale = load.timescale()
time = timescale.utc(currentyear, currentmonth, currentday)

eph = load('de421.bsp')
sun, earth = eph['sun'], eph['earth']
#print('the data for', len( cometdatas ), 'comets have been loaded into the program') #print how many commets have been loaded

# use the last known location for each commet, indexed by designation
cometdatas = (cometdatas.sort_values('reference')
          .groupby('designation', as_index=False).last()
          .set_index('designation', drop=False))

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