# apps/backend/app/schemas/event_search.py
from pydantic import BaseModel
from typing import List

from app.schemas.location import GeodeticLocation
from app.schemas.event_criteria import EventCriteria


class EventSearchRequest(BaseModel):
    start_time: int              # unix timestamp (seconds)
    end_time: int                # unix timestamp (seconds)
    loc: GeodeticLocation        # { lon, lat, elevation }
    whitelisted_event_types: List[str]
    event_specific_criteria: List[EventCriteria] = []
