from pydantic import BaseModel
from typing import List, Any, Dict
from datetime import datetime

from app.schemas.location import GeodeticLocation
from app.schemas.event_criteria import EventCriteria
from fastapi import Depends

from app.services.auth import get_current_user_uuid
class EventSearchRequest(BaseModel):
    start_time: int
    end_time: int
    loc: GeodeticLocation
    whitelisted_event_types: List[str]
    event_specific_criteria: List[EventCriteria]
    user_uuid: str = Depends(get_current_user_uuid)
    

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
    user_uuid: str = Depends(get_current_user_uuid)

class BodyListRequest(BaseModel):
    user_uuid: str = Depends(get_current_user_uuid)