"""
This module provides the methods to interact with the Status model.
"""

from fastapi import HTTPException

from app.models.pydantic.CoefficientModel import PydanticCoefficientModelResponse
from app.models.pydantic.CourseTypeModel import PydanticCourseTypeModel
from app.models.pydantic.StatusModel import PydanticStatusResponseModel
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.coefficient import CoefficientInDB
from app.models.tortoise.status import StatusInDB
from app.services.PermissionService import check_permissions
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableOperations, AvailableServices


async def get_all_status(academic_year: int,
                         current_account: AccountInDB) -> list[PydanticStatusResponseModel]:
    """
    This method returns all the statuses.
    """
    await check_permissions(AvailableServices.STATUS_SERVICE,
                            AvailableOperations.GET_MULTIPLE,
                            current_account,
                            academic_year)

    statuses : list[StatusInDB] = await StatusInDB.all()
    coefficients: list[CoefficientInDB] = await CoefficientInDB.all().prefetch_related("course_type")


    coefficients_map = {}

    for coefficient in coefficients:
        if coefficient.status_id not in coefficients_map:
            coefficients_map[coefficient.status_id] = []

        coefficients_map[coefficient.status_id].append(
            PydanticCoefficientModelResponse(
                multiplier=coefficient.multiplier,
                course_type=PydanticCourseTypeModel.model_validate(coefficient.course_type)
            )
        )

    status_with_coef : list[PydanticStatusResponseModel] = [
        PydanticStatusResponseModel(
            id=status.id,
            name=status.name,
            description=status.description,
            quota=status.quota,
            multiplier=coefficients_map.get(status.id,[]),
        )
        for status in statuses
    ]
    return status_with_coef


async def get_status_by_id(academic_year: int,
                           status_id: int,
                           current_account: AccountInDB) -> PydanticStatusResponseModel:
    """
    This method returns the status of the given status id.
    """
    await check_permissions(AvailableServices.STATUS_SERVICE,
                            AvailableOperations.GET_SINGLE,
                            current_account,
                            academic_year)

    status = await StatusInDB.get_or_none(id=status_id)
    if status is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.STATUS_NOT_FOUND.value)

    coefficients : list[CoefficientInDB] = await CoefficientInDB.filter(status_id=status_id).prefetch_related("course_type")

    coefficients_list = [
        PydanticCoefficientModelResponse(
            multiplier=coefficient.multiplier,
            course_type=PydanticCourseTypeModel.model_validate(coefficient.course_type)
        )
        for coefficient in coefficients
    ]

    return PydanticStatusResponseModel(
        id=status.id,
        name=status.name,
        description=status.description,
        quota=status.quota,
        multiplier=coefficients_list,
    )

