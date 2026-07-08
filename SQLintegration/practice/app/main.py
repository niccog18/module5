from fastapi import FastAPI

from app.database import Base, engine
from app.routers.notes import router as notes_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes API")

app.include_router(notes_router)


@app.get("/")
def root():
    return {"message": "Notes API is running"}