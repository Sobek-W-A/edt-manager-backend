"""
Academic_Year services. Basically the real functionalities concerning the Academic_Year_Table model.
"""
from app.models.pydantic import AcademicYearTable
from app.models.pydantic.AcademicYearTable import PydanticAcademicTableModel
from app.models.tortoise.academic_year_table import AcademicYearTableInDB
from app.services.PermissionService import check_permissions
from app.utils.enums.permission_enums import AvailableServices, AvailableOperations


async def get_all_academic_year(current_account) -> list[PydanticAcademicTableModel]:
    """
        This method retrieves all the academic year.
    """

    await check_permissions(AvailableServices.PROFILE_SERVICE,
                            AvailableOperations.GET,
                            current_account)


    academic_years : list[AcademicYearTableInDB] = await AcademicYearTable.all()

    return [PydanticAcademicTableModel.model_validate(academic_years)]