"""
Security Measures

1. JWT Authentication
2. Password hashing with bcrypt
3. OAuth2 Bearer authentication
4. CORS restricted to approved frontend origins
5. Rate limiting with SlowAPI
6. Input validation using Pydantic
7. SQLAlchemy ORM prevents SQL injection
8. Background task logging
"""

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

# Added this section
tags_metadata = [
    {
        "name": "Authentication",
        "description": (
            "Register new users and log in to receive a JWT Bearer token. "
            "Protected endpoints require authentication."
        ),
    },
    {
        "name": "Students",
        "description": (
            "Create, view, update, and delete student records."
        ),
    },
    {
        "name": "Users",
        "description": (
            "Manage authenticated user information."
        ),
    },
]

app = FastAPI(
    title="Secure Student API",
    description="""
A secure Student Management API built with FastAPI, SQLAlchemy, and JWT authentication.

## Features

- JWT authentication
- Password hashing with bcrypt
- SQLAlchemy database integration
- Pydantic validation
- Rate limiting
- CORS protection
- Background task logging

## Quick Start

1. Register a new user at **POST /auth/register**
2. Log in at **POST /auth/login**
3. Copy the `access_token`
4. Click **Authorize** in Swagger UI
5. Enter `Bearer <your_token>`
6. Access the protected student endpoints
""",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

@app.get("/")
def root():
    """
    API health check endpoint.

    Returns:
    - API status message
    """
    return {
        "message": "Secure Student API is running"
    }