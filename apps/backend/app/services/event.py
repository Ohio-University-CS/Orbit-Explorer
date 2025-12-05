from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

from app.schemas.event_item import EventItem
from app.schemas.event_criteria import EventCriteria

from app.schemas.location import GeodeticLocation

import psycopg2

# Database connection function
def get_conn():
    return psycopg2.connect(
        host="db",
        port=5432,
        database="orbit_explorer",
        user="postgres",
        password="123456"
    )


async def get_events(location: GeodeticLocation, start_time: int, end_time: int, whitelisted_event_types: List[str], event_specific_criteria: List[EventCriteria]) -> List[EventItem]:
    start_dt = datetime.utcfromtimestamp(start_time)
    end_dt = datetime.utcfromtimestamp(end_time)

    dummy_event = EventItem(
        id="event_001",
        type="solar_eclipse",
        name="Partial Solar Eclipse",
        time=start_dt,
        desc=f"Dummy event at lat {location.lat}, lon {location.lon}"
    )

    return [dummy_event]

async def event_types():
    try:
        conn = get_conn()
        cur = conn.cursor()
        event_types_list = []

        cur.execute("SELECT id, parent_id, name FROM celestial_event_types")
        for row in cur.fetchall():
            id, parent_id, name = row
            event_types_list.append({
                "id": id,
                "parent_id": parent_id,
                "name": name
            })

        cur.close()
        conn.close()
        return event_types_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get event types: {e}")