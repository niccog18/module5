from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class Category(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    books = "books"
    food = "food"

class SortField(str, Enum):
    name = "name"
    price = "price"
    rating = "rating"

class ProductResponse(BaseModel):
    id: int
    name: str
    category: Category
    price: float
    rating: float