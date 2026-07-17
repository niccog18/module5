from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from app.database import get_db
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate, BookPatch, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])


def get_book_or_404(db: Session, book_id: int) -> Book:
    """Helper: fetch a book or raise 404."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# CREATE
@router.post("/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.model_dump())
    try:
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A book with this ISBN already exists")
    return db_book


# READ (many)
@router.get("/", response_model=list[BookResponse])
def list_books(
    author: Optional[str] = None,
    min_price: Optional[float] = Query(default=None, ge=0),
    max_price: Optional[float] = Query(default=None, ge=0),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Book)
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if min_price is not None:
        query = query.filter(Book.price >= min_price)
    if max_price is not None:
        query = query.filter(Book.price <= max_price)
    return query.offset(skip).limit(limit).all()


# READ (one)
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return get_book_or_404(db, book_id)


# UPDATE (full — PUT)
@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db)):
    db_book = get_book_or_404(db, book_id)
    for field, value in book_data.model_dump().items():
        setattr(db_book, field, value)
    db.commit()
    db.refresh(db_book)
    return db_book


# UPDATE (partial — PATCH)
@router.patch("/{book_id}", response_model=BookResponse)
def patch_book(book_id: int, book_data: BookPatch, db: Session = Depends(get_db)):
    db_book = get_book_or_404(db, book_id)
    update_data = book_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
    db.commit()
    db.refresh(db_book)
    return db_book


# DELETE
@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = get_book_or_404(db, book_id)
    db.delete(db_book)
    db.commit()