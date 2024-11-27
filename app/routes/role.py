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
    return await RoleService.get_all_roles(role_id)

@roleRouter.post("/", status_code=201, response_model=PydanticRoleModel)
async def add_role( body: PydanticCreateRoleModel ) -> PydanticRoleModel:
    """
    This method creates a new role.
    """
    return None

@roleRouter.patch("/{role_id}", status_code=205, response_model=PydanticRoleModel)
async def modify_role( role_id: int) -> PydanticRoleModel:
    """
    This method modifies the role of the given role id.
    """
    return None


@roleRouter.delete("/{role_id}", status_code=204, response_model=PydanticRoleModel)
async def delete_role( role_id: int) -> PydanticRoleModel:
    """
    This method deletes the role of the given role id.
    """
    return None


