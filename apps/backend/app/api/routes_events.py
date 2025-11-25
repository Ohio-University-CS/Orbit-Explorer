from fastapi import APIRouter, Depends
from typing import List
from app.services.event import get_events, event_types

from app.schemas.event_item import EventItem
from app.schemas.event_criteria import EventCriteria
from app.schemas.location import GeodeticLocation
from app.schemas.events import EventSearchRequest

router = APIRouter()

@router.post("/search", response_model=List[EventItem])
async def event_search(req: EventSearchRequest) -> List[EventItem]:
    events = await get_events(
        req.loc,
        req.start_time,
        req.end_time,
        req.whitelisted_event_types,
        req.event_specific_criteria,
    )
    return events

@router.get("/types")
async def get_event_types():
    return await event_types()