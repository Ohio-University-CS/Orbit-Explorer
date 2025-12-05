from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import List
import psycopg2
import uuid
from passlib.context import CryptContext
from app.schemas.location import GeodeticLocation
from app.schemas.user import LoginRequest, RegisterRequest, User

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

# Get saved locations for a user (mocked data for now)
async def get_user_saved_locations(user_id: int):
    # TODO: Replace with real database logic for saved locations
    return [
        GeodeticLocation(lon=-82, lat=39, elevation=100),
        GeodeticLocation(lon=-82, lat=39.2, elevation=200),
    ]

# Save a user's location to the database
async def save_user_location(user_id: int, loc: GeodeticLocation, name: str):
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Insert location for the user
        cur.execute(
            "INSERT INTO user_locations (user_id, name, latitude, longitude, elevation) VALUES (%s, %s, %s, %s, %s)",
            (user_id, name, loc.lat, loc.lon, loc.elevation)
        )
        conn.commit()

        cur.close()
        conn.close()

        return {"message": "Location saved successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save location: {e}")


async def get_user_info(uuid: str):
    return User()

async def get_user_preferences(user_id: int):
    # TODO: Replace with real database logic for user preferences
    return []

async def get_user_saved_events(user_id: int):
    # TODO: Replace with real database logic for user events
    return []

async def update_user_preferences(user_id: int, options: List):
    return []