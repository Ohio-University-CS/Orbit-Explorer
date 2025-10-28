#calculate possible solar eclipses in a timeframe
import skyfield
import datetime
import sys
from skyfield import almanac
from skyfield.api import N, S, E, W, load, wgs84

if len(sys.argv) != 7:
    print("Please run the program again with a begin and end date (month1, day1, year1, month2, day2, year2)")
    sys.exit(0)

beginmonth = int(sys.argv[1])
beginday = int(sys.argv[2])
beginyear = int(sys.argv[3])
begin = datetime.datetime(beginyear, beginmonth, beginday)

endmonth = int(sys.argv[4])
endday = int(sys.argv[5])
endyear = int(sys.argv[6])
end = datetime.datetime(endyear, endmonth, endday)

ts = load.timescale()
eph = load('de421.bsp')
sun = eph['Sun']
athens = wgs84.latlon(39.3244 * N, 82.1014 * W)
 # we'll start with the latitude and longitude of ohio university for early verion
observer = eph['Earth'] + athens


#lunar eclipses within a time from t0 date to t1 date (year, month, day)
from skyfield import eclipselib

t0 = ts.utc(beginyear, beginmonth, beginday)
t1 = ts.utc(endyear, endmonth, endday)
t, y, details = eclipselib.lunar_eclipses(t0, t1, eph)

print("Lunar eclupses between", begin.strftime("%B %d %Y"), "and", end.strftime("%B %d %Y"), ":")
for ti, yi in zip(t, y):
    print(ti.utc_strftime('%B %d %Y %H:%M'), eclipselib.LUNAR_ECLIPSES[yi])


