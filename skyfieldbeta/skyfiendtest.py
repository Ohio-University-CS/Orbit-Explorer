#calculate possible solar eclipses in a timeframe
#import skyfield
from skyfield import almanac
#double check correct calls for intended dates (also timezone)
t0 = ts.utc(2025, 10, 22) #beginning of timeframe october 22
t1 = ts.utc(2025, 11, 1) #end of timeframe nov 1st
t, y = almanac.find_discrete(t0, t1, almanac.moon_nodes(eph))

print(t.utc_iso())
print(y)
print([almanac.MOON_NODES[yi] for yi in y])
#double check time section of time formatting (also change timezone?)
['2025-10-22T00:00:00Z', '2025-11-01T23:59:59Z']
[1 0]
['ascending', 'descending']

