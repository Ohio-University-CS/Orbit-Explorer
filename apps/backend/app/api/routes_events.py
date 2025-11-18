from fastapi import APIRouter, Depends
from typing import List
from app.services.event import get_events, event_types

from app.schemas.event_item import EventItem
from app.schemas.event_criteria import EventCriteria
from app.schemas.location import GeodeticLocation

router = APIRouter()

@router.get("/search", response_model = List[EventItem])
async def event_search(start_time: int, end_time: int, loc: GeodeticLocation, whitelisted_event_types: List[str], event_specific_criteria: List[EventCriteria]) -> List[EventItem]:
    events = await get_events(loc, start_time, end_time, whitelisted_event_types, event_specific_criteria)
    return events

@router.get("/types")
async def get_event_types():
    return await event_types()