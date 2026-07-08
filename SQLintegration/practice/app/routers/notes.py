from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteResponse

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


@router.post("/", response_model=NoteResponse, status_code=201)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db)
):
    db_note = Note(**note.model_dump())

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note


@router.get("/", response_model=list[NoteResponse])
def get_notes(
    category: str | None = None,
    is_pinned: bool | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Note)

    if category is not None:
        query = query.filter(Note.category == category)

    if is_pinned is not None:
        query = query.filter(Note.is_pinned == is_pinned)

    return query.all()


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(Note.id == note_id).first()

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return note


@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(Note.id == note_id).first()

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    db.delete(note)
    db.commit()

    return {"message": "Note deleted"}