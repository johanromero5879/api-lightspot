from fastapi import APIRouter, Depends

from app.auth.infrastructure import get_current_user
from app.user.domain import UserOut

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me")
async def get_my_info(
    user: UserOut = Depends(get_current_user)
):
    return user
