from fastapi import FastAPI
from app.routers import recipes, ingredients

app = FastAPI(title="Recipe API")

app.include_router(recipes.router)
app.include_router(ingredients.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Recipe API!"}