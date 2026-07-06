from pydantic import BaseModel

class IngredientCreate(BaseModel):
    """ Schema for creating a new ingredient."""
    name: str
    category: str

class Ingredient(IngredientCreate):
    """ Schema for retrieving an ingredient with an ID"""
    id: int