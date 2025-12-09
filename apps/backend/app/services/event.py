from fastapi import HTTPException
from typing import List
from datetime import datetime

from app.schemas.event_item import EventItem
from app.schemas.event_criteria import EventCriteria
from app.schemas.location import GeodeticLocation

import psycopg2


# -------------------------------------------------------------------
# Database connection helper
# -------------------------------------------------------------------
def get_conn():
    """
    Open a new connection to the Postgres database running in the
    Docker container named 'db'.
    """
    return psycopg2.connect(
        host="db",
        port=5432,
        database="orbit_explorer",
        user="postgres",
        password="123456",
    )


# -------------------------------------------------------------------
# Event search
# -------------------------------------------------------------------
async def get_events(
    location: GeodeticLocation,
    start_time: int,
    end_time: int,
    whitelisted_event_types: List[str],
    event_specific_criteria: List[EventCriteria],
) -> List[EventItem]:
    """
    Fetch real events from the celestial_events table.

    - Filters by time window [start_time, end_time]
    - Optionally filters by event type names (from celestial_event_types)
    - Ignores event_specific_criteria for now (hook for future logic)
    """

    # Convert unix timestamps (seconds) -> Python datetimes (UTC)
    start_dt = datetime.utcfromtimestamp(start_time)
    end_dt = datetime.utcfromtimestamp(end_time)

    try:
        conn = get_conn()
        cur = conn.cursor()

        # Base query
        sql = """
            SELECT
                e.id,
                cet.event_name,
                e.name,
                e.event_time,
                e.description,
                e.latitude,
                e.longitude,
                e.elevation
            FROM celestial_events e
            JOIN celestial_event_types cet
              ON e.type_id = cet.id
            WHERE e.event_time BETWEEN %s AND %s
        """
        params = [start_dt, end_dt]

        # If user picked specific event types, filter by them
        if whitelisted_event_types:
            sql += " AND cet.event_name = ANY(%s)"
            params.append(whitelisted_event_types)

        sql += " ORDER BY e.event_time;"

        cur.execute(sql, params)
        rows = cur.fetchall()

        events: List[EventItem] = []
        for row in rows:
            (
                event_id,
                event_type,
                name,
                event_time,
                desc,
                lat,
                lon,
                elev,
            ) = row

            events.append(
                EventItem(
                    id=str(event_id),
                    type=event_type,
                    name=name,
                    time=event_time,
                    desc=desc or "",
                )
            )

        cur.close()
        conn.close()

        return events

    except Exception as e:
        # Surface any DB issues as a 500 to the frontend
        raise HTTPException(status_code=500, detail=f"Failed to get events: {e}")


# -------------------------------------------------------------------
# Event types
# -------------------------------------------------------------------
async def event_types():
    """
    Return the event type tree from celestial_event_types.
    """
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
