from pydantic import BaseModel

class RecipeCreate(BaseModel):
    """ Schema for creating a new recipe."""
    title: str
    cuisine: str
    prep_time_minutes: int
    servings: int

class Recipe(RecipeCreate):
    """ Schema for retrieving a recipe with an ID."""
    id: int