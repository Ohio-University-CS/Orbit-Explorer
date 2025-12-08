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


from app.schemas.event_item import EventItem
from app.schemas.location import GeodeticLocation

def get_events(
    location: GeodeticLocation,
    start_time: int,
    end_time: int,
    event_types: List[str],
    event_criteria: List
) -> List[EventItem]:
    """
    Temporary placeholder event generator so the backend does not crash.
    Replace with real astronomy event calculations later.
    """

    # Example dummy event
    return [
        EventItem(
            id="event_001",
            type="solar_eclipse",
            name="Partial Solar Eclipse",
            time="1970-01-01T00:00:01",
            desc=f"Dummy event at lat {location.lat}, lon {location.lon}"
        )
    ]
