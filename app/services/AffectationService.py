"""
Service for affectations.
Used to assign/unassign classes to teachers and retrieve these informations.
"""

from datetime import datetime
from fastapi import HTTPException
from app.models.aliases import AuthenticatedAccount
from app.models.pydantic.AffectationModel import PydanticAffectation, PydanticAffectationInCreate, PydanticAffectationInModify
from app.models.pydantic.CourseModel import PydanticCourseModel
from app.models.pydantic.ProfileModel import PydanticProfileResponse
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.affectation import AffectationInDB
from app.models.tortoise.coefficient import CoefficientInDB
from app.models.tortoise.course import CourseInDB
from app.models.tortoise.profile import ProfileInDB
from app.services.PermissionService import check_permissions
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableOperations, AvailableServices


async def get_teacher_affectations(academic_year: int,
                                   profile_id: int,
                                   current_account: AccountInDB) -> list[PydanticAffectation]:
    """
    This method returns all classes assigned to a teacher.
    """

    # await check_permissions(AvailableServices.AFFECTATION_SERVICE,
    #                         AvailableOperations.GET_MULTIPLE,
    #                         current_account,
    #                         academic_year)

    profile : ProfileInDB | None = await ProfileInDB.get_or_none(id=profile_id)
    if profile is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.PROFILE_NOT_FOUND)

    affectations : list[AffectationInDB] = await AffectationInDB.filter(profile_id=profile_id)\
                                                                .prefetch_related("course")
    for affectation in affectations:
        await affectation.fetch_related("course")
        if affectation.course is not None:
            await affectation.course.fetch_related("course_type")

    return [PydanticAffectation(
                id=affectation.id,
                profile=profile.id,
                course=PydanticCourseModel.model_validate(affectation.course),
                hours=affectation.hours,
                notes=affectation.notes,
                date=affectation.date,
                group=affectation.group
            ) for affectation in affectations]

async def get_course_affectations(academic_year: int,
                                  course_id: int,
                                  current_account: AccountInDB) -> list[PydanticAffectation]:
    """
    This method returns all teachers assigned to a class.
    """

    await check_permissions(AvailableServices.AFFECTATION_SERVICE,
                            AvailableOperations.GET_MULTIPLE,
                            current_account,
                            academic_year)

    course : CourseInDB | None = await CourseInDB.get_or_none(id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.COURSE_NOT_FOUND)

    affectations : list[AffectationInDB] = await AffectationInDB.filter(course_id=course_id)\
                                                                .all()\
                                                                .prefetch_related("profile")

    return [PydanticAffectation(
                id=affectation.id,
                profile=PydanticProfileResponse.model_validate(affectation.profile),
                course=course.id,
                hours=affectation.hours,
                notes=affectation.notes,
                date=affectation.date,
                group=affectation.group
            ) for affectation in affectations]

async def assign_course_to_profile(academic_year: int,
                                   affectation: PydanticAffectationInCreate,
                                   current_account: AccountInDB) -> PydanticAffectation:
    """
    This method assigns a course to a teacher.
    """

    await check_permissions(AvailableServices.AFFECTATION_SERVICE,
                            AvailableOperations.CREATE,
                            current_account,
                            academic_year)

    profile_id: int = affectation.profile_id
    course_id: int = affectation.course_id

    profile: ProfileInDB | None = await ProfileInDB.get_or_none(id=profile_id)
    if profile is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.PROFILE_NOT_FOUND)
    course: CourseInDB | None = await CourseInDB.get_or_none(id=course_id)
    if course is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.COURSE_NOT_FOUND)

    if profile.academic_year != course.academic_year:
        raise HTTPException(status_code=400,
                            detail=CommonErrorMessages.AFFECTATION_ACADEMIC_YEAR_MISMATCH)
    
    if course.group_count < affectation.group or affectation.group < 1:
        raise HTTPException(status_code=400,
                            detail=CommonErrorMessages.AFFECTATION_GROUP_INVALID)

    affectation_created: AffectationInDB = await AffectationInDB.create(profile_id=profile_id,
                                                                        course_id=course_id,
                                                                        notes=affectation.notes,
                                                                        hours=affectation.hours,
                                                                        group=affectation.group,
                                                                        date=datetime.now())
    
    await affectation_created.fetch_related("profile", "course")

    return PydanticAffectation(
                id=affectation_created.id,
                profile=profile.id,
                course=affectation_created.course.id,
                hours=affectation_created.hours,
                notes=affectation_created.notes,
                date=affectation_created.date,
                group=affectation_created.group)


async def modify_affectation_by_affectation_id(academic_year: int,
                                               current_account: AccountInDB,
                                               new_data: PydanticAffectationInModify,
                                               affectation_id: int) -> None:
    """
    This method modifies an affectation.
    Searches the affectation with the affectation ID and the calls the method that changes info.
    """
    await check_permissions(AvailableServices.AFFECTATION_SERVICE,
                            AvailableOperations.UPDATE,
                            current_account,
                            academic_year)
    
    affectation: AffectationInDB | None = await AffectationInDB.get_or_none(id=affectation_id)
    if affectation is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.AFFECTATION_NOT_FOUND)
    
    return await modify_affectation(new_data, affectation)

async def modify_affectation_by_profile_and_course(academic_year: int,
                                                   current_account: AccountInDB,
                                                   new_data: PydanticAffectationInModify,
                                                   profile_id: int,
                                                   course_id: int) -> None:
    """
    This method modifies an affectation.
    Searches the affectation with the profile and course id.
    Then calls the method to change the informations.
    """
    await check_permissions(AvailableServices.AFFECTATION_SERVICE,
                            AvailableOperations.UPDATE,
                            current_account,
                            academic_year)

    affectation: AffectationInDB | None = await AffectationInDB.get_or_none(profile_id=profile_id,
                                                                            course_id=course_id)
    if affectation is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.AFFECTATION_NOT_FOUND)
    
    return await modify_affectation(new_data, affectation)

async def modify_affectation(new_data: PydanticAffectationInModify,
                             affectation: AffectationInDB) -> None:
    """
    This method modifies an affectation.
    CAREFUL : It is not checking the permissions. Not meant to be directly used.
    """
    has_changed : bool = False
    if new_data.profile_id is not None:
        profile: ProfileInDB | None = await ProfileInDB.get_or_none(id=new_data.profile_id)
        if profile is None:
            raise HTTPException(status_code=404,
                                detail=CommonErrorMessages.PROFILE_NOT_FOUND)
        affectation.profile = profile
        has_changed = True

    if new_data.course_id is not None:
        course: CourseInDB | None = await CourseInDB.get_or_none(id=new_data.course_id)
        if course is None:
            raise HTTPException(status_code=404,
                                detail=CommonErrorMessages.COURSE_NOT_FOUND)
        affectation.course = course
        has_changed = True

    if new_data.hours is not None:
        affectation.hours = new_data.hours
        has_changed = True

    if new_data.notes is not None:
        affectation.notes = new_data.notes
        has_changed = True

    if new_data.group is not None:
        course: CourseInDB | None = await affectation.course.first()
        if course is None:
            raise HTTPException(status_code=404,
                                detail=CommonErrorMessages.COURSE_NOT_FOUND)
        else:
            affectation.course = course
        if new_data.group < 1 or new_data.group > affectation.course.group_count:
            raise HTTPException(status_code=400,
                                detail=CommonErrorMessages.AFFECTATION_GROUP_INVALID)
        affectation.group = new_data.group
        has_changed = True

    if has_changed:
        affectation.date = datetime.now()

    await affectation.save()

async def unassign_course_from_profile_with_profile_and_course(academic_year: int,
                                                               profile_id: int,
                                                               course_id: int,
                                                               current_account: AccountInDB) -> None:
    """
    This method unassigns a course from a teacher.
    It uses the profile id and the course id. to call the method that uses the affectation id.
    """
    await check_permissions(AvailableServices.AFFECTATION_SERVICE,
                            AvailableOperations.DELETE,
                            current_account,
                            academic_year)

    profile: ProfileInDB | None = await ProfileInDB.get_or_none(id=profile_id)
    if profile is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.PROFILE_NOT_FOUND)
    
    course: CourseInDB | None = await CourseInDB.get_or_none(id=course_id)
    if course is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.COURSE_NOT_FOUND)
    
    affectation: AffectationInDB | None = await AffectationInDB.get_or_none(profile_id=profile_id, course_id=course_id)
    if affectation is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.AFFECTATION_NOT_FOUND)

    await unassign_course(affectation)


async def unassign_course_from_profile_with_affectation_id(academic_year: int,
                                                           affectation_id: int,
                                                           current_account: AccountInDB) -> None:
    """
    This method unassigns a course from a teacher.
    It uses the affectation id.
    """

    await check_permissions(AvailableServices.AFFECTATION_SERVICE,
                            AvailableOperations.DELETE,
                            current_account,
                            academic_year)

    affectation: AffectationInDB | None = await AffectationInDB.get_or_none(id=affectation_id)
    if affectation is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.AFFECTATION_NOT_FOUND)
    
    await unassign_course(affectation)


async def unassign_course(affectation: AffectationInDB) -> None:
    """
    This method unassigns a course from a teacher.
    CAREFUL : It is not checking the permissions. Not meant to be directly used.
    """
    await affectation.delete()

async def get_total_hours(academic_year: int, profile_id: int):
    teacher = await ProfileInDB.get(id=profile_id)
    current_account=None
    affectations = await get_teacher_affectations(academic_year, profile_id, current_account)
    coeffs = {coeff.course_type_id: coeff.multiplier for coeff in await CoefficientInDB.all()}
    return {
        affectation.id: affectation.hours * coeffs.get(affectation.course.course_type.id, 1.) for affectation in affectations
    }


