"""
This module provieds a router for the /role endpoint.
"""
from fastapi import APIRouter

from app.models.pydantic.ClassicModel import ClassicModel
from app.models.pydantic.RoleModel import PydanticRoleModel,PydanticCreateRoleModel
from app.routes.tags import Tag
from app.services import RoleService

roleRouter: APIRouter = APIRouter(prefix="/role")
tag: Tag = {
    "name": "Role",
    "description": "Role-related operations."
}

@roleRouter.get("/", status_code=200, response_model=list[ClassicModel])
async def get_all_roles() -> list[ClassicModel]:
    """
    This method returns all the roles.
    """
    return await RoleService.get_all_roles()


@roleRouter.get("/{role_name}", status_code=200, response_model=ClassicModel)
async def get_role_by_id(role_name: str) -> ClassicModel:
    """
    This method returns the role of the given role name.
    """
    return await RoleService.get_role_by_id(role_name)

@roleRouter.post("/", status_code=201)
async def add_role( body: PydanticCreateRoleModel ) -> None:
    """
    This method creates a new role.
    """
    await RoleService.add_role(body)

@roleRouter.patch("/{role_id}", status_code=205)
async def modify_role(body : PydanticCreateRoleModel, role_id: int) -> None :
    """
    This method modifies the role of the given role id.
    """
    await RoleService.modify_role(role_id, body)


@roleRouter.delete("/{role_name}", status_code=204)
async def delete_role( role_name: str) -> None:
    """
    This method deletes the role of the given role id.
    """
    await RoleService.delete_role(role_name)


