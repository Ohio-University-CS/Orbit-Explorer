from fastapi import APIRouter
from typing import List

from app.services.event import get_events, event_types
from app.schemas.event_item import EventItem
from app.schemas.event_search import EventSearchRequest

router = APIRouter()


@router.post("/search", response_model=List[EventItem])
async def event_search(payload: EventSearchRequest) -> List[EventItem]:
    events = await get_events(
        location=payload.loc,
        start_time=payload.start_time,
        end_time=payload.end_time,
        whitelisted_event_types=payload.whitelisted_event_types,
        event_specific_criteria=payload.event_specific_criteria,
    )
    return events


@router.get("/types")
async def get_event_types():
    return await event_types()
