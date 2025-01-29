"""
Service for affectations.
Used to assign/unassign classes to teachers and retrieve these informations.
"""

from datetime import datetime
from fastapi import HTTPException
from app.models.pydantic.AffectationModel import PydanticAffectation, PydanticAffectationInCreate, PydanticAffectationInModify
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

    return [PydanticAffectation(
                id=affectation.id,
                profile=PydanticProfileResponse.model_validate(affectation.profile),
                course_id=affectation.course.id,
                hours=affectation.hours,
                notes=affectation.notes,
                date=affectation.date,
                group=affectation.group
            ) for affectation in affectations]

async def get_course_affectations(course_id: int, current_account: AccountInDB) -> list[PydanticAffectation]:
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
    return [PydanticAffectation(
                id=affectation.id,
                profile=PydanticProfileResponse.model_validate(affectation.profile),
                course_id=affectation.course.id,
                hours=affectation.hours,
                notes=affectation.notes,
                date=affectation.date,
                group=affectation.group
            ) for affectation in affectations]

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
    
    if course.group_count < affectation.group or affectation.group < 1:
        raise HTTPException(status_code=400, detail=CommonErrorMessages.AFFECTATION_GROUP_INVALID)

    affectation_created: AffectationInDB = await AffectationInDB.create(profile_id=profile_id,
                                                                        course_id=course_id,
                                                                        notes=affectation.notes,
                                                                        hours=affectation.hours,
                                                                        date=datetime.now())
    
    return PydanticAffectation.model_validate(affectation_created)


async def modify_affectation_by_affectation_id(current_account: AccountInDB, new_data: PydanticAffectationInModify, affectation_id: int) -> None:
    """
    This method modifies an affectation.
    Searches the affectation with the affectation ID and the calls the method that changes info.
    """
    await check_permissions(AvailableServices.AFFECTATION_SERVICE,
                            AvailableOperations.UPDATE,
                            current_account)
    
    affectation: AffectationInDB | None = await AffectationInDB.get_or_none(id=affectation_id)
    if affectation is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.AFFECTATION_NOT_FOUND)
    
    return await modify_affectation(new_data, affectation)

async def modify_affectation_by_profile_and_course(current_account: AccountInDB, new_data: PydanticAffectationInModify, profile_id: int, course_id: int) -> None:
    """
    This method modifies an affectation.
    Searches the affectation with the profile and course id.
    Then calls the method to change the informations.
    """
    await check_permissions(AvailableServices.AFFECTATION_SERVICE,
                            AvailableOperations.UPDATE,
                            current_account)

    affectation: AffectationInDB | None = await AffectationInDB.get_or_none(profile_id=profile_id,
                                                                            course_id=course_id)
    if affectation is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.AFFECTATION_NOT_FOUND)
    
    return await modify_affectation(new_data, affectation)

async def modify_affectation(new_data: PydanticAffectationInModify, affectation: AffectationInDB) -> None:
    """
    This method modifies an affectation.
    CAREFUL : It is not checking the permissions. Not meant to be directly used.
    """
    has_changed : bool = False
    if new_data.profile_id is not None:
        profile: ProfileInDB | None = await ProfileInDB.get_or_none(id=new_data.profile_id)
        if profile is None:
            raise HTTPException(status_code=404, detail=CommonErrorMessages.PROFILE_NOT_FOUND)
        affectation.profile = profile
        has_changed = True

    if new_data.course_id is not None:
        course: CourseInDB | None = await CourseInDB.get_or_none(id=new_data.course_id)
        if course is None:
            raise HTTPException(status_code=404, detail=CommonErrorMessages.COURSE_NOT_FOUND)
        affectation.course = course
        has_changed = True

    if new_data.hours is not None:
        affectation.hours = new_data.hours
        has_changed = True

    if new_data.notes is not None:
        affectation.notes = new_data.notes
        has_changed = True

    if new_data.group is not None:
        if new_data.group < 1 or new_data.group > affectation.course.group_count:
            raise HTTPException(status_code=400, detail=CommonErrorMessages.AFFECTATION_GROUP_INVALID)
        affectation.group = new_data.group
        has_changed = True

    if has_changed:
        affectation.date  = datetime.now()

    await affectation.save()

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
