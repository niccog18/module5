from fastapi import APIRouter, Depends, HTTPException, Request

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db

from app.models.user import User

from app.schemas.auth import RegisterRequest

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


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):

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

    return {"message": "User registered"}


@router.post("/login")
@limiter.limit("50/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

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