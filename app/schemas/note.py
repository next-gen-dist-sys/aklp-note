"""Note schema definitions."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, computed_field


class NoteCreate(BaseModel):
    """Schema for creating a new note.

    Attributes:
        title: Title of the note (1-255 characters)
        content: Content of the note (at least 1 character)
        session_id: Optional session ID for AI-generated notes
    """

    title: str = Field(min_length=1, max_length=255, description="Title of the note")
    content: str = Field(min_length=1, description="Content of the note")
    session_id: UUID | None = Field(
        default=None, description="Optional session ID for AI-generated notes"
    )


class NoteUpdate(BaseModel):
    """Schema for updating an existing note.

    Attributes:
        title: Updated title (optional)
        content: Updated content (optional)

    Note:
        At least one field should be provided, but empty updates are allowed.
    """

    title: str | None = Field(
        default=None, min_length=1, max_length=255, description="Updated title"
    )
    content: str | None = Field(default=None, min_length=1, description="Updated content")


class NoteResponse(BaseModel):
    """Schema for note response.

    Attributes:
        id: Unique identifier
        session_id: Optional session ID for AI-generated notes
        title: Title of the note
        content: Content of the note
        created_at: Timestamp when the note was created
        updated_at: Timestamp when the note was last updated
    """

    id: UUID
    session_id: UUID | None
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class NoteListResponse(BaseModel):
    """Schema for paginated note list response.

    Attributes:
        items: List of notes
        total: Total number of notes
        page: Current page number
        limit: Number of items per page
        total_pages: Total number of pages (computed)
        has_next: Whether there is a next page (computed)
        has_prev: Whether there is a previous page (computed)
    """

    items: list[NoteResponse]
    total: int = Field(description="Total number of notes")
    page: int = Field(ge=1, description="Current page number")
    limit: int = Field(ge=1, description="Number of items per page")

    @computed_field  # type: ignore
    @property
    def total_pages(self) -> int:
        """Calculate total number of pages."""
        return (self.total + self.limit - 1) // self.limit if self.total > 0 else 1

    @computed_field  # type: ignore
    @property
    def has_next(self) -> bool:
        """Check if there is a next page."""
        return self.page < self.total_pages

    @computed_field  # type: ignore
    @property
    def has_prev(self) -> bool:
        """Check if there is a previous page."""
        return self.page > 1
