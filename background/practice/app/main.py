from fastapi import FastAPI

from app.database import Base, engine

from app.routers.students import router as student_router

from app.routers.auth import router as auth_router

from app.routers.users import router as user_router

import app.models.student
import app.models.user

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure Student API"
)

app.include_router(auth_router)

app.include_router(student_router)

app.include_router(user_router)


@app.get("/")
def root():
    return {
        "message": "Secure Student API"
    }