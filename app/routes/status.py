"""
Status routes.
Used to manage status operations.
"""

# TODO

from fastapi import APIRouter

from app.models.aliases import AuthenticatedAccount
from app.models.pydantic.StatusModel import PydanticStatusResponseModel
from app.routes.tags import Tag
from app.services import StatusService

statusRouter: APIRouter = APIRouter(prefix="/status")
tag: Tag = {
    "name": "Status",
    "description": "Status-related operations."
}

@statusRouter.get("/{academic_year}",status_code=200, response_model=list[PydanticStatusResponseModel])
async def get_all_status(academic_year: int, current_account: AuthenticatedAccount) -> list[PydanticStatusResponseModel]:
    """
    This method returns the status of the given status id.
    """
    return await StatusService.get_all_status(academic_year, current_account)

@statusRouter.get("/{status_id}",status_code=200, response_model=None)
async def get_status_by_id(status_id: int) -> None:
    """
    This method returns the status of the given status id.
    """
    return None

@statusRouter.post("/", status_code=201, response_model=None)
async def add_status() -> None:
    """
    This method creates a new status.
    """
    return None

@statusRouter.patch("/{status_id}", status_code=205)
async def modify_status(status_id: int, body: None) -> None:
    """
    This method modifies the status of the given status id.
    """
    return None

@statusRouter.delete("/{status_id}", status_code=204)
async def delete_status(status_id: int) -> None:
    """
    This method deletes the status of the given status id.
    """
    return None
