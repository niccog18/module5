from fastapi import APIRouter, Depends, HTTPException, Request

from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

from app.schemas.auth import (
    RegisterRequest,
    TokenResponse,
)

from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.utils.limiter import limiter


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    responses={
        400: {
            "description": "Username already exists"
        },
        422: {
            "description": "Validation error"
        },
    },
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    """
    Register a new user account.

    The username must be unique.
    Passwords are securely hashed before being stored
    in the database.

    Errors:
    - 400: Username already exists.
    - 422: Invalid registration data.
    """

    existing = (
        db.query(User)
        .filter(User.username == request.username)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    user = User(
        username=request.username,
        hashed_password=hash_password(
            request.password
        ),
    )

    db.add(user)
    db.commit()

    return {
        "message": "User registered"
    }


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate user and receive JWT token",
    responses={
        401: {
            "description": "Invalid username or password"
        },
        422: {
            "description": "Validation error"
        },
        429: {
            "description": "Rate limit exceeded"
        },
    },
)
@limiter.limit("50/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and generate a JWT access token.

    The returned token must be included in the Authorization
    header for protected endpoints.

    Example:

    Bearer <access_token>

    Errors:
    - 401: Invalid login credentials.
    - 422: Invalid request format.
    """

    user = (
        db.query(User)
        .filter(User.username == form_data.username)
        .first()
    )

    if (
        not user
        or not verify_password(
            form_data.password,
            user.hashed_password,
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = create_access_token(
        {"sub": user.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }