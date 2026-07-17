from fastapi import APIRouter, Depends, Request


from app.utils.security import get_current_user
from app.utils.limiter import limiter

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
@limiter.limit("60/minute")
def me(
    request: Request,
    user=Depends(get_current_user)):
    return {
        "id": user.id,
        "username": user.username,
    }