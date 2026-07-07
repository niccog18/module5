from pydantic import BaseModel, Field
from enum import Enum


class Genre(str, Enum):
    fiction = "fiction"
    nonfiction = "nonfiction"
    science = "science"
    history = "history"


class SortOption(str, Enum):
    title = "title"
    year = "year"


class Book(BaseModel):
    id: int = Field(gt=0)
    title: str
    author: str
    genre: Genre
    year: int = Field(gt=0)