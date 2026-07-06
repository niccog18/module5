from fastapi import APIRouter

from app.schemas.ingredient import Ingredient, IngredientCreate

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"]
)

ingredients = []


@router.get("/", response_model=list[Ingredient])
def get_ingredients():
    return ingredients


@router.post("/", response_model=Ingredient, status_code=201)
def create_ingredient(ingredient: IngredientCreate):
    new_ingredient = ingredient.model_dump()
    new_ingredient["id"] = len(ingredients) + 1

    ingredients.append(new_ingredient)

    return new_ingredient