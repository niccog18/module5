from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User
from app.routers import auth, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="JWT Auth Demo")

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "JWT Authentication Demo is running"}
