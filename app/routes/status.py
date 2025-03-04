"""
Status routes.
Used to manage status operations.
"""
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

@statusRouter.get("/",status_code=200, response_model=list[PydanticStatusResponseModel])
async def get_all_status(academic_year: int,
                         current_account: AuthenticatedAccount) -> list[PydanticStatusResponseModel]:
    """
    This method returns the status of the given status id.
    """
    return await StatusService.get_all_status(academic_year, current_account)

@statusRouter.get("/{status_id}",status_code=200, response_model=PydanticStatusResponseModel)
async def get_status_by_id(academic_year: int,
                           status_id: int,
                           current_account: AuthenticatedAccount) -> PydanticStatusResponseModel:
    """
    This method returns the status of the given status id.
    """
    return await StatusService.get_status_by_id(academic_year, status_id, current_account)
