from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    isbn: Optional[str] = Field(default=None, min_length=10, max_length=13)
    price: float = Field(gt=0)
    pages: Optional[int] = Field(default=None, gt=0)

class BookUpdate(BaseModel):
    """Full update — all fields required (except optional ones)."""
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    isbn: Optional[str] = Field(default=None, min_length=10, max_length=13)
    price: float = Field(gt=0)
    pages: Optional[int] = Field(default=None, gt=0)

class BookPatch(BaseModel):
    """Partial update — all fields optional."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    author: Optional[str] = Field(default=None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(default=None, min_length=10, max_length=13)
    price: Optional[float] = Field(default=None, gt=0)
    pages: Optional[int] = Field(default=None, gt=0)

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: Optional[str]
    price: float
    pages: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True