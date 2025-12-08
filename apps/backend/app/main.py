from fastapi import FastAPI, HTTPException
from typing import List
from app.api import user_router, event_router, auth_router

from app.schemas.event_item import EventItem
from app.schemas.event_criteria import EventCriteria
from app.schemas.location import GeodeticLocation
from app.astro_lib.events import get_events
from app.astro_lib.utils import get_body_info
from passlib.context import CryptContext
import psycopg2

app = FastAPI(title="Orbit-Explorer API")



@app.get("/")
def home():
    return {"message": "Hi class, welcome to Orbit Explorer!"}

@app.get("/event/search")
def event_search(
    start_time: int,
    end_time: int,
    lon: float,
    lat: float,
    elevation: float,
    whitelisted_event_types: List[str],
    event_specific_criteria: List[EventCriteria]
) -> List[EventItem]:

    geodetic_loc = GeodeticLocation(lon=lon, lat=lat, elevation=elevation)
    events = get_events(
        geodetic_loc,
        start_time,
        end_time,
        whitelisted_event_types,
        event_specific_criteria
    )

    return events


@app.get("/bodies/{name}")
def read_body(name: str):
    info = get_body_info(name)
    if not info:
        raise HTTPException(status_code=404, detail="Celestial body not found")
    return info


@app.get("/user/info")
def get_user_info(user_id: int):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT email, username, created_at, first_name FROM users WHERE user_id = %s",
            (user_id,)
        )
        row = cur.fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="User not found")

        email, username, created_at, first_name = row

        cur.close()
        conn.close()

        return {
            "id": user_id,
            "first_name": first_name,
            "email": email,
            "username": username,
            "created_at": created_at
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user: {e}")


@app.get("/user/add")
def post_add_user(email: str, first_name: str, password: str, username: str):
    try:
        conn = get_conn()
        cur = conn.cursor()

        pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        hashed = pwd_context.hash(password)

        cur.execute(
            "INSERT INTO users (email, first_name, password_hash, username)"
            " VALUES (%s, %s, %s, %s) RETURNING user_id",
            (email, first_name, hashed, username)
        )

        user_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return {"id": user_id, "status": "success"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add user: {e}")


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
    save_user_location(
        GeodeticLocation(lon=lon, lat=lat, elevation=elevation),
        name
    )


@app.post("/user/preferences/update")
def post_update_user_preferences(options: List):
    update_user_preferences(options)


def get_user_saved_locations():
    return [
        GeodeticLocation(lon=-82, lat=39, elevation=100),
        GeodeticLocation(lon=-82, lat=39.2, elevation=200),
    ]


def save_user_location(loc: GeodeticLocation, name: str):
    pass


def get_user_preferences():
    return []


def get_user_saved_events():
    return []


def get_conn():
    return psycopg2.connect(
        host="db",
        port=5432,
        database="orbit_explorer",
        user="postgres",
        password="123456"
    )


app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(event_router, prefix="/events", tags=["events"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

from app.api.routes_reverse_geocode import reverse_router

app.include_router(reverse_router, prefix="/events", tags=["reverse-geocode"])
