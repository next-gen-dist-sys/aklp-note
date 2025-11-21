"""Pydantic schemas package."""

from app.schemas.note import (
    NoteCreate,
    NoteListResponse,
    NoteResponse,
    NoteUpdate,
)
from app.schemas.responses import (
    BaseResponse,
    ErrorResponse,
    HealthResponse,
    SuccessResponse,
)

__all__ = [
    # Note schemas
    "NoteCreate",
    "NoteUpdate",
    "NoteResponse",
    "NoteListResponse",
    # Response schemas
    "BaseResponse",
    "SuccessResponse",
    "ErrorResponse",
    "HealthResponse",
]
