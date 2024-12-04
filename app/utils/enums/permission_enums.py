"""
This module provides Enums to help manage permissions.
These are basically static data that needs to be stored in database at creation.
They are used to check if a user has the permission to perform a certain operation 
on a certain service.
"""
from abc import ABC, ABCMeta, abstractmethod
import enum

from app.models.tortoise.operation import OperationInDB
from app.models.tortoise.permission import PermissionInDB
from app.models.tortoise.role import RoleInDB
from app.models.tortoise.service import ServiceInDB

class LoadableData(ABC):
    """
    This class is used to provide a method to load the data to the database.
    """
    @abstractmethod
    async def load_to_db(self) -> None:
        """
        This method is used to load the data to the database.
        """

class Operation(LoadableData):
    """
    Describes what an Operation is.
    """
    operation_name: str
    operation_description: str

    def __init__(self, operation_name: str, operation_description: str):
        self.operation_name = operation_name
        self.operation_description = operation_description

    async def load_to_db(self) -> None:
        """
        This method is used to load the operation to the database.
        """
        await OperationInDB.create(name=self.operation_name,
                                   description=self.operation_description)

class Service(LoadableData):
    """
    Describes what a Service is.
    """
    service_name: str
    service_description: str

    def __init__(self, service_name: str, service_description: str):
        self.service_name = service_name
        self.service_description = service_description

    async def load_to_db(self) -> None:
        """
        This method is used to load the service to the database.
        """
        await ServiceInDB.create(name=self.service_name,
                                 description=self.service_description)

class Permission(LoadableData):
    """
    Describes what a permission is.
    """
    service:    Service
    operations: list[Operation]

    def __init__(self, service: Service, operations: list[Operation]):
        self.service = service
        self.operations = operations

    async def load_to_db(self) -> None:
        """
        This method is used to load the permission to the database.
        """
        operations  : dict[str, OperationInDB] = {}
        services    : dict[str, ServiceInDB]   = {}

        map(lambda op: operations.update({op.name: op}), await OperationInDB.all())
        map(lambda serv: services.update({serv.name: serv}), await ServiceInDB.all())

        for operation in self.operations:
            await PermissionInDB.create(service=services[self.service.service_name],
                                        operation=operations[operation.operation_name])

class Role(LoadableData):
    """
    Describes what a role is.
    """
    role_name        : str
    role_description : str
    admin            : bool
    permissions      : list[Permission] | None

    def __init__(self, role_name: str, role_description: str,
                 permissions: list[Permission] | None, admin: bool = False):
        self.role_name = role_name
        self.role_description = role_description
        self.permissions = permissions
        self.admin = admin

    async def load_to_db(self) -> None:
        """
        This method is used to load the role to the database.
        """
        role: RoleInDB = await RoleInDB.create(name=self.role_name,
                                               description=self.role_description)

        if self.admin:
            for permission in AvailablePermissions:
                perms: list[PermissionInDB] = await PermissionInDB.all().filter(service=permission.value.service.service_name)
                await role.permissions.add(*perms)
        else:
            if self.permissions is not None :
                for permission in self.permissions:
                    perms: list[PermissionInDB] = await PermissionInDB.all().filter(service=permission.service.service_name,
                                                                                    operation__in=[op.operation_name for op in permission.operations])
                    await role.permissions.add(*perms)

# Enums
class EnumABCMeta(enum.EnumMeta, ABCMeta):
    """
    This class is used to make pylint happy.
    """

class AbstractEnumLoader(ABC, enum.Enum, metaclass=EnumABCMeta):
    """
    This class is meant to be inherited by the different Enum classes.
    It provides a method to load the enum to the database.
    """
    @classmethod
    async def load_enum_to_db(cls):
        """
        This method loads all instances of the enum to the database.
        """
        for element in cls:
            await element.value.load_to_db()

class AvailableOperations(AbstractEnumLoader):
    """
    Enumeration to provide the available CRUD operations on the available services.
    """
    CREATE = Operation("Create", "Operations that correspond to the creation of a resource")
    GET    = Operation("Get",    "Operations that correspond to the retrieval of a resource")
    UPDATE = Operation("Update", "Operations that correspond to an update of a resource")
    DELETE = Operation("Delete", "Operations that correspond to the deletion of a resource")

