"""
Affectation routes.
used to manage teacher and classes associations.
"""

from fastapi import APIRouter

from app.models.pydantic.AffectationModel import PydanticAffectation
from app.routes.tags import Tag
from app.services import AffectationService

affectationRouter: APIRouter = APIRouter(prefix="/affectation")
tag: Tag = {
    "name": "Affectations",
    "description": "Affectations-related operations. Used to manage classes-teachers associations."
}


@affectationRouter.get("/{profile_id}",status_code=200, response_model=None)
async def get_teacher_affectations(profile_id: int) -> list[PydanticAffectation]:
    """
    This method returns all classes assigned to a teacher.
    """
    return await AffectationService.get_teacher_affectations(profile_id)
