"""Note service for CRUD operations."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate


class NoteService:
    """Service for managing notes."""

    def __init__(self, db: AsyncSession):
        """Initialize note service.

        Args:
            db: Database session
        """
        self.db = db

    async def create(self, note_data: NoteCreate) -> Note:
        """Create a new note.

        Args:
            note_data: Note creation data

        Returns:
            Created note
        """
        note = Note(
            title=note_data.title,
            content=note_data.content,
            session_id=note_data.session_id,
        )
        self.db.add(note)
        await self.db.commit()
        await self.db.refresh(note)
        return note

    async def get_by_id(self, note_id: UUID) -> Note | None:
        """Get a note by ID.

        Args:
            note_id: Note UUID

        Returns:
            Note if found, None otherwise
        """
        result = await self.db.execute(select(Note).where(Note.id == note_id))
        return result.scalar_one_or_none()

    async def get_list(
        self,
        page: int = 1,
        session_id: UUID | None = None,
    ) -> tuple[list[Note], int]:
        """Get paginated list of notes.

        Args:
            page: Page number (1-indexed)
            session_id: Optional session ID filter

        Returns:
            Tuple of (notes list, total count)
        """
        # Fixed limit: 10 notes per page
        limit = 10
        # Calculate offset: (page - 1) * limit
        offset = (page - 1) * limit

        # Build base query
        query = select(Note)
        count_query = select(func.count()).select_from(Note)

        # Apply session_id filter if provided
        if session_id is not None:
            query = query.where(Note.session_id == session_id)
            count_query = count_query.where(Note.session_id == session_id)

        # Order by created_at DESC (newest first)
        query = query.order_by(Note.created_at.desc())

        # Apply pagination
        query = query.offset(offset).limit(limit)

        # Execute queries
        notes_result = await self.db.execute(query)
        notes = list(notes_result.scalars().all())

        count_result = await self.db.execute(count_query)
        total = count_result.scalar_one()

        return notes, total

    async def update(self, note_id: UUID, note_data: NoteUpdate) -> Note | None:
        """Update a note.

        Args:
            note_id: Note UUID
            note_data: Note update data

        Returns:
            Updated note if found, None otherwise
        """
        note = await self.get_by_id(note_id)
        if note is None:
            return None

        # Update fields if provided
        if note_data.title is not None:
            note.title = note_data.title
        if note_data.content is not None:
            note.content = note_data.content

        await self.db.commit()
        await self.db.refresh(note)
        return note

    async def delete(self, note_id: UUID) -> bool:
        """Delete a note.

        Args:
            note_id: Note UUID

        Returns:
            True if deleted, False if not found
        """
        note = await self.get_by_id(note_id)
        if note is None:
            return False

        await self.db.delete(note)
        await self.db.commit()
        return True
