from fastapi import FastAPI
from app.config import settings
from app.routers import contacts

app = FastAPI(
    title=settings.app_name,
    description="A Validated Contact API",
    version="0.1.0"
)

app.include_router(contacts.router)

@app.get("/")
def root():
    return {"app": settings.app_name, "docs": "/docs"}