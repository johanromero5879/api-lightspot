from fastapi import APIRouter, Depends, HTTPException, status, Security
from dependency_injector.wiring import Provide, inject

from app.auth.infrastructure import get_current_user
from app.role.domain import Permission
from app.role.application import FindRole, RoleNotFound
from app.user.domain import UserOut, UserIn, UserList
from app.user.application import RegisterUser, EmailFoundError, SendEmailToNewUser, FindUsers

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me")
async def get_my_info(
    user: UserOut = Depends(get_current_user)
):
    return user


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[Permission.REGISTER_USERS])]
)
@inject
async def create_user(
    user: UserIn,
    find_role: FindRole = Depends(Provide["services.find_role"]),
    register_user: RegisterUser = Depends(Provide["services.register_user"]),
    send_email_to_new_user: SendEmailToNewUser = Depends(Provide["services.send_email_to_new_user"])
):
    try:
        role = find_role(name=user.role)
        user.role = role.id

        user = await register_user(user)
        send_email_to_new_user(user)

    except EmailFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )
    except RoleNotFound as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.get(
    path="/",
    response_model=UserList,
    dependencies=[Security(get_current_user, scopes=[Permission.GET_USERS])]
)
@inject
async def get_users(
    limit: int = 5,
    page: int = 1,
    find_users: FindUsers = Depends(Provide["services.find_users"])
):
    try:
        return find_users(limit, page)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
