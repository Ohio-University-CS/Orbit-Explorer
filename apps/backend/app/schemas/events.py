from pydantic import BaseModel
from typing import List

from app.schemas.location import GeodeticLocation
from app.schemas.event_criteria import EventCriteria
class EventSearchRequest(BaseModel):
    start_time: int
    end_time: int
    loc: GeodeticLocation
    whitelisted_event_types: List[str]
    event_specific_criteria: List[EventCriteria]