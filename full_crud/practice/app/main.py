"""
Main FastAPI application file.

Responsible for:
- Creating the FastAPI application
- Creating database tables
- Registering API routers
"""

from fastapi import FastAPI
from app.database import Base, engine
from app.routers.students import router as student_router

# Creates database tables automatically
Base.metadata.create_all(
    bind=engine
)

# Initialize FastAPI application
app = FastAPI(
    title="Student CRUD API",
    description="Database-backed API for managing students"
)

# Register student CRUD routes
app.include_router(
    student_router
)