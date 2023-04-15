from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from app.role.application import FindRoles

router = APIRouter(
    prefix="/roles",
    tags=["roles"]
)


@router.get("/")
@inject
async def get_roles(
    find_roles: FindRoles = Depends(Provide["services.find_roles"])
):
    return find_roles()
