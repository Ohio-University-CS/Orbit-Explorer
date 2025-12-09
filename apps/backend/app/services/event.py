from fastapi import HTTPException
from typing import List
from datetime import datetime, timedelta

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
        password="123456",
    )


async def get_events(
    location: GeodeticLocation,
    start_time: int,
    end_time: int,
    whitelisted_event_types: List[str],
    event_specific_criteria: List[EventCriteria],
) -> List[EventItem]:
    """
    Temporary implementation:
    - Uses your time window & location.
    - Returns one dummy event per whitelisted type so you can see the wiring working.
    - Later you can replace this with real Skyfield / DB logic.
    """
    start_dt = datetime.utcfromtimestamp(start_time)
    end_dt = datetime.utcfromtimestamp(end_time)

    # If nothing selected, default to a generic OCCULTATION so the UI still shows something.
    if not whitelisted_event_types:
        whitelisted_event_types = ["OCCULTATION"]

    events: List[EventItem] = []

    for idx, ev_type in enumerate(whitelisted_event_types):
        event_time = start_dt + timedelta(minutes=idx * 10)

        # encode criteria summary (optional)
        criteria_summary = ", ".join(
            f"{c.name}: {c.description}" for c in (event_specific_criteria or [])
        )

        desc = (
            f"Dummy {ev_type} near lat {location.lat:.4f}, lon {location.lon:.4f}, "
            f"elevation {location.elevation}m."
        )
        if criteria_summary:
            desc += f" Criteria → {criteria_summary}"

        events.append(
            EventItem(
                id=f"dummy_{idx+1}",
                type=ev_type,
                name=f"Placeholder {ev_type.replace('_', ' ').title()}",
                time=event_time,
                desc=desc,
            )
        )

    return events


async def event_types():
    try:
        conn = get_conn()
        cur = conn.cursor()
        event_types_list = []

        cur.execute("SELECT id, parent_id, event_name FROM celestial_event_types")
        for row in cur.fetchall():
            id, parent_id, event_name = row
            event_types_list.append(
                {
                    "id": id,
                    "parent_id": parent_id,
                    "name": event_name,
                }
            )

        cur.close()
        conn.close()
        return event_types_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get event types: {e}")
