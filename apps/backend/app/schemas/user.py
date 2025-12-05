from typing import Optional
from pydantic import BaseModel, EmailStr, model_validator

class User(BaseModel):
    uuid: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    created_at: Optional[int] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None