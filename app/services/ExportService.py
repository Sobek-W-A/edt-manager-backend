

from typing import Any, Type

from pydantic import BaseModel

from app.models.pydantic.AcademicYearTable import PydanticAcademicYearTableExportModel
from app.models.pydantic.AccountMetadataModel import PydanticAccountMetaExportModel
from app.models.pydantic.AccountModel import PydanticAccountExportModel
from app.models.pydantic.AffectationModel import PydanticAffectationExport
from app.models.pydantic.CoefficientModel import PydanticCoefficientExportModel
from app.models.pydantic.CourseModel import PydanticCourseExportModel
from app.models.pydantic.CourseTypeModel import PydanticCourseTypeExportModel
from app.models.pydantic.NodeModel import PydanticNodeExportModel
from app.models.pydantic.OperationModel import PydanticOperationExportModel
from app.models.pydantic.PermissionsModel import PydanticPermissionExportModel
from app.models.pydantic.ProfileModel import PydanticProfileExportModel
from app.models.pydantic.PydanticRole import PydanticRoleExportModel
from app.models.pydantic.ServiceModel import PydanticServiceExportModel
from app.models.pydantic.StatusModel import PydanticStatusExportModel
from app.models.pydantic.UEModel import PydanticUEExportModel

from app.models.tortoise.abstract.serializable_model import SerializableModel
from app.models.tortoise.academic_year_table import AcademicYearTableInDB
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.account_metadata import AccountMetadataInDB
from app.models.tortoise.affectation import AffectationInDB
from app.models.tortoise.coefficient import CoefficientInDB
from app.models.tortoise.course import CourseInDB
from app.models.tortoise.course_type import CourseTypeInDB
from app.models.tortoise.node import NodeInDB
from app.models.tortoise.operation import OperationInDB
from app.models.tortoise.permission import PermissionInDB
from app.models.tortoise.profile import ProfileInDB
from app.models.tortoise.role import RoleInDB
from app.models.tortoise.service import ServiceInDB
from app.models.tortoise.status import StatusInDB
from app.models.tortoise.ue import UEInDB


async def export():
    truc: dict[str, tuple[Type[SerializableModel], Type[BaseModel]]] = {
        "academic_year": (AcademicYearTableInDB, PydanticAcademicYearTableExportModel),
        "account_metadata": (AccountMetadataInDB, PydanticAccountMetaExportModel),
        "account": (AccountInDB, PydanticAccountExportModel),
        "affectation": (AffectationInDB, PydanticAffectationExport),
        "coefficient": (CoefficientInDB, PydanticCoefficientExportModel),
        "course_type": (CourseTypeInDB, PydanticCourseTypeExportModel),
        "course": (CourseInDB, PydanticCourseExportModel),
        "node": (NodeInDB, PydanticNodeExportModel),
        "operation": (OperationInDB, PydanticOperationExportModel),
        "permission": (PermissionInDB, PydanticPermissionExportModel),
        "profile": (ProfileInDB, PydanticProfileExportModel),
        # "role": (RoleInDB, PydanticRoleExportModel),
        "service": (ServiceInDB, PydanticServiceExportModel),
        "status": (StatusInDB, PydanticStatusExportModel),
        # "ue": (UEInDB, PydanticUEExportModel)
    }

    result: dict[str, Any] = {}

    for name, value in truc.items():
        tortoise_model, pydantic_model = value
        result[name] = await tortoise_model.export(pydantic_model)

    return result