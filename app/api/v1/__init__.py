"""API v1 package."""

from fastapi import APIRouter

from app.api.v1.endpoints import notes

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
