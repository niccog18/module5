from fastapi import FastAPI
from app.routers import books

app = FastAPI(
    title="Library Search API"
)

app.include_router(
    books.router
)

@app.get("/")
def home():
    return {
        "message": "Library API running"
    }