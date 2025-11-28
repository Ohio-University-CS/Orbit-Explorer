import asyncio
from datetime import datetime
from app.schemas.location import GeodeticLocation
from app.schemas.event_criteria import EventCriteria
from app.schemas.event_item import EventItem

from app.services.spice_events import create_site_helper, generate_site_guid
from datetime import datetime


import os

# Create a dummy location and criteria
location = GeodeticLocation(
    lat=40.0,
    lon=-82.0,
    alt_km=250
)

criteria = [
]
start_time = datetime(2026, 1, 1)
end_time   = datetime(2026, 11, 11)

async def main():
    guid = generate_site_guid(21)
    create_site_helper(guid, 399901, location)

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
