import skyfield
import datetime
import sys
from skyfield import almanac
from skyfield.api import N, S, E, W, load, wgs84
from datetime import date, timedelta
import numpy
eph = load('de421.bsp')

def checkLunarValidDate(month, day, year):
    if day < 1:
        return False
    if month < 1 or month > 12 :
        return False
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        if day > 31 :
            return False
    if month == 2:
        if year % 4 == 0: # if it is a leap year
            if day > 29 :
                return False
        else : 
            if day > 28:
                return False
            return False
    if month == 4 or month == 6 or month == 9 or month == 11:
        if day > 30:
            return False
    return True

timescale = load.timescale()
numarg = len(sys.argv) #number of command line arguments
#checks for the right number of arguments, exits if not. will upate to default to starting with today's date
if numarg != 1 and numarg != 4:
    print("Please run the program again with the corrent number of arguments")
    sys.exit(0)

#if no arguments provided, find next full moon starting from today
if numarg == 1: 
    today = datetime.date.today()
    beginmonth = today.month
    beginday = today.day
    beginyear = today.year
    begin = today

#if a date is provided, find next full moon starting from that date (m d y)
if numarg == 4:
    beginmonth = int(sys.argv[1])
    beginday = int(sys.argv[2])
    beginyear = int(sys.argv[3])
    begin = datetime.datetime(beginyear, beginmonth, beginday)
    if not checkLunarValidDate(beginmonth, beginday, beginyear) :
        print("Error: invalid date")
        sys.exit(0)

timescaleTime = timescale.utc(beginyear, beginmonth, beginday)

phase = almanac.moon_phase(eph, timescaleTime)

begintime = timescale.utc(beginyear, beginmonth, beginday)

#get the date 30 days from now to find when the full moon is in this span (the next full moon)
enddate = begin + timedelta(days=30)

endmonth = enddate.month
endday = enddate.day
endyear = enddate.year

endtime = timescale.utc(endyear, endmonth, endday)

moonphasetimes, phases = almanac.find_discrete(begintime, endtime, almanac.moon_phases(eph))
#full moon is when phases = 2 

#find location in data where phases = 2
templist = numpy.array(phases)
indexoffullmoon = list(templist).index(2)

#date corresponding to where phases = 2 (full noon)
dateofnextfullmoon = moonphasetimes[indexoffullmoon].utc_strftime('%m %d %Y') #format is mm dd yyyy

#print("The next full moon is", dateofnextfullmoon)
print(dateofnextfullmoon)