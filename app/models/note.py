"""Note model for file storage."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import Index, Text, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class Note(Base):
    """Note model representing a stored note.

    Attributes:
        id: Unique identifier (UUID)
        session_id: Optional session identifier for AI-generated notes
        filename: Name of the note
        content: Content of the note
        created_at: Timestamp when the note was created
        updated_at: Timestamp when the note was last updated
    """

    __tablename__ = "notes"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        comment="Unique identifier",
    )
    session_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
        index=True,
        comment="Optional session ID for AI-generated notes",
    )
    filename: Mapped[str] = mapped_column(
        index=True,
        comment="Name of the Note",
    )
    content: Mapped[str] = mapped_column(
        Text,
        comment="Content of the Note",
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        comment="Timestamp when created",
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        comment="Timestamp when last updated",
    )

    __table_args__ = (
        Index("idx_notes_created_at", "created_at", postgresql_ops={"created_at": "DESC"}),
    )

    def __repr__(self) -> str:
        """String representation of Note."""
        return f"<Note(id={self.id}, filename={self.filename}, session_id={self.session_id})>"
