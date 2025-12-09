#find the sunrise and sunset times for today, in military time
import sys
from skyfield import almanac
from skyfield.api import N, S, E, W, load, wgs84
import datetime
from pytz import timezone

numarg = len(sys.argv) 
timescale = load.timescale()
eph = load('de421.bsp')
sun = eph['Sun']
#if no latitude and longitude are specified, use the baker center coordinates
if numarg == 1:
    observerlatitude = 39.3249
    observerlongitude = -82.1017

#take user latitude and longitude as command line arguments
if numarg == 3:
    observerlatitude = sys.argv[1]
    observerlongitude = sys.argv[2]

today = datetime.date.today()
beginmonth = today.month
beginday = today.day
beginyear = today.year

#observer's location on earth
observerloc = wgs84.latlon(observerlatitude, observerlongitude)
#observer's location from the sun is the location of the center of the earth from the sun + the observer's location from the center of the earth
observer = eph['Earth'] + observerloc

obstzone = timezone('US/Eastern')
currentdateandtime = obstzone.localize( datetime.datetime.now() )
#last midnight was at 0,0,0,0 of today
lastmidnight = currentdateandtime.replace( hour=0, minute = 0 , second = 0 , microsecond = 0 )
#next midnight is exactly 1 day after last midnight
nextmidnight = lastmidnight + datetime.timedelta(days = 1)
timescale = load.timescale()
timestart = timescale.from_datetime(lastmidnight)
timeend = timescale.from_datetime(nextmidnight)

sunrise, x = almanac.find_risings(observer, sun, timestart, timeend)
sunrisetimedatetime = sunrise[0].astimezone(obstzone)
sunrisehours = sunrisetimedatetime.hour
sunriseminutes = sunrisetimedatetime.minute
print(sunrisehours,":", sunriseminutes,sep="")

sunset, y = almanac.find_settings(observer, sun, timestart, timeend)
sunsettimedatetime = sunset[0].astimezone(obstzone)
sunsethours = sunsettimedatetime.hour
sunsetminutes = sunsettimedatetime.minute
print(sunsethours,":", sunsetminutes,sep="")