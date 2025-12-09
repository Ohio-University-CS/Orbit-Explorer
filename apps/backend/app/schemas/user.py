from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Any, Dict, Optional

from app.services.auth import get_current_user_uuid
from datetime import datetime

class User(BaseModel):
    uuid: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    created_at: Optional[datetime] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserLocation(BaseModel):
    id: int | None = None
    user_uuid: str
    loc_name: str | None = None
    loc_description: str | None = None
    latitude: float
    longitude: float
    alt_km: float

class UserLocationRequest(BaseModel):
    loc_name: str | None = None
    loc_description: str | None = None
    latitude: float
    longitude: float
    alt_km: float


class EventSaveRequest(BaseModel):
    event_type: str
    payload: Dict[str, Any]

class EventRemoveRequest(BaseModel):
    id: int