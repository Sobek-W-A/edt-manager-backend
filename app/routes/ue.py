"""
UE routes.
Used to manage ue operations.
"""

from fastapi import APIRouter

from app.models.aliases import AuthenticatedAccount
from app.models.pydantic.UEModel import (
    PydanticUEModel,
    PydanticCreateUEModel,
    PydanticModifyUEModel,
)
from app.routes.tags import Tag
from app.services import UEService


ueRouter: APIRouter = APIRouter(prefix="/ue")
tag: Tag = {"name": "UE", "description": "UE-related operations."}


@ueRouter.get("/{ue_id}", status_code=200, response_model=PydanticUEModel)
async def get_ue_by_id(
    ue_id: int, current_account: AuthenticatedAccount
) -> PydanticUEModel:
    """
    This method returns the UE of the given UE id.
    """
    return await UEService.get_ue_by_id(ue_id, current_account)


@ueRouter.get("/affectedto/{profile_id}", status_code=200, response_model=list[PydanticUEModel])
async def get_ue_by_affected_profile(
    academic_year: int,
    profile_id: int, current_account: AuthenticatedAccount
) -> list[PydanticUEModel]:
    """
    This method returns the UEs affected to the given profile id.
    """
    return await UEService.get_ue_by_affected_profile(academic_year, profile_id, current_account)


@ueRouter.post("/", status_code=201)
async def add_ue(
    body: PydanticCreateUEModel, current_account: AuthenticatedAccount
) -> None:
    """
    This method creates a new UE.
    """
    await UEService.add_ue(body, current_account)

@ueRouter.post("/attach/{ue_id}/{node_id}", status_code=201, response_model=None)
async def attach_ue_to_node(academic_year: int,
    ue_id: int, node_id: int, current_account: AuthenticatedAccount
) -> None:
    """
    This method attaches the UE to the parent node.
    """
    await UEService.attach_ue_to_node(ue_id, node_id, academic_year,  current_account)

@ueRouter.post("/detach/{ue_id}/{node_id}", status_code=201, response_model=None)
async def detach_ue_from_node(academic_year: int,
    ue_id: int, node_id: int, current_account: AuthenticatedAccount
) -> None:
    """
    This method detaches the UE from the parent node.
    """
    await UEService.detach_ue_from_node(ue_id, node_id, academic_year, current_account)

@ueRouter.patch("/{ue_id}", status_code=205, response_model=None)
async def modify_ue(
    ue_id: int, body: PydanticModifyUEModel, current_account: AuthenticatedAccount
) -> None:
    """
    This method modifies the UE of the given UE id.
    """
    return await UEService.modify_ue(ue_id, body, current_account)

@ueRouter.delete("/{ue_id}", status_code=204)
async def delete_ue(ue_id: int, current_account: AuthenticatedAccount) -> None:
    """
    This method deletes the UE of the given UE id.
    """
    await UEService.delete_ue(ue_id, current_account)
