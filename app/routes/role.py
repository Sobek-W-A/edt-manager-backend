"""
This module provieds a router for the /role endpoint.
"""
from fastapi import APIRouter

from app.models.pydantic.RoleModel import PydanticRoleModel,PydanticCreateRoleModel
from app.routes.tags import Tag
from app.services import RoleService

roleRouter: APIRouter = APIRouter(prefix="/role")
tag: Tag = {
    "name": "Role",
    "description": "Role-related operations."
}

@roleRouter.get("/", status_code=200, response_model=list[PydanticRoleModel])
async def get_all_roles() -> list[PydanticRoleModel]:
    """
    This method returns all the roles.
    """
    return await RoleService.get_all_roles()


@roleRouter.get("/{role_id}", status_code=200, response_model=PydanticRoleModel)
async def get_role_by_id(role_id: int) -> PydanticRoleModel:
    """
    This method returns the role of the given role id.
    """
    return await RoleService.get_role_by_id(role_id)

@roleRouter.post("/", status_code=201, response_model=PydanticRoleModel)
async def add_role( body: PydanticCreateRoleModel ) -> PydanticRoleModel:
    """
    This method creates a new role.
    """
    return await RoleService.add_role(body)

@roleRouter.patch("/{role_id}", status_code=205)
async def modify_role(body : PydanticCreateRoleModel, role_id: int) -> None :
    """
    This method modifies the role of the given role id.
    """
    await RoleService.modify_role(role_id, body)


@roleRouter.delete("/{role_id}", status_code=204)
async def delete_role( role_id: int) -> None:
    """
    This method deletes the role of the given role id.
    """
    await RoleService.delete_role(role_id)


