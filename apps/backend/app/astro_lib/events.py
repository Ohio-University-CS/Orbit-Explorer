# astro_lib/events.py
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
from skyfield.api import load


class EventType:
    def __init__(self, name, subtypes = None, search_params = None):
        self.name = name
        self.subtypes = subtypes or []
        self.search_params = search_params or []

    def add_subtype(self, subtype):
        self.subtypes.append(subtype)

    def __repr__(self):
        if self.subtypes:
            return f"{self.name}: [{', '.join([str(s) for s in self.subtypes])}]"
        return self.name


def gen_events():
    lunar_search_params = [
        Field("")
    ]
    # ------------------------------
    # 1. Eclipses
    # ------------------------------
    LUNAR_ECLIPSE = EventType("LUNAR_ECLIPSE", [
        EventType("PENUMBRAL"),
        EventType("PARTIAL"),
        EventType("TOTAL"),
        EventType("CENTRAL"),
        EventType("SELENELION")
    ])

    SOLAR_ECLIPSE = EventType("SOLAR_ECLIPSE", [
        EventType("PARTIAL"),
        EventType("TOTAL"),
        EventType("ANNULAR"),
        EventType("HYBRID")
    ])

    # ------------------------------
    # 2. Celestial Alignments
    # ------------------------------
    SYZYGY = EventType("SYZYGY", [
        EventType("PERIGEE_SYZYGY"),
        EventType("OPPOSITION"),
        EventType("CONJUNCTION"),
        EventType("QUADRATURE")
    ])

    # ------------------------------
    # 3. Planetary Motion
    # ------------------------------
    RETROGRADE_MOTION = EventType("RETROGRADE_MOTION")

    # ------------------------------
    # 4. Small Bodies
    # ------------------------------
    METEOR = EventType("METEOR", [
        EventType("SHOWER"),
        EventType("OUTBURST")
    ])

    COMET = EventType("COMET_APPEARANCE")

    ASTEROID = EventType("ASTEROID_FLYBY")

    # ------------------------------
    # 5. Transits / Occultations
    # ------------------------------
    TRANSIT = EventType("TRANSIT")
    OCCULTATION = EventType("OCCULTATION")

    # ------------------------------
    # 6. Seasonal / Solar Events
    # ------------------------------
    SEASONAL = EventType("SEASONAL", [
        EventType("EQUINOX"),
        EventType("SOLSTICE")
    ])

class EventType(BaseModel):
    name: str
    subtypes: List["EventType"] = []  # use a string type for self-reference
    criteria: List["EventCriteria"] = []
    description: str

    class Config:
        arbitrary_types_allowed = True  # ignore unknown nested types


planets = load('de421.bsp')
earth = planets['earth']

def get_body_info(name: str):
    name = name.lower()


    ts = load.timescale()
    t = ts.now()
    body = planets[name]

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