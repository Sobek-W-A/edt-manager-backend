"""
Service for affectations.
Used to assign/unassign classes to teachers and retrieve these informations.
"""

from fastapi import HTTPException
from app.models.pydantic.AffectationModel import PydanticAffectation
from app.models.tortoise.affectation import AffectationInDB
from app.models.tortoise.profile import ProfileInDB
from app.utils.enums.http_errors import CommonErrorMessages


async def get_teacher_affectations(profile_id: int) -> list[PydanticAffectation]:
    """
    This method returns all classes assigned to a teacher.
    """

    profile : ProfileInDB | None = await ProfileInDB.get_or_none(id=profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.PROFILE_NOT_FOUND)

    affectations : list[AffectationInDB] = await AffectationInDB.filter(profile_id=profile_id).all()
    return [PydanticAffectation.model_validate(affectation) for affectation in affectations]
