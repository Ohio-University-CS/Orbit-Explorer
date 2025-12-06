import asyncio
from datetime import datetime
from app.schemas.location import GeodeticLocation
from app.schemas.event_criteria import EventCriteria
from app.schemas.event_item import EventItem

from app.services.spice_events import (
    create_site_helper,
    handle_occultations,
    generate_site_guid,
    calculate_phase_angle,
    l_observational_attributes,
    populate_bodies_table
)

from app.services.event import (
    get_planet_visibility
)
from datetime import datetime


import os

# Create a dummy location and criteria
location = GeodeticLocation(
    lat=66.066666,
    lon=-23.116666,
    alt_km=0
)


location = GeodeticLocation(
    lat=43.462779,
    lon=-23.805,
    alt_km=0
)

location = GeodeticLocation(
    lat =42.22038,
    lon=-4.02100,
    alt_km=0,
)


criteria = [
]
start_time = datetime(2026, 1, 1,1)
end_time   = datetime(2026, 1, 1,2)

async def main():
    #guid = generate_site_guid(21)
    #create_site_helper(guid, 399901, location)
    #site = "GC87F937ACA4E436C8177"
    #site=guid
    #handle_occultations(site, start_time, end_time)

    obj = get_planet_visibility(
        location.lat,
        location.lon,
        location.alt_km / 1000,
        start_time,
        end_time
    )

    print(obj)
# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
