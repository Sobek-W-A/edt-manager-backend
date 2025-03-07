"""
Affectation routes.
used to manage teacher and classes associations.
"""

from fastapi import APIRouter

from app.models.aliases import AuthenticatedAccount

from app.models.pydantic.AffectationModel import (PydanticAffectation,
                                                  PydanticAffectationInCreate,
                                                  PydanticAffectationInModify)
from app.routes.tags import Tag
from app.services import AffectationService

affectationRouter: APIRouter = APIRouter(prefix="/affectation")
tag: Tag = {
    "name": "Affectations",
    "description": "Affectations-related operations. Used to manage classes-teachers associations."
}

@affectationRouter.get("/profile/{profile_id}",status_code=200, response_model=list[PydanticAffectation])
async def get_teacher_affectations(profile_id: int, academic_year: int, current_account: AuthenticatedAccount) -> list[PydanticAffectation]:
    """
    This method returns all classes assigned to a teacher.
    """
    return await AffectationService.get_teacher_affectations(profile_id, current_account)

@affectationRouter.get("/course/{course_id}",status_code=200, response_model=list[PydanticAffectation])
async def get_course_affectations(course_id: int, academic_year: int, current_account: AuthenticatedAccount) -> list[PydanticAffectation]:
    """
    This method returns all teachers assigned to a class.
    """
    return await AffectationService.get_course_affectations(course_id, current_account)

@affectationRouter.post("/assign",status_code=201, response_model=PydanticAffectation)
async def assign_course_to_profile(affectation: PydanticAffectationInCreate, academic_year: int, current_account: AuthenticatedAccount) -> PydanticAffectation:
    """
    This method assigns a course to a teacher.
    """
    return await AffectationService.assign_course_to_profile(affectation, current_account)

@affectationRouter.patch("/{affectation_id}",status_code=205)
async def modify_affectation_by_affectation_id(affectation_id: int, academic_year: int, affectation: PydanticAffectationInModify, current_account: AuthenticatedAccount) -> None:
    """
    This method modifies an affectation.
    """
    await AffectationService.modify_affectation_by_affectation_id(current_account, affectation, affectation_id)

@affectationRouter.patch("/{profile_id}/{course_id}",status_code=205)
async def modify_affectation_by_profile_and_course(profile_id: int, academic_year: int, course_id: int, affectation: PydanticAffectationInModify, current_account: AuthenticatedAccount) -> None:
    """
    This method modifies an affectation.
    """
    await AffectationService.modify_affectation_by_profile_and_course(current_account, affectation, profile_id, course_id)

@affectationRouter.delete("/unassign/{affectation_id}",status_code=205)
async def unassign_course_from_profile_with_affectation_id(academic_year: int, affectation_id: int, current_account: AuthenticatedAccount) -> None:
    """
    This method unassigns a course from a teacher.
    """
    await AffectationService.unassign_course_from_profile_with_affectation_id(affectation_id, current_account)

@affectationRouter.delete("/unassign/profile/{profile_id}/course/{course_id}", status_code=205)
async def unassign_course_from_profile_with_profile_and_course(profile_id: int, course_id: int, academic_year: int, current_account: AuthenticatedAccount) -> None:
    """
    This method unassigns a course from a teacher.
    """
    await AffectationService.unassign_course_from_profile_with_profile_and_course(profile_id, course_id, current_account)
