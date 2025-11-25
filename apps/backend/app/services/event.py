from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from functools import partial

from app.schemas.event_item import EventItem
from app.schemas.event_criteria import EventCriteria

from app.schemas.location import GeodeticLocation

import psycopg2


from skyfield import api
from skyfield.searchlib import find_discrete
from skyfield.toposlib import Topos

import spiceypy as spice
import numpy as np

# Database connection function
def get_conn():
    return psycopg2.connect(
        host="db",
        port=5432,
        database="orbit_explorer",
        user="postgres",
        password="123456"
    )


def find_occultation(t, location, observer_eph, target_eph, occulting_eph):
    """Observer must be Earth"""
    ref_pt = observer_eph + Topos(latitude=location.lat, longitude=location.lon, elevation_m=location.elevation)
    o = ref_pt.at(t)

    # Apparent positions as seen from observer
    target_pos = o.observe(target_eph).apparent()
    occulting_pos = o.observe(occulting_eph).apparent()

    # Angular separation in degrees
    separation = target_pos.separation_from(occulting_pos).degrees

    # Apparent angular radii in degrees
    target_rad = target_pos.angular_radius().degrees
    occulting_rad = occulting_pos.angular_radius().degrees

    # Occultation occurs if separation < sum of angular radii
    is_occulting = separation < (target_rad + occulting_rad)

    print("is_occulting:", is_occulting)
    return is_occulting

def find_all_occulations(location: GeodeticLocation, start_time: int, end_time: int):
    ts = api.load.timescale()
    t0 = ts.utc(2020, 6, 2)
    t1 = ts.utc(2021, 6, 2)

    eph = api.load('de421.bsp')
    earth, sun, moon = eph['earth'], eph['sun'], eph['moon']
    callback = partial(
        find_occultation,
        location=location,
        observer_eph=earth,
        target_eph=sun,
        occulting_eph=moon
    )


    callback.step_days = .01
    t_events, states = find_discrete(t0, t1, callback)

    return t_events

async def get_events(location: GeodeticLocation, start_time: int, end_time: int, whitelisted_event_types: List[str], event_specific_criteria: List[EventCriteria]) -> List[EventItem]:
    start_dt = datetime.utcfromtimestamp(start_time)
    end_dt = datetime.utcfromtimestamp(end_time)

    events = []
    
    occulations = spice_get_occulations(location, start_time, end_time)
    for idx, e in enumerate(occulations):
        events.append(EventItem(
            id=f"event_{idx:03d}"
        ))

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