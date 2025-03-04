"""
Academic_year routes.
used to manage academic_year.
"""

from fastapi import APIRouter

from app.models.aliases import AuthenticatedAccount
from app.models.pydantic.AcademicYearTable import PydanticAcademicTableModel
from app.routes.tags import Tag
from app.services import AcademicYearService

academic_yearRouter: APIRouter = APIRouter(prefix="/academic_year")
tag: Tag = {
    "name": "Academic Year",
    "description": "Affectations-related operations. Used to manage Academic Year."
}

@academic_yearRouter.get("/", status_code=200,response_model=list[PydanticAcademicTableModel])
async def get_all_academic_year() -> list[PydanticAcademicTableModel]:
    """
    This method returns all the academic_year.
    """
    return await AcademicYearService.get_all_academic_year()

@academic_yearRouter.post("/", status_code=201,response_model=PydanticAcademicTableModel)
async def create_new_academic_year(academic_year: int,
                                   current_account: AuthenticatedAccount) -> PydanticAcademicTableModel:
    """
    This method creates a new academic_year.
    """
    return await AcademicYearService.create_new_academic_year(academic_year, current_account)
