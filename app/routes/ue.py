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
# TODO


@ueRouter.get("/{ue_id}", status_code=200, response_model=PydanticUEModel)
async def get_ue_by_id(
    ue_id: int, current_account: AuthenticatedAccount
) -> PydanticUEModel:
    """
    This method returns the UE of the given UE id.
    """
    return await UEService.get_ue_by_id(ue_id, current_account)


@ueRouter.post("/", status_code=201)
async def add_ue(
    body: PydanticCreateUEModel, current_account: AuthenticatedAccount
) -> None:
    """
    This method creates a new UE.
    """
    await UEService.add_ue(body, current_account)


@ueRouter.patch("/{ue_id}", status_code=205)
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
    return await UEService.delete_ue(ue_id, current_account)


