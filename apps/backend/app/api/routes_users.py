from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.schemas.user import User
from app.services.user import (
    create_user,
    get_user_info,
    get_user_saved_locations,
    get_user_preferences,
    save_user_location,
    get_user_saved_events,
    update_user_preferences
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


# Add user saved location
@router.post("/locations/add")
async def post_user_saved_location(
    loc: GeodeticLocation,
    name: str,
    user_uuid: str = Depends(get_current_user_uuid),
):
    success = await save_user_location(user_uuid, loc, name)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save location")
    return {"message": "Location saved successfully"}


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