"""Main FastAPI application for the AI-Ready Task Manager API."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import Base, engine
from app.routers import auth, tasks, users
from app.models import user, task
from app.exceptions import (
    NotFoundException,
    DuplicateException,
    ForbiddenException,
)


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI-Ready Task Manager API",
    description=(
        "A production-quality task management API "
        "with JWT authentication, user-scoped CRUD operations, "
        "and an AI-ready suggestion endpoint."
    ),
    version="1.0.0",
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Global Exception Handlers
# -------------------------

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(
    request: Request,
    exc: NotFoundException,
):
    """Handle missing resources."""

    return JSONResponse(
        status_code=404,
        content={
            "error": "not_found",
            "message": str(exc),
        },
    )


@app.exception_handler(DuplicateException)
async def duplicate_exception_handler(
    request: Request,
    exc: DuplicateException,
):
    """Handle duplicate resource errors."""

    return JSONResponse(
        status_code=409,
        content={
            "error": "duplicate",
            "message": exc.message,
        },
    )


@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(
    request: Request,
    exc: ForbiddenException,
):
    """Handle unauthorized resource access."""

    return JSONResponse(
        status_code=403,
        content={
            "error": "forbidden",
            "message": str(exc),
        },
    )


# -------------------------
# Routers
# -------------------------

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)

app.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["Tasks"],
)

app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

# -------------------------
# Health Check
# -------------------------

@app.get(
    "/",
    tags=["Health"],
    summary="Health check",
)
def health_check() -> dict[str, str]:
    """
    Verify that the API is running.

    Returns:
        API status message.
    """

    return {
        "status": "ok",
        "message": "Task Manager API is running",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )