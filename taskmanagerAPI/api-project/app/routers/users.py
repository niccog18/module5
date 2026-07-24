"""User profile endpoints."""

from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse


router = APIRouter()


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Return the authenticated user's profile.
    """

    return current_user