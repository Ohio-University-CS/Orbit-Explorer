# astro_lib/events.py
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field

from skyfield.api import load

# Simple EventItem model
class EventItem(BaseModel):
    id: str
    type: str
    name: str
    time: datetime
    desc: str

class GeodeticLocation(BaseModel):
    lon: float = Field(..., ge=-180.0, le=180.0, description="Longitude in degrees east")
    lat: float = Field(..., ge=-90.0, le=90.0, description="Latitude in degrees north")
    elevation: float = Field(..., description="Elevation in meters above WGS84 ellipsoid")


planets = load('de421.bsp')
earth = planets['earth']

def get_body_info(name: str):
    name = name.lower()
    body_map = {
        'sun': 'sun',
        'moon': 'moon',
        'mercury': 'mercury',
        'venus': 'venus',
        'mars': 'mars',
        'jupiter': 'jupiter barycenter',
        'saturn': 'saturn barycenter',
        'uranus': 'uranus barycenter',
        'neptune': 'neptune barycenter',
        'pluto': 'pluto barycenter',
    }

    if name not in body_map:
        return None

    ts = load.timescale()
    t = ts.now()
    body = planets[body_map[name]]

    astrometric = earth.observe(body).apparent()
    ra, dec, distance = astrometric.radec()

    return {
        "name": name.capitalize(),
        "right_ascension_hours": ra.hours,
        "declination_degrees": dec.degrees,
        "distance_au": distance.au,
        "distance_km": distance.km,
        "datetime": t.utc_strftime('%Y-%m-%d %H:%M:%S UTC')
    }


def get_events(location: GeodeticLocation, start_time: int, end_time: int) -> List[EventItem]:
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