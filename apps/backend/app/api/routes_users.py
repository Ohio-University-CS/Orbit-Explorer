from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.schemas.user import (
    User,
    UserLocation,
    UserLocationRequest,
    EventSaveRequest,
    EventRemoveRequest,
)

from app.services.user import (
    create_user,
    get_user_info,
    get_user_saved_locations,
    get_user_preferences,
    save_user_location,
    get_user_saved_events,
    get_user_saved_event,
    update_user_preferences,
    save_event,
    delete_event,
    delete_user_location
)
from app.services.auth import get_current_user_uuid
from app.schemas.location import GeodeticLocation

router = APIRouter()

# Get user info
@router.get("/info")
async def get_user_info_route(user_uuid: str = Depends(get_current_user_uuid)):
    user_info = await get_user_info(user_uuid)
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")
    return user_info

# Get user locations
@router.get("/locations")
async def get_user_locations(user_uuid: str = Depends(get_current_user_uuid)):
    return await get_user_saved_locations(user_uuid)


# Get user preferences
@router.get("/preferences")
async def read_user_preferences(user_uuid: str = Depends(get_current_user_uuid)):
    preferences = await get_user_preferences(user_uuid)
    if not preferences:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return preferences


# Get saved events
@router.get("/saved-events")
async def read_user_saved_events(user_uuid: str = Depends(get_current_user_uuid)):
    return await get_user_saved_events(user_uuid)


@router.post("/events/{eid}")
async def post_remove_event(eid: int, user_uuid: str = Depends(get_current_user_uuid)):
    return await get_user_saved_event(user_uuid, eid)

@router.post("/event/remove")
async def post_remove_event(req: EventRemoveRequest, user_uuid: str = Depends(get_current_user_uuid)):
    deleted = await delete_event(user_uuid, req.id)
    if deleted:
        return {"message": "Event deleted successfully", "id": req.id}
    else:
        raise HTTPException(status_code=404, detail="Event not found")

@router.post("/locations/add")
async def post_user_saved_location(
    loc_req: UserLocationRequest,
    user_uuid: str = Depends(get_current_user_uuid)
):
    loc = UserLocation(
        id=None,
        user_uuid=user_uuid,
        loc_name=loc_req.loc_name,
        loc_description=loc_req.loc_description,
        latitude=loc_req.latitude,
        longitude=loc_req.longitude,
        alt_km=loc_req.alt_km
    )

    success = await save_user_location(user_uuid, loc)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save location")

    return {"message": "Location saved successfully", "id": success["id"]}

@router.post("/location/remove")
async def remove_user_saved_location(
    loc_req: dict,
    user_uuid: str = Depends(get_current_user_uuid)
):
    loc_id = loc_req.get("id")
    if not loc_id:
        raise HTTPException(status_code=400, detail="Location id is required")

    success = await delete_user_location(user_uuid, loc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Location not found or not owned by user")

    return {"message": "Location removed successfully", "id": loc_id}

# Update user preferences
@router.post("/preferences/update")
async def post_update_user_preferences(
    options: List,
    user_uuid: str = Depends(get_current_user_uuid),
):
    success = await update_user_preferences(user_uuid, options)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update preferences")
    return {"message": "Preferences updated successfully"}

@router.post("/event/save")
async def post_save_event(
    req: EventSaveRequest,
    user_uuid: str = Depends(get_current_user_uuid),
):
    obj = await save_event(
        req, user_uuid
    )
    return obj
