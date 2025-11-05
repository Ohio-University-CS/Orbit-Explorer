#calculate possible lunar eclipses in a timeframe
import skyfield
import datetime
import sys
from skyfield import almanac
from skyfield.api import N, S, E, W, load, wgs84
numarg = len(sys.argv) #number of command line arguments
#checks for the right number of arguments, exits if not. will upate to default to starting with today's date
if numarg != 7 and numarg != 4 and numarg != 1:
    print("Please run the program again with the corrent number of arguments")
    sys.exit(0)

#date of the beginning of the range if a date other than the current one is specified (m d y)
if len(sys.argv) == 7:
    beginmonth = int(sys.argv[1])
    beginday = int(sys.argv[2])
    beginyear = int(sys.argv[3])
    begin = datetime.datetime(beginyear, beginmonth, beginday)
#date at the end of the range
    endmonth = int(sys.argv[4])
    endday = int(sys.argv[5])
    endyear = int(sys.argv[6])
    end = datetime.datetime(endyear, endmonth, endday)

#if no begin date specified, use today's date instead
if len(sys.argv) == 4:
    today = datetime.date.today()
    beginmonth = today.month
    beginday = today.day
    beginyear = today.year
    begin = today
#date at the end of the range (no begin date specified by user)
    endmonth = int(sys.argv[1])
    endday = int(sys.argv[2])
    endyear = int(sys.argv[3])
    end = datetime.datetime(endyear, endmonth, endday)

#if no begin or end date are specified, begin with today's date and find lunar eclipses in the next year
if len(sys.argv) == 1:
    today = datetime.date.today()
    beginmonth = today.month
    beginday = today.day
    beginyear = today.year
    begin = today

    endmonth = today.month
    endday = today.day
    endyear = beginyear + 1
    end = datetime.datetime(endyear, endmonth, endday)

timescale = load.timescale()
eph = load('de421.bsp')
sun = eph['Sun'] #location of the sun
 # defaults to the latitude and longitude of ohio university 
athens = wgs84.latlon(39.3244 * N, 82.1014 * W)

#create an observer locations in athens on earth
observer = eph['Earth'] + athens


#lunar eclipses within a time from t0 date to t1 date (year, month, day)
from skyfield import eclipselib

#load time for beginning of the range
begintime = timescale.utc(beginyear, beginmonth, beginday) 
#load time for end of the range
endtime = timescale.utc(endyear, endmonth, endday) 
eclipsetimes, eclipsetypes, details = eclipselib.lunar_eclipses(begintime, endtime, eph)

eclipsedatas = [] #array to store the eclipses found in format mm dd yyyy hh:mmm type for each index

#print results
#prints in military time, might change it to am/pm
for i in range(len(eclipsetimes)):
    eclipsedatas.append(eclipsetimes[i].utc_strftime('%m %d %Y %H:%M') + " " + eclipselib.LUNAR_ECLIPSES[i])
#print("Lunar eclipses between", begin.strftime("%B %d %Y"), "and", end.strftime("%B %d %Y"), ":")
print(eclipsedatas[0])
print(eclipsedatas[1])