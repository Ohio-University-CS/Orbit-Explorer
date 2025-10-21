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