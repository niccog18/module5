from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.utils.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_router)

app.include_router(student_router)

app.include_router(user_router)


@app.get("/")
def root():
    return {
        "message": "Secure Student API"
    }