class AvailableServices(AbstractEnumLoader):
    """
    Enumeration to provide the available services.
    """
    PROFILE_SERVICE = Service("Profile Service", "Service that manages profiles.")
    ACCOUNT_SERVICE = Service("Account Service", "Service that manages accounts and logging.")
    STATUS_SERVICE  = Service("Status Service", "Service that manages statuses.")
    UE_SERVICE      = Service("UE Service", "Service that manages Learning Units.")
    ROLE_SERVICE    = Service("Role Service", "Service that manages roles.")

class AvailablePermissions(AbstractEnumLoader):
    """
    Enumeration to provide the available permissions.
    """
    CRUD_PROFILE = Permission(AvailableServices.PROFILE_SERVICE.value,
                              [AvailableOperations.CREATE.value,
                               AvailableOperations.GET.value,
                               AvailableOperations.UPDATE.value,
                               AvailableOperations.DELETE.value])
    CRUD_ACCOUNT = Permission(AvailableServices.ACCOUNT_SERVICE.value,
                                [AvailableOperations.CREATE.value,
                                 AvailableOperations.GET.value,
                                 AvailableOperations.UPDATE.value,
                                 AvailableOperations.DELETE.value])
    CRUD_STATUS  = Permission(AvailableServices.STATUS_SERVICE.value,
                                [AvailableOperations.CREATE.value,
                                 AvailableOperations.GET.value,
                                 AvailableOperations.UPDATE.value,
                                 AvailableOperations.DELETE.value])
    CRUD_UE      = Permission(AvailableServices.UE_SERVICE.value,
                                [AvailableOperations.CREATE.value,
                                 AvailableOperations.GET.value,
                                 AvailableOperations.UPDATE.value,
                                 AvailableOperations.DELETE.value])
    CRUD_ROLE    = Permission(AvailableServices.ROLE_SERVICE.value,
                                [AvailableOperations.CREATE.value,
                                 AvailableOperations.GET.value,
                                 AvailableOperations.UPDATE.value,
                                 AvailableOperations.DELETE.value])

class AvailableEnsemblesPermissions(enum.Enum):
    """
    This class regroups the different kind of permissions for the services.
    """
    GET_PROFILE     = Permission(AvailableServices.PROFILE_SERVICE.value,
                                [AvailableOperations.GET.value])
    MANAGE_PROFILE  = AvailablePermissions.CRUD_ROLE.value

    GET_ACCOUNT     = Permission(AvailableServices.ACCOUNT_SERVICE.value,
                                [AvailableOperations.GET.value])
    MANAGE_ACCOUNT  = AvailablePermissions.CRUD_ACCOUNT.value

    GET_STATUS      = Permission(AvailableServices.STATUS_SERVICE.value,
                                [AvailableOperations.GET.value])
    MANAGE_STATUS   = AvailablePermissions.CRUD_STATUS.value

    GET_UE          = Permission(AvailableServices.UE_SERVICE.value,
                                 [AvailableOperations.GET.value])
    MANAGE_UE       = AvailablePermissions.CRUD_UE.value

    GET_ROLE        = Permission(AvailableServices.ROLE_SERVICE.value,
                                    [AvailableOperations.GET.value])
    MANAGE_ROLE     = AvailablePermissions.CRUD_ROLE.value

class AvailableRoles(AbstractEnumLoader):
    """
    Enumeration to provide the available roles.
    This is static data. It should be stored in the database at 
    startup if not already present.
    """
    ADMIN           = Role("Administrator", "Role that has all permissions",
                           None, True)
    DPT_MANAGER     = Role("Department Manager", "Role that manages a department",
                           None, False)
    FMT_MANAGER     = Role("Formation Manager", "Role that manages a formation",
                           None, False)
    ED_SECRETARIAT  = Role("Educational Secretariat", "Role that manages the educational secretariat",
                           None, False)
    TEACHER         = Role("Teacher", "Teacher Role",
                           None, False)
    # TODO : Add proper Ensemble permissions to roles.
