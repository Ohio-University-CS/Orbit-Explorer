from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List


from app.astro_lib.events import *

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/event/search")
async def event_search(start_time: int, end_time: int, lon: float, lat: float, elevation: float, whitelisted_event_types: List[str], event_specific_criteria: List[EventCriteria]) -> List[EventItem]:
    geodetic_loc = GeodeticLocation(lon = lon, lat = lat, elevation = elevation)
    events = get_events(geodetic_loc, start_time, end_time, whitelisted_event_types, event_specific_criteria)
    return events

@app.get("/bodies/{name}")
def read_body(name: str):
    info = get_body_info(name)
    if not info:
        raise HTTPException(status_code=404, detail="Celestial body not found")
    return info

@app.get("/user/locations")
def read_user_locations():
    return get_user_saved_locations()

@app.get("/user/preferences")
def read_user_preferences():
    return get_user_preferences()

@app.get("/user/saved-events")
def read_user_saved_events():
    return get_user_saved_events()

@app.post("/user/locations/add")
def post_user_saved_location(lon: float, lat: float, elevation: float, name: str):
    save_user_location(GeodeticLocation(lon, lat, elevation), name)

@app.post("/user/preferences/update")
def post_update_user_preferences(options: List):
    update_user_preferences(options)

def get_user_saved_locations():
    return {
        GeodeticLocation(-82, 39, 100),
        GeodeticLocation(-82, 39.2, 200),
    }