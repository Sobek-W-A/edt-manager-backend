"""
This module provieds a router for the /role endpoint.
"""
from fastapi import APIRouter

from app.models.aliases import AuthenticatedAccount
from app.models.pydantic.RoleModel import (PydanticCreateRoleModel,
                                              PydanticUpdateRoleModel,
                                              PydanticRoleResponseModel)
from app.routes.tags import Tag
from app.services import RoleService


roleRouter: APIRouter = APIRouter(prefix="/role")
tag: Tag = {
    "name": "Role",
    "description": "Role-related operations."
}


@roleRouter.get("/", status_code=200, response_model=list[PydanticRoleResponseModel])
async def get_all_roles(academic_year: int,
                        current_account: AuthenticatedAccount) -> list[PydanticRoleResponseModel]:
    """
    This method returns all the roles.
    """
    return await RoleService.get_all_roles(academic_year, current_account)


@roleRouter.get("/{role_name}", status_code=200, response_model=PydanticRoleResponseModel)
async def get_role_by_name(academic_year: int,
                           role_name: str,
                           current_account: AuthenticatedAccount) -> PydanticRoleResponseModel:
    """
    This method returns the role of the given role name.
    """
    return await RoleService.get_role_by_id(academic_year, role_name, current_account)

@roleRouter.post("/", status_code=201, response_model=None)
async def add_role(academic_year: int,
                   body: PydanticCreateRoleModel,
                   current_account: AuthenticatedAccount) -> None:
    """
    This method creates a new role.
    """
    await RoleService.add_role(academic_year, body, current_account)

@roleRouter.patch("/{role_name}", status_code=205, response_model=None)
async def modify_role(academic_year: int,
                      body : PydanticUpdateRoleModel,
                      role_name: str,
                      current_account: AuthenticatedAccount) -> None :
    """
    This method modifies the role of the given role id.
    """
    await RoleService.modify_role(academic_year, role_name, body, current_account)

@roleRouter.delete("/{role_name}", status_code=204, response_model=None)
async def delete_role(academic_year: int,
                      role_name: str,
                      current_account: AuthenticatedAccount) -> None:
    """
    This method deletes the role of the given role id.
    """
    await RoleService.delete_role(academic_year, role_name, current_account)
