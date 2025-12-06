from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.schemas.location import GeodeticLocation
from app.schemas.event_criteria import EventCriteria
class EventSearchRequest(BaseModel):
    start_time: int
    end_time: int
    loc: GeodeticLocation
    whitelisted_event_types: List[str]
    event_specific_criteria: List[EventCriteria]

class OccultationSearchRequest(BaseModel):
    location: GeodeticLocation
    start_time: datetime
    end_time: datetime
    occulting_naif_id: str
    occulted_naif_id: str

class ObserveBodyRequest(BaseModel):
    location: GeodeticLocation
    dt: datetime
    body_naif_id: str

class VisiblePlanetsRequest(BaseModel):
    location: GeodeticLocation
    start_time: datetime
    end_time: datetime
