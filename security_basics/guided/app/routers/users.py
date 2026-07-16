from fastapi import APIRouter, Depends

from app.utils.security import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
def me(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "username": user.username,
    }