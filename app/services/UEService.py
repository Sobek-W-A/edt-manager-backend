"""
UE-related operations service.
Provides the methods to use when interacting with an UE.
"""
from fastapi import HTTPException

from app.models.pydantic.UEModel import PydanticCreateUEModel, PydanticUEModel, PydanticModifyUEModel
from app.models.tortoise.ue import UEInDB
from app.utils.enums.http_errors import CommonErrorMessages


async def get_ue_by_id(ue_id: int) -> PydanticUEModel:
    """
    This method returns the UE of the given UE id.
    """

    #TODO

    ue : UEInDB= await UEInDB.get_or_none(id=ue_id)

    if ue is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.UE_NOT_FOUND.value)

    return PydanticUEModel(academic_year=ue.academic_year,
                           courses=ue.courses,
                           name=ue.name,
                           ue_id=ue.id)




async def add_ue(body: PydanticCreateUEModel) -> PydanticUEModel:
    """
    This method creates a new UE.
    """

    if await UEInDB.filter(name=body.name).exists():
        raise HTTPException(status_code=409, detail=CommonErrorMessages.UE_ALREADY_EXIST.value)

    ue_to_create : UEInDB = UEInDB(name=body.name, academic_year=body.academic_year)

    await UEInDB.save(ue_to_create)

    return PydanticUEModel(academic_year=body.academic_year,
                           courses=[],
                           name=body.name,
                           ue_id=ue_to_create.id)



async def modify_ue(ue_id: int, body: PydanticModifyUEModel) -> None:
    """
    This method modifies the UE of the given UE id.
    """

    ue_to_modify: UEInDB = await UEInDB.get_or_none(id=ue_id)

    if ue_to_modify is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.UE_NOT_FOUND.value)

    if await UEInDB.filter(name=body.name).exists():
        raise HTTPException(status_code=409, detail=CommonErrorMessages.UE_ALREADY_EXIST.value)

    try:
        await ue_to_modify.update_from_dict(body.model_dump(exclude_none=True))  # type: ignore
        await ue_to_modify.save()

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e


    return None


async def delete_ue(ue_id: int) -> None:
    """
    This method deletes the UE of the given UE id.
    """
    #TODO
    return None
