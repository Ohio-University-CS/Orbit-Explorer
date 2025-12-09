from fastapi import HTTPException
from pydantic import BaseModel, Field

from typing import List, Dict, Any
import psycopg2
from psycopg2 import errors
import json
from datetime import datetime

import uuid
from passlib.context import CryptContext
from app.schemas.location import GeodeticLocation
from app.schemas.user import (
    LoginRequest,
    RegisterRequest,
    User,
    UserLocation
)

# Database connection function
def get_conn():
    return psycopg2.connect(
        host="db",
        port=5432,
        database="orbit_explorer",
        user="postgres",
        password="123456"
    )

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Get user information by user_id
async def user_login(login_request: LoginRequest) -> User:
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("SELECT uuid, password_hash FROM users WHERE username = %s", (login_request.username,))

        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        user_uuid, password_hash = row

        # Verify password
        if not pwd_context.verify(login_request.password, password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        cur.close()
        conn.close()

        return User(uuid=user_uuid)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to login: {e}")

# Create a new user
async def create_user(new_user: RegisterRequest) -> User:
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Check if username already exists
        cur.execute("SELECT 1 FROM users WHERE username = %s", (new_user.username,))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="username already exists")

        user_uuid = str(uuid.uuid4())
        # Hash password
        hashed = pwd_context.hash(new_user.password)

        # Insert user
        cur.execute(
            "INSERT INTO users (email, first_name, last_name, password_hash, username, uuid) VALUES (%s, %s, %s, %s, %s, %s)", 
            (new_user.email, new_user.first_name, new_user.last_name, hashed, new_user.username, user_uuid,)
        )

        conn.commit()

        cur.close()
        conn.close()

        user = User(uuid=user_uuid)
        return user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add user: {e}")

async def get_user_saved_locations(user_uuid: str) -> List[UserLocation]:
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, loc_name, loc_description, latitude, longitude, alt_km, user_uuid
            FROM user_locations
            WHERE user_uuid = %s
        """, (user_uuid,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [
            UserLocation(
                id=row[0],
                loc_name=row[1],
                loc_description=row[2],
                latitude=row[3],
                longitude=row[4],
                alt_km=row[5],
                user_uuid=row[6],
            )
            for row in rows
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch locations: {e}")

async def save_user_location(user_uuid: str, loc: UserLocation):
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Insert location for the user
        cur.execute(
            """
            INSERT INTO user_locations (user_uuid, loc_name, loc_description, latitude, longitude, alt_km)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (user_uuid, loc.loc_name, loc.loc_description, loc.latitude, loc.longitude, loc.alt_km)
        )

        loc_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return {
            "message": "Location saved successfully",
            "id": loc_id,
            "user_uuid": user_uuid,
            "loc_name": loc.loc_name,
            "loc_description": loc.loc_description,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "alt_km": loc.alt_km
        }

    except Exception as e:
        # Handle duplicate entry for same user
        if isinstance(e, errors.UniqueViolation):
            raise HTTPException(
                status_code=400,
                detail="A location with the same coordinates already exists for this user."
            )
        raise HTTPException(status_code=500, detail=f"Failed to save location: {e}")

