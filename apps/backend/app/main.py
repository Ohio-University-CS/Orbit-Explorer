from fastapi import FastAPI
from app.api import user_router, event_router, auth_router

app = FastAPI(title="Orbit-Explorer API")

# Register routers
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(event_router, prefix="/events", tags=["events"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])