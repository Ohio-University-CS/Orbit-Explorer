#find solar noon (time of the day sun is directly overhead) in military time
import datetime
from skyfield import almanac
from skyfield.api import wgs84, load
import sys
from pytz import timezone
#from datetime import ts

numarg = len(sys.argv) 
#if no latitude and longitude are specified, use the baker center coordinates
if numarg == 1:
    observerlatitude = 39.3249
    observerlongitude = -82.1017

#take user latitude and longitude as command line arguments
if numarg == 3:
    observerlatitude = sys.argv[1]
    observerlongitude = sys.argv[2]

obstzone = timezone('US/Eastern')
currentdateandtime = obstzone.localize( datetime.datetime.now() )
#last midnight was at 0,0,0,0 of today
lastmidnight = currentdateandtime.replace( hour=0, minute = 0 , second = 0 , microsecond = 0 )
#next midnight is exactly 1 day after last midnight
nextmidnight = lastmidnight + datetime.timedelta(days = 1)

timescale = load.timescale()
timestart = timescale.from_datetime(lastmidnight)
timeend = timescale.from_datetime(nextmidnight)

eph = load('de421.bsp')
observerloc = wgs84.latlon(observerlatitude, observerlongitude)
sunlocations = almanac.meridian_transits(eph, eph['Sun'], observerloc)
times, events = almanac.find_discrete(timestart, timeend, sunlocations)

times = times[events == 1]
solarnoontime = times[0]
#change solarnoon time we just found to a stardard python datetime object, which is easier to work with
solarnoondatetime = solarnoontime.astimezone(obstzone)
print(solarnoondatetime.hour,':',solarnoondatetime.minute,sep="")