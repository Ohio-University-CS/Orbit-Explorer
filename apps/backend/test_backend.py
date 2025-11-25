import asyncio
from datetime import datetime
from app.schemas.location import GeodeticLocation
from app.schemas.event_criteria import EventCriteria
from app.schemas.event_item import EventItem

from app.services.spice_events import get_events, event_types, create_observer_spk, find_occultations
from datetime import datetime


import os

# Create a dummy location and criteria
location = GeodeticLocation(
    lat=40.0,
    lon=-82.0,
    elevation=250
)

criteria = [
]
start_time = datetime(2026, 1, 1)
end_time   = datetime(2026, 11, 11)

async def main():

    file_loc = r"C:\Users\Jim\kernels\test.bsp"

    # Extract folder path
    folder = os.path.dirname(file_loc)
    os.makedirs(folder, exist_ok=True)

"""
    # Now create the observer SPK
    create_observer_spk(
        location.lat,
        location.lon,
        location.elevation,
        start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        end_time.strftime("%Y-%m-%dT%H:%M:%S"),
        file_loc,
        -99
    )
"""

    # Then find occultations
    events = find_occultations(
        observer_spk=file_loc,
        observer_id=-99,
        target='SUN',
        occulter='MOON',
        start_utc='2026-09-24T00:00:00',
        end_utc='2026-09-25T00:00:00'
    )

    print("Occultation events:")
    for start, end in events:
        print(start, "-", end)

    # Call get_events directly
    events = await get_events(location, start_time, end_time, ["OCCULTATION"], criteria)
    print("Events returned:")
    for e in events:
        print(e)


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
