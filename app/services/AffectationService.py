"""
Service for affectations.
Used to assign/unassign classes to teachers and retrieve these informations.
"""

from fastapi import HTTPException
from app.models.pydantic.AffectationModel import PydanticAffectation, PydanticAffectationInCreate
from app.models.pydantic.ProfileModel import PydanticProfileResponse
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.affectation import AffectationInDB
from app.models.tortoise.course import CourseInDB
from app.models.tortoise.profile import ProfileInDB
from app.services.PermissionService import check_permissions
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableOperations, AvailableServices


async def get_teacher_affectations(profile_id: int, current_account: AccountInDB) -> list[PydanticAffectation]:
    """
    This method returns all classes assigned to a teacher.
    """

    await check_permissions(AvailableServices.AFFECTATION_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    profile : ProfileInDB | None = await ProfileInDB.get_or_none(id=profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.PROFILE_NOT_FOUND)

    affectations : list[AffectationInDB] = await AffectationInDB.filter(profile_id=profile_id).all()
    return [PydanticAffectation.model_validate(affectation) for affectation in affectations]

async def get_course_affectations(course_id: int, current_account: AccountInDB) -> list[PydanticProfileResponse]:
    """
    This method returns all teachers assigned to a class.
    """

    await check_permissions(AvailableServices.AFFECTATION_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    course : CourseInDB | None = await CourseInDB.get_or_none(id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.COURSE_NOT_FOUND)

    affectations : list[AffectationInDB] = await AffectationInDB.filter(course_id=course_id)\
                                                                .all()\
                                                                .prefetch_related("profile")
    return [PydanticProfileResponse.model_validate(affectation.profile) for affectation in affectations]

async def assign_course_to_profile(affectation: PydanticAffectationInCreate, current_account: AccountInDB) -> PydanticAffectation:
    """
    This method assigns a course to a teacher.
    """

    await check_permissions(AvailableServices.AFFECTATION_SERVICE,
                            AvailableOperations.CREATE,
                            current_account)

    profile_id: int = affectation.profile_id
    course_id: int = affectation.course_id

    profile: ProfileInDB | None = await ProfileInDB.get_or_none(id=profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.PROFILE_NOT_FOUND)
    course: CourseInDB | None = await CourseInDB.get_or_none(id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.COURSE_NOT_FOUND)

    if profile.academic_year != course.academic_year:
        raise HTTPException(status_code=400, detail=CommonErrorMessages.AFFECTATION_ACADEMIC_YEAR_MISMATCH)

    affectation_created: AffectationInDB = await AffectationInDB.create(profile_id=profile_id,
                                                                        course_id=course_id,
                                                                        notes=affectation.notes,
                                                                        hours=affectation.hours,
                                                                        date=affectation.date)
    
    return PydanticAffectation.model_validate(affectation_created)


async def unassign_course_from_profile_with_profile_and_course(profile_id: int, course_id: int, current_account: AccountInDB) -> None:
    """
    This method unassigns a course from a teacher.
    It uses the profile id and the course id. to call the method that uses the affectation id.
    """
    await check_permissions(AvailableServices.AFFECTATION_SERVICE,
                            AvailableOperations.DELETE,
                            current_account)

    profile: ProfileInDB | None = await ProfileInDB.get_or_none(id=profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.PROFILE_NOT_FOUND)
    
    course: CourseInDB | None = await CourseInDB.get_or_none(id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.COURSE_NOT_FOUND)
    
    affectation: AffectationInDB | None = await AffectationInDB.get_or_none(profile_id=profile_id, course_id=course_id)
    if affectation is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.AFFECTATION_NOT_FOUND)

    await unassign_course(affectation)


async def unassign_course_from_profile_with_affectation_id(affectation_id: int, current_account: AccountInDB) -> None:
    """
    This method unassigns a course from a teacher.
    It uses the affectation id.
    """

    await check_permissions(AvailableServices.AFFECTATION_SERVICE,
                            AvailableOperations.DELETE,
                            current_account)

    affectation: AffectationInDB | None = await AffectationInDB.get_or_none(id=affectation_id)
    if affectation is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.AFFECTATION_NOT_FOUND)
    
    await unassign_course(affectation)


async def unassign_course(affectation: AffectationInDB) -> None:
    """
    This method unassigns a course from a teacher.
    CAREFUL : It is not checking the permissions. Not meant to be directly used.
    """
    await affectation.delete()
