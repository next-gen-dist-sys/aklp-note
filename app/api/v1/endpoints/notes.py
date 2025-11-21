"""Note API endpoints."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.core.deps import DBSession
from app.schemas.note import NoteCreate, NoteListResponse, NoteResponse, NoteUpdate
from app.services.note_service import NoteService

router = APIRouter()

# Fixed limit: 10 notes per page
NOTES_PER_PAGE = 10


@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
)
async def create_note(
    note_data: NoteCreate,
    db: DBSession,
) -> NoteResponse:
    """Create a new note.

    Args:
        note_data: Note creation data
        db: Database session

    Returns:
        Created note
    """
    service = NoteService(db)
    note = await service.create(note_data)
    return NoteResponse.model_validate(note)


@router.get(
    "",
    response_model=NoteListResponse,
    summary="Get list of notes",
)
async def list_notes(
    db: DBSession,
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    session_id: UUID | None = Query(default=None, description="Filter by session ID"),
) -> NoteListResponse:
    """Get paginated list of notes.

    Args:
        db: Database session
        page: Page number (1-indexed)
        session_id: Optional session ID filter

    Returns:
        Paginated note list
    """
    service = NoteService(db)
    notes, total = await service.get_list(page=page, session_id=session_id)

    return NoteListResponse(
        items=[NoteResponse.model_validate(note) for note in notes],
        total=total,
        page=page,
        limit=NOTES_PER_PAGE,
    )


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Get a note by ID",
)
async def get_note(
    note_id: UUID,
    db: DBSession,
) -> NoteResponse:
    """Get a note by ID.

    Args:
        note_id: Note UUID
        db: Database session

    Returns:
        Note details

    Raises:
        HTTPException: 404 if note not found
    """
    service = NoteService(db)
    note = await service.get_by_id(note_id)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note {note_id} not found",
        )

    return NoteResponse.model_validate(note)


@router.put(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Update a note",
)
async def update_note(
    note_id: UUID,
    note_data: NoteUpdate,
    db: DBSession,
) -> NoteResponse:
    """Update a note.

    Args:
        note_id: Note UUID
        note_data: Note update data
        db: Database session

    Returns:
        Updated note

    Raises:
        HTTPException: 404 if note not found
    """
    service = NoteService(db)
    note = await service.update(note_id, note_data)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note {note_id} not found",
        )

    return NoteResponse.model_validate(note)


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
)
async def delete_note(
    note_id: UUID,
    db: DBSession,
) -> None:
    """Delete a note.

    Args:
        note_id: Note UUID
        db: Database session

    Raises:
        HTTPException: 404 if note not found
    """
    service = NoteService(db)
    deleted = await service.delete(note_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note {note_id} not found",
        )
