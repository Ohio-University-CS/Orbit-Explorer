from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import user_router, event_router, auth_router

app = FastAPI(title="Orbit-Explorer API")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3003",
    "http://127.0.0.1:3003",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(event_router, prefix="/events", tags=["events"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
