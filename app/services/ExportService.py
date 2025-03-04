

from typing import Type

from pydantic import BaseModel

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
        "academic_year": (AcademicYearTableInDB, PydanticAcademicTableModel),
        "account_metadata": (AccountMetadataInDB, PydanticAccountMetaModelFromJSON),
        "account": (AccountInDB, PydanticAccountWithoutProfileModel),
        "affectation": (AffectationInDB, PydanticAffectation),
        "coefficient": (CoefficientInDB, PydanticCoefficientModelFromJSON),
        "course_type": (CourseTypeInDB, PydanticCourseTypeModel),
        "course": (CourseInDB, PydanticCourseModel),
        "node": (NodeInDB, PydanticNodeModel),
        "operation": (OperationInDB, PydanticOperationModel),
        "permission": (PermissionInDB, PydanticPermissionsModel),
        "profile": (ProfileInDB, PydanticProfileModelFromJSON),
        "role": (RoleInDB, PydanticRoleModel),
        "service": (ServiceInDB, PydanticServiceModel),
        "status": (StatusInDB, PydanticStatusResponseModel),
        "ue": (UEInDB, PydanticUEModel)
    }

    result: dict[str, Any] = {}

    for name, value in truc.items():
        tortoise_model, pydantic_model = value
        result[name] = await tortoise_model.export(pydantic_model)

    return result