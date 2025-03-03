"""
This module provides the methods to interact with the Status model.
"""

from fastapi import HTTPException
from app.models.pydantic.StatusModel import PydanticStatusResponseModel
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.status import StatusInDB
from app.services.PermissionService import check_permissions
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableOperations, AvailableServices


async def get_all_status(academic_year: int, current_account: AccountInDB) -> list[PydanticStatusResponseModel]:
    """
    This method returns all the statuses.
    """
    await check_permissions(AvailableServices.STATUS_SERVICE,
                            AvailableOperations.GET,
                            current_account,
                            academic_year)

    return [PydanticStatusResponseModel.model_validate(status) for status in await StatusInDB.all()]

async def get_status_by_id(academic_year: int, status_id: int, current_account: AccountInDB) -> PydanticStatusResponseModel:
    """
    This method returns the status of the given status id.
    """
    await check_permissions(AvailableServices.STATUS_SERVICE,
                            AvailableOperations.GET,
                            current_account,
                            academic_year)

    status = await StatusInDB.get_or_none(id=status_id)
    if status is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.STATUS_NOT_FOUND.value)

    return PydanticStatusResponseModel.model_validate(status)
