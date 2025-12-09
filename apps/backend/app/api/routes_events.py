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
    get_planet_visibility,
    get_asteroids,
    get_moons,
    get_planets
)

from app.schemas.event_item import EventItem
from app.schemas.event_criteria import EventCriteria
from app.schemas.location import GeodeticLocation
from app.schemas.events import (
    EventSearchRequest,
    OccultationSearchRequest,
    ObserveBodyRequest,
    VisiblePlanetsRequest,
    BodyListRequest
)

from app.services.auth import get_current_user_uuid
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
async def search_occ(
    req: OccultationSearchRequest,
    user_uuid: str = Depends(get_current_user_uuid),
):
    obj = await get_occultations(
        req.location,
        req.start_time,
        req.end_time,
        req.occulting_naif_id,
        req.occulted_naif_id
    )
    return obj

@router.post("/observe")
async def observe_body(
    req: ObserveBodyRequest,
    user_uuid: str = Depends(get_current_user_uuid),
) -> object:
    obj = await get_observational_attributes(
        req.location,
        req.dt,
        req.body_naif_id
    )

    return obj

@router.post("/visibility/planets")
async def planets_visibility(req: VisiblePlanetsRequest) -> object:
    obj = get_planet_visibility(
        req.location.lat,
        req.location.lon,
        req.location.alt_km * 1000,
        req.start_time,
        req.end_time
    )
    return obj

@router.post("/bodies/planets")
async def get_bodies_planets(req: BodyListRequest) -> object:
    obj = get_planets()
    return obj

@router.post("/bodies/moons")
async def get_bodies_moons(req: BodyListRequest) -> object:
    obj = get_moons()
    return obj

@router.post("/bodies/asteroids")
async def get_bodies_asteroids(req: BodyListRequest) -> object:
    obj = get_asteroids()
    return obj