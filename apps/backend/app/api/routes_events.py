from fastapi import APIRouter
from typing import List
import httpx

from app.schemas.event_item import EventItem
from app.schemas.event_criteria import EventCriteria
from app.schemas.location import GeodeticLocation
from app.services.event import get_events, event_types

router = APIRouter()

# Search events
@router.get("/search", response_model=List[EventItem])
async def event_search(
    start_time: int,
    end_time: int,
    loc: GeodeticLocation,
    whitelisted_event_types: List[str],
    event_specific_criteria: List[EventCriteria],
):
    return await get_events(loc, start_time, end_time, whitelisted_event_types, event_specific_criteria)

# Event types
@router.get("/types")
async def get_event_types_route():
    return await event_types()

# ⭐ ADD THIS — Reverse geocode ⭐
@router.get("/reverse_geocode")
async def reverse_geocode(lat: float, lon: float):
    url = (
        "https://nominatim.openstreetmap.org/reverse"
        f"?lat={lat}&lon={lon}&format=json"
    )

    async with httpx.AsyncClient(headers={"User-Agent": "OrbitExplorer/1.0"}) as client:
        r = await client.get(url)
        data = r.json()

    address = data.get("address", {})

    return {
        "city": address.get("city") or address.get("town") or address.get("village"),
        "state": address.get("state"),
        "country": address.get("country"),
    }
