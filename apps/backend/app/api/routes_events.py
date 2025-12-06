from fastapi import APIRouter, Depends
from typing import List
from app.services.spice_events import (
    get_events,
    event_types,
    get_occultations,
    get_observational_attributes,
    get_visible_planets
)

from app.services.event import (
    get_planet_visibility
)

from app.schemas.event_item import EventItem
from app.schemas.event_criteria import EventCriteria
from app.schemas.location import GeodeticLocation
from app.schemas.events import (
    EventSearchRequest,
    OccultationSearchRequest,
    ObserveBodyRequest,
    VisiblePlanetsRequest
)

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

@router.post("/search/occultations")
async def search_occ(req: OccultationSearchRequest) -> object:
    obj = await get_occultations(
        req.location,
        req.start_time,
        req.end_time,
        req.occulting_naif_id,
        req.occulted_naif_id,
    )

    return obj

@router.post("/observe")
async def observe_body(req: ObserveBodyRequest) -> object:
    obj = await get_observational_attributes(
        req.location,
        req.dt,
        req.body_naif_id
    )

    return obj

@router.post("/visibility/planets")
async def planets_visibility(req: VisiblePlanetsRequest) -> object:
    obj = await get_planet_visibility(
        req.location.lat,
        req.location.lon,
        req.location.alt_km / 1000,
        req.start_time,
        req.end_time
    )