from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.auth.schemas import UserResponse
from app.users.models import User


router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user