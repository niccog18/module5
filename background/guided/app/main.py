from fastapi import FastAPI
from app.routers.tasks_demo import router as tasks_router

app = FastAPI(title="Background Tasks Demo")

app.include_router(tasks_router)


@app.get("/")
def root():
    return {"message": "Background Tasks Demo"}