from fastapi import APIRouter, HTTPException

from app.schemas.recipe import Recipe, RecipeCreate

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)

recipes = []


@router.get("/", response_model=list[Recipe])
def get_recipes():
    return recipes


@router.get("/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: int):
    for recipe in recipes:
        if recipe["id"] == recipe_id:
            return recipe

    raise HTTPException(status_code=404, detail="Recipe not found")


@router.post("/", response_model=Recipe, status_code=201)
def create_recipe(recipe: RecipeCreate):
    new_recipe = recipe.model_dump()
    new_recipe["id"] = len(recipes) + 1

    recipes.append(new_recipe)

    return new_recipe