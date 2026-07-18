from fastapi import APIRouter, Depends, Request

from app.schemas.user import UserResponse
from app.utils.security import get_current_user
from app.utils.limiter import limiter


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current authenticated user",
    responses={
        401: {
            "description": "Not authenticated. A valid JWT Bearer token is required."
        },
        429: {
            "description": "Rate limit exceeded."
        },
    },
)
@limiter.limit("60/minute")
def me(
    request: Request,
    user=Depends(get_current_user),
):
    """
    Retrieve the profile information of the currently authenticated user.

    This endpoint requires a valid JWT access token.

    Authorization header format:

    Bearer <access_token>

    Returns the user's ID and username.
    """
    return {
        "id": user.id,
        "username": user.username,
    }