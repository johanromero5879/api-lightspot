from dependency_injector.wiring import Provide, inject

from app.role.domain import BaseRole, RoleRepository, RoleOut, Permission


@inject
def check_roles(
    role_repository: RoleRepository = Provide["repositories.role"]
):
    default_roles = [
        BaseRole(
            name="admin",
            permissions=[
                Permission.UPLOAD_FLASHES_DATA,
                Permission.GENERATE_FLASHES_REPORT,
                Permission.REMOVE_MY_UPLOADED_FLASHES,
                Permission.REGISTER_USERS
            ]
        )
    ]

    roles = role_repository.find_all()

    if len(roles) > 0:
        update_permissions(roles, default_roles)
    else:
        create_roles(default_roles)


@inject
def update_permissions(
    roles: list[RoleOut],
    default_roles: list[BaseRole],
    role_repository: RoleRepository = Provide["repositories.role"]
):
    for role in roles:
        # Search for role name in default_roles list to get permissions list
        role_found = next(filter(lambda r: r.name == role.name, default_roles), None)

        if role_found and len(role_found.permissions) > 0:
            role_repository.replace_permissions(role.id, role_found.permissions)


@inject
def create_roles(
    roles: list[BaseRole],
    role_repository: RoleRepository = Provide["repositories.role"]
):
    role_repository.insert_many(roles)

