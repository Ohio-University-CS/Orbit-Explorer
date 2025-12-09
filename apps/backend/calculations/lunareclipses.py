#calculate possible lunar eclipses in a timeframe, defaults to 1 year out from current day
import skyfield
import datetime
import sys
from skyfield import almanac
from skyfield.api import N, S, E, W, load, wgs84 #positional constants, include world geodetic system
from skyfield import eclipselib # used to find eclipses
numarg = len(sys.argv) #number of command line arguments
#checks for the right number of arguments, exits if not. will upate to default to starting with today's date
def beginToday():
    timescale = load.timescale()
    today = datetime.date.today()
    beginmonth = today.month
    beginday = today.day
    beginyear = today.year
    return timescale.utc(beginyear, beginmonth, beginday) 

def checkValidDate(month, day, year):
    # no zero, negative day months
    if day < 1:
        return False
    #months cannot be less than 1 or greater than 12
    if month < 1 or month > 12 :
        return False
    #case: month should have 31 days
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        if day > 31 :
            return False
    if month == 2:
        if year % 4 == 0: 
            # if it is a leap year
            if day > 29 :
                return False
        else : 
            # non leap year february
            if day > 28:
                return False
            return False
    if month == 4 or month == 6 or month == 9 or month == 11:
    #case: month should have 30 days
        if day > 30:
            return False
    return True

def checkEndAfterBegin(bmonth,bday,byear,emonth,eday,eyear):
    if eyear > byear:
        return True
    if eyear < byear:
        return False
    if emonth > bmonth:
        return True
    if emonth < bmonth:
        return True
    if eday < bday:
        return False
    return True       
        
def checkSpan(bmonth,bday,byear,emonth,eday,eyear):
    beginmonth = bmonth
    beginday = bday
    beginyear = byear
    if not checkValidDate(beginmonth, beginday, beginyear) :
        print("Error: invalid date")
        sys.exit(0)
    begin = datetime.datetime(beginyear, beginmonth, beginday)
#date at the end of the range
    endmonth = emonth
    endday = eday
    endyear = eyear
    if not checkValidDate(endmonth, endday, endyear) :
        print("Error: invalid date")
        sys.exit(0)
    end = datetime.datetime(endyear, endmonth, endday)
    if not checkEndAfterBegin(beginmonth,beginday,beginyear,endmonth,endday,endyear):
        print("Error: end date cannot be before begin date")
        sys.exit(0)
    timescale = load.timescale()
    eph = load('de421.bsp')
    timescale.utc(beginyear, beginmonth, beginday) 
    #load time for beginning of the range
    begintime = beginToday() 
    #load time for end of the range
    endtime = timescale.utc(endyear, endmonth, endday) 
    eclipsetimes, eclipsetypes, details = eclipselib.lunar_eclipses(begintime, endtime, eph)

    eclipsedatas = [] #array to store the eclipses found in format mm dd yyyy hh:mmm type for each index

    for i in range(len(eclipsetimes)):
        eclipsedatas.append(eclipsetimes[i].utc_strftime('%m %d %Y %H:%M') + " " + eclipselib.LUNAR_ECLIPSES[eclipsetypes[i]])
        print(eclipsedatas[i])    
    

def checkNextYear():
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
    timescale.utc(beginyear, beginmonth, beginday) 
    #load time for beginning of the range
    begintime = beginToday() 
    #load time for end of the range
    endtime = timescale.utc(endyear, endmonth, endday) 
    eclipsetimes, eclipsetypes, details = eclipselib.lunar_eclipses(begintime, endtime, eph)

    eclipsedatas = [] #array to store the eclipses found in format mm dd yyyy hh:mmm type for each index

    for i in range(len(eclipsetimes)):
        eclipsedatas.append(eclipsetimes[i].utc_strftime('%m %d %Y %H:%M') + " " + eclipselib.LUNAR_ECLIPSES[eclipsetypes[i]])
        print(eclipsedatas[i])    


if numarg != 7 and numarg != 4 and numarg != 1:
    print("Please run the program again with the corrent number of arguments")
    sys.exit(0)

#date of the beginning of the range if a date other than the current one is specified (m d y)
if len(sys.argv) == 7:
    beginmonth = int(sys.argv[1])
    beginday = int(sys.argv[2])
    beginyear = int(sys.argv[3])
    if not checkValidDate(beginmonth, beginday, beginyear) :
        print("Error: invalid date")
        sys.exit(0)
    begin = datetime.datetime(beginyear, beginmonth, beginday)
#date at the end of the range
    endmonth = int(sys.argv[4])
    endday = int(sys.argv[5])
    endyear = int(sys.argv[6])
    if not checkValidDate(endmonth, endday, endyear) :
        print("Error: invalid date")
        sys.exit(0)
    end = datetime.datetime(endyear, endmonth, endday)

    if not checkEndAfterBegin(beginmonth,beginday,beginyear,endmonth,endday,endyear):
        print("Error: end date cannot be before begin date")
        sys.exit(0)

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
    if not checkValidDate(endmonth, endday, endyear) :
        sys.exit(0)
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


#load time for beginning of the range
begintime = timescale.utc(beginyear, beginmonth, beginday) 
#load time for end of the range
endtime = timescale.utc(endyear, endmonth, endday) 
eclipsetimes, eclipsetypes, details = eclipselib.lunar_eclipses(begintime, endtime, eph)

eclipsedatas = [] #array to store the eclipses found in format mm dd yyyy hh:mmm type for each index

#print results
#prints in military time, might change it to am/pm
for i in range(len(eclipsetimes)):
    eclipsedatas.append(eclipsetimes[i].utc_strftime('%m %d %Y %H:%M') + " " + eclipselib.LUNAR_ECLIPSES[eclipsetypes[i]])
    print(eclipsedatas[i])

#print("Lunar eclipses between", begin.strftime("%B %d %Y"), "and", end.strftime("%B %d %Y"), ":")
#checkNextYear()