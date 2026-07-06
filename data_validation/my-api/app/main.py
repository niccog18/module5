from fastapi import FastAPI
from app.routers import tasks

app = FastAPI(title="Task API")

app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Expanding API Complexity!"}