async def delete_user_location(user_uuid: str, loc_id: int):
    """
    Deletes a location by id for the given user.
    Returns True if a row was deleted, False otherwise.
    """
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            DELETE FROM user_locations
            WHERE id = %s AND user_uuid = %s
            RETURNING id
            """,
            (loc_id, user_uuid)
        )

        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return bool(result)  # True if a row was deleted
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove location: {e}")

async def get_user_info(uuid: str) -> User:
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT uuid, first_name, last_name, email, username, created_at
            FROM users
            WHERE uuid = %s
        """, (uuid,))

        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return None  # or raise 404 in the route

        return User(
            uuid=row[0],
            first_name=row[1],
            last_name=row[2],
            email=row[3],
            username=row[4],
            created_at=row[5]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user info: {e}")

async def get_user_preferences(user_id: int):
    # TODO: Replace with real database logic for user preferences
    return []


async def get_user_saved_events(user_uuid: str):
    """
    Fetch all saved events for a given user.
    Returns a list of events, each with id, event_type, payload, created_at.
    """
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, event_type, payload, created_at
            FROM user_events
            WHERE user_uuid = %s
            ORDER BY created_at DESC
            """,
            (user_uuid,)
        )

        rows = cur.fetchall()
        cur.close()
        conn.close()

        events = []
        for row in rows:
            event_id, event_type, payload_json, created_at = row

            # payload may already be a dict (psycopg2 auto-parses jsonb)
            try:
                payload = (
                    payload_json
                    if isinstance(payload_json, dict)
                    else json.loads(payload_json)
                )
            except Exception:
                payload = {}

            events.append({
                "id": event_id,
                "event_type": event_type,
                "payload": payload,
                "created_at": (
                    created_at.isoformat()
                    if isinstance(created_at, datetime)
                    else str(created_at)
                )
            })

        return events

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch saved events: {e}")



async def get_user_saved_event(user_uuid: str, event_id: int):
    """
    Fetch a single saved event for a given user by event ID.
    Returns id, event_type, payload, created_at.
    """
    try:
        conn = get_conn()
        cur = conn.cursor()


        cur.execute(
            """
            SELECT id, event_type, payload, created_at
            FROM user_events
            WHERE user_uuid = %s AND id = %s
            LIMIT 1
            """,
            (user_uuid, event_id)
        )

        row = cur.fetchone()

        cur.close()
        conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="Event not found")

        event_id, event_type, payload_json, created_at = row

        print(f"[DEBUG] Raw payload_json: {payload_json} (type: {type(payload_json)})")

        try:
            payload = json.loads(payload_json) if isinstance(payload_json, str) else payload_json
        except Exception as json_err:
            payload = {}


        return {
            "id": event_id,
            "event_type": event_type,
            "payload": payload,
            "created_at": created_at.isoformat()
                if isinstance(created_at, datetime)
                else str(created_at)
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Exception in get_user_saved_event: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch event: {e}")





async def update_user_preferences(user_id: int, options: List):
    return []


async def save_event(req, user_uuid: str):
    """
    Save a celestial event for the user and verify it was saved.
    req: Pydantic model with attributes:
         - event_type: str
         - payload: dict
    """
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Convert dict to JSON string
        payload_json = json.dumps(req.payload)

        # Insert event
        cur.execute(
            """
            INSERT INTO user_events (user_uuid, event_type, payload, created_at)
            VALUES (%s, %s, %s::jsonb, %s)
            RETURNING id
            """,
            (
                user_uuid,
                req.event_type,
                payload_json,
                datetime.utcnow()
            )
        )

        event_id = cur.fetchone()[0]
        conn.commit()

        # Verify event was saved
        cur.execute(
            """
            SELECT id, user_uuid, event_type, payload, created_at
            FROM user_events
            WHERE id = %s AND user_uuid = %s
            """,
            (event_id, user_uuid)
        )

        row = cur.fetchone()
        if not row:
            cur.close()
            conn.close()
            raise HTTPException(status_code=500, detail="Event was not saved properly!")

        db_event_id, db_user_uuid, db_event_type, db_payload, db_created_at = row

        cur.close()
        conn.close()

        return {
            "message": "Event saved successfully",
            "id": db_event_id,
            "user_uuid": db_user_uuid,
            "event_type": db_event_type,
            "payload": db_payload if isinstance(db_payload, dict) else json.loads(db_payload),
            "created_at": db_created_at.isoformat()
        }

    except Exception as e:
        if isinstance(e, errors.UniqueViolation):
            raise HTTPException(
                status_code=400,
                detail="This event has already been saved for this user."
            )
        raise HTTPException(status_code=500, detail=f"Failed to save event: {e}")


async def delete_event(user_uuid: str, event_id: int) -> bool:
    """
    Delete a saved event for a user.
    Returns True if deleted, False if event not found.
    """
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM user_events WHERE user_uuid = %s AND id = %s RETURNING id",
            (user_uuid, event_id)
        )
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return bool(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete event: {e}")