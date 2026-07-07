from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional

from app.schemas.book import Book, Genre, SortOption


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


books = [
    {
        "id": 1,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "genre": "fiction",
        "year": 1937
    },
    {
        "id": 2,
        "title": "A Brief History of Time",
        "author": "Stephen Hawking",
        "genre": "science",
        "year": 1988
    },
    {
        "id": 3,
        "title": "Sapiens",
        "author": "Yuval Noah Harari",
        "genre": "history",
        "year": 2011
    },
    {
        "id": 4,
        "title": "Clean Code",
        "author": "Robert Martin",
        "genre": "nonfiction",
        "year": 2008
    },
    {
        "id": 5,
        "title": "Dune",
        "author": "Frank Herbert",
        "genre": "fiction",
        "year": 1965
    },
    {
        "id": 6,
        "title": "The Selfish Gene",
        "author": "Richard Dawkins",
        "genre": "science",
        "year": 1976
    },
    {
        "id": 7,
        "title": "The Art of War",
        "author": "Sun Tzu",
        "genre": "history",
        "year": 500
    },
    {
        "id": 8,
        "title": "Atomic Habits",
        "author": "James Clear",
        "genre": "nonfiction",
        "year": 2018
    }
]


# GET /books
@router.get("/", response_model=list[Book])
def get_books(
    genre: Optional[Genre] = None,
    min_year: Optional[int] = Query(None, gt=0),
    max_year: Optional[int] = Query(None),
    search: Optional[str] = Query(None, min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=25)
):

    results = books

    # Filter genre
    if genre:
        results = [
            book for book in results
            if book["genre"] == genre.value
        ]

    # Minimum year
    if min_year:
        results = [
            book for book in results
            if book["year"] >= min_year
        ]

    # Maximum year
    if max_year:
        results = [
            book for book in results
            if book["year"] <= max_year
        ]

    # Search title
    if search:
        results = [
            book for book in results
            if search.lower() in book["title"].lower()
        ]

    # Pagination
    return results[skip:skip + limit]


# GET /books/{book_id}
@router.get("/{book_id}", response_model=Book)
def get_book(
    book_id: int = Path(gt=0)
):

    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


# GET /books/genre/{genre}
@router.get("/genre/{genre}", response_model=list[Book])
def get_books_by_genre(
    genre: Genre,
    sort_by: Optional[SortOption] = None
):

    results = [
        book for book in books
        if book["genre"] == genre.value
    ]

    if sort_by == SortOption.title:
        results.sort(
            key=lambda book: book["title"]
        )

    elif sort_by == SortOption.year:
        results.sort(
            key=lambda book: book["year"]
        )

    return results