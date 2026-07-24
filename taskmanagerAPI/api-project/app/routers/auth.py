"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user

from app.utils.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.exceptions import DuplicateException
from app.database import get_db
from app.models.user import User
from app.schemas.user import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)

router = APIRouter()


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Register a new user.

    Creates a user account with a securely hashed password.

    Returns a JWT access token upon successful registration.
    """

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise DuplicateException(
    "Email already registered"
)

    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(
            user.password
        ),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = create_access_token(
        {
            "sub": str(db_user.id)
        }
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login",
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Authenticate a user.

    Returns a JWT access token if the
    supplied credentials are valid.
    """

    user = (
        db.query(User)
        .filter(User.email == credentials.email)
        .first()
    )

    if (
        user is None
        or not verify_password(
            credentials.password,
            user.hashed_password,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )
