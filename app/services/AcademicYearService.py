"""
Academic_Year services. Basically the real functionalities concerning the Academic_Year_Table model.
"""
from fastapi import HTTPException

from app.models.pydantic import AcademicYearTable
from app.models.pydantic.AcademicYearTable import PydanticAcademicTableModel
from app.models.tortoise.academic_year_table import AcademicYearTableInDB
from app.services.PermissionService import check_permissions
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableServices, AvailableOperations


async def get_all_academic_year(current_account) -> list[PydanticAcademicTableModel]:
    """
        This method retrieves all the academic year.
    """

    await check_permissions(AvailableServices.PROFILE_SERVICE,
                            AvailableOperations.GET,
                            current_account)


    academic_years : list[AcademicYearTableInDB] = await AcademicYearTableInDB.all()

    if academic_years is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.ACADEMIC_YEAR_NOT_FOUND.value)

    return [PydanticAcademicTableModel.model_validate(academic_year) for academic_year in academic_years]

async def create_new_academic_year(current_account) -> PydanticAcademicTableModel:
    """
        This method create a new academic year by finding the most recent one and adding +1.
    """

    await check_permissions(AvailableServices.PROFILE_SERVICE,
                            AvailableOperations.CREATE,
                            current_account)


    last_academic_year = await AcademicYearTableInDB.all().order_by('-academic_year').first()

    if last_academic_year is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.ACADEMIC_YEAR_NOT_FOUND.value)

    new_academic_year = last_academic_year.academic_year + 1
    new_description = f"{new_academic_year}-{new_academic_year + 1}"

    new_academic_year_entry : AcademicYearTableInDB = AcademicYearTableInDB(
                                            academic_year=new_academic_year,
                                            description=new_description
                                            )

    await AcademicYearTableInDB.save(new_academic_year_entry)

    return PydanticAcademicTableModel.model_validate(new_academic_year_entry)
