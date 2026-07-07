from fastapi import FastAPI
from app.routers import products

app = FastAPI(title="Task API")

app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "Building a Flexible Product Search API!"}