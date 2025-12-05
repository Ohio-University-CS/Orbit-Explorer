from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.auth import create_access_token
from app.services.user import create_user, user_login
from app.schemas.user import LoginRequest, RegisterRequest, User
router = APIRouter()

@router.post("/login")
async def login(login_request: LoginRequest) -> dict:
    user = await user_login(login_request)
    access_token = create_access_token(data={"sub": user.uuid})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register(new_user: RegisterRequest) -> dict:
    user = await create_user(new_user)
    access_token = create_access_token(data={"sub": user.uuid})
    return {"uuid:": user.uuid, "access_token": access_token, "token_type": "bearer"}