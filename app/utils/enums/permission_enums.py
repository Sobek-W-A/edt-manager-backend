"""
This module provides Enums to help manage permissions.
These are basically static data that needs to be stored in database at creation.
They are used to check if a user has the permission to perform a certain operation 
on a certain service.
"""

from enum import Enum
from app.models.tortoise.operation import OperationInDB
from app.models.tortoise.permission import PermissionInDB
from app.models.tortoise.role import RoleInDB
from app.models.tortoise.service import ServiceInDB
from app.utils.enums.enum_loaders import AbstractEnumLoader, LoadableData

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

        for op in await OperationInDB.all():
            operations.update({op.name: op})
        for serv in await ServiceInDB.all(): 
            services.update({serv.name: serv})

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
                perms: list[PermissionInDB] = await PermissionInDB.all()\
                                                                  .filter(service=permission.value.service.service_name)
                await role.permissions.add(*perms)
        else:
            if self.permissions is not None :
                for permission in self.permissions:
                    perms: list[PermissionInDB] = await PermissionInDB.all()\
                                                                      .filter(service=permission.service.service_name,
                                                                              operation__name__in=[op.operation_name for op in permission.operations])
                    await role.permissions.add(*perms)

# Enums
class AvailableOperations(AbstractEnumLoader):
    """
    Enumeration to provide the available CRUD operations on the available services.
    """
    CREATE       = Operation("Create",
                             "Operations that correspond to the creation of a resource")
    GET_MULTIPLE = Operation("Get Multiple",
                             "Operations that correspond to the retrieval of multiple resources")
    GET_SINGLE   = Operation("Get Single",
                             "Operations that correspond to the retrieval of a single resource")
    GET_ME       = Operation("Get Me",
                             "Operations that correspond to the retrieval of data about the current user")
    UPDATE       = Operation("Update",
                             "Operations that correspond to an update of a resource")
    DELETE       = Operation("Delete",
                             "Operations that correspond to the deletion of a resource")

class AvailableServices(AbstractEnumLoader):
    """
    Enumeration to provide the available services.
    """
    PROFILE_SERVICE       = Service("Profile Service",
                                    "Service that manages profiles.")
    ACCOUNT_SERVICE       = Service("Account Service",
                                    "Service that manages accounts and logging.")
    AFFECTATION_SERVICE   = Service("Affectation Service",
                                    "Service that manages course to teachers affectations.")
    STATUS_SERVICE        = Service("Status Service",
                                    "Service that manages statuses.")
    UE_SERVICE            = Service("UE Service",
                                    "Service that manages Learning Units.")
    NODE_SERVICE          = Service("Node Service",
                                    "Service that manages nodes.")
    ROLE_SERVICE          = Service("Role Service",
                                    "Service that manages roles.")
    COURSE_SERVICE        = Service("Course Service",
                                    "Service that manages courses.")
    ACADEMIC_YEAR_SERVICE = Service("Academic Year Service",
                                    "Service that manages academic years.")

class AvailablePermissions(AbstractEnumLoader):
    """
    Enumeration to provide the available permissions.
    """
    CRUD_PROFILE = Permission(AvailableServices.PROFILE_SERVICE.value,
                                    [AvailableOperations.CREATE.value,
                                     AvailableOperations.GET_MULTIPLE.value,
                                     AvailableOperations.GET_SINGLE.value,
                                     AvailableOperations.GET_ME.value,
                                     AvailableOperations.UPDATE.value,
                                     AvailableOperations.DELETE.value])

    CRUD_ACCOUNT = Permission(AvailableServices.ACCOUNT_SERVICE.value,
                                    [AvailableOperations.CREATE.value,
                                     AvailableOperations.GET_MULTIPLE.value,
                                     AvailableOperations.GET_SINGLE.value,
                                     AvailableOperations.GET_ME.value,
                                     AvailableOperations.UPDATE.value,
                                     AvailableOperations.DELETE.value])

    CRUD_STATUS  = Permission(AvailableServices.STATUS_SERVICE.value,
                                    [AvailableOperations.CREATE.value,
                                     AvailableOperations.GET_MULTIPLE.value,
                                     AvailableOperations.GET_SINGLE.value,
                                     AvailableOperations.GET_ME.value,
                                     AvailableOperations.UPDATE.value,
                                     AvailableOperations.DELETE.value])

    CRUD_NODE    = Permission(AvailableServices.NODE_SERVICE.value,
                                    [AvailableOperations.CREATE.value,
                                     AvailableOperations.GET_MULTIPLE.value,
                                     AvailableOperations.GET_SINGLE.value,
                                     AvailableOperations.GET_ME.value,
                                     AvailableOperations.UPDATE.value,
                                     AvailableOperations.DELETE.value])

    CRUD_UE      = Permission(AvailableServices.UE_SERVICE.value,
                                    [AvailableOperations.CREATE.value,
                                     AvailableOperations.GET_MULTIPLE.value,
                                     AvailableOperations.GET_SINGLE.value,
                                     AvailableOperations.GET_ME.value,
                                     AvailableOperations.UPDATE.value,
                                     AvailableOperations.DELETE.value])

    CRUD_ROLE    = Permission(AvailableServices.ROLE_SERVICE.value,
                                    [AvailableOperations.CREATE.value,
                                     AvailableOperations.GET_MULTIPLE.value,
                                     AvailableOperations.GET_SINGLE.value,
                                     AvailableOperations.GET_ME.value,
                                     AvailableOperations.UPDATE.value,
                                     AvailableOperations.DELETE.value])

    CRUD_AFFECTATION = Permission(AvailableServices.AFFECTATION_SERVICE.value,
                                    [AvailableOperations.CREATE.value,
                                     AvailableOperations.GET_MULTIPLE.value,
                                     AvailableOperations.GET_SINGLE.value,
                                     AvailableOperations.GET_ME.value,
                                     AvailableOperations.UPDATE.value,
                                     AvailableOperations.DELETE.value])

    CRUD_COURSE      = Permission(AvailableServices.COURSE_SERVICE.value,
                                    [AvailableOperations.CREATE.value,
                                    AvailableOperations.GET_MULTIPLE.value,
                                    AvailableOperations.GET_SINGLE.value,
                                    AvailableOperations.GET_ME.value,
                                    AvailableOperations.UPDATE.value,
                                    AvailableOperations.DELETE.value])

    CRUD_ACADEMIC_YEAR = Permission(AvailableServices.ACADEMIC_YEAR_SERVICE.value,
                                    [AvailableOperations.CREATE.value,
                                    AvailableOperations.GET_MULTIPLE.value,
                                    AvailableOperations.GET_SINGLE.value,
                                    AvailableOperations.GET_ME.value,
                                    AvailableOperations.UPDATE.value,
                                    AvailableOperations.DELETE.value])


class AvailableGetPermissions(Enum):
    """
    This class provides the GET permissions.
    """
    GET_PROFILES       = Permission(AvailableServices.PROFILE_SERVICE.value,
                                          [AvailableOperations.GET_MULTIPLE.value,
                                           AvailableOperations.GET_SINGLE.value,
                                           AvailableOperations.GET_ME.value])
    GET_ACCOUNT        = Permission(AvailableServices.ACCOUNT_SERVICE.value,
                                          [AvailableOperations.GET_MULTIPLE.value,
                                           AvailableOperations.GET_SINGLE.value,
                                           AvailableOperations.GET_ME.value])
    GET_SERVICE        = Permission(AvailableServices.STATUS_SERVICE.value,
                                          [AvailableOperations.GET_MULTIPLE.value,
                                           AvailableOperations.GET_SINGLE.value,
                                           AvailableOperations.GET_ME.value])
    GET_STATUS         = Permission(AvailableServices.STATUS_SERVICE.value,
                                          [AvailableOperations.GET_MULTIPLE.value,
                                           AvailableOperations.GET_SINGLE.value,
                                           AvailableOperations.GET_ME.value])
    GET_NODE           = Permission(AvailableServices.NODE_SERVICE.value,
                                          [AvailableOperations.GET_MULTIPLE.value,
                                           AvailableOperations.GET_SINGLE.value,
                                           AvailableOperations.GET_ME.value])
    GET_UE             = Permission(AvailableServices.UE_SERVICE.value,
                                          [AvailableOperations.GET_MULTIPLE.value,
                                           AvailableOperations.GET_SINGLE.value,
                                           AvailableOperations.GET_ME.value])
    GET_ROLE           = Permission(AvailableServices.ROLE_SERVICE.value,
                                      [AvailableOperations.GET_MULTIPLE.value,
                                       AvailableOperations.GET_SINGLE.value,
                                       AvailableOperations.GET_ME.value])
    GET_AFFECTATION    = Permission(AvailableServices.AFFECTATION_SERVICE.value,
                                      [AvailableOperations.GET_MULTIPLE.value,
                                       AvailableOperations.GET_SINGLE.value,
                                       AvailableOperations.GET_ME.value])
    GET_COURSE         = Permission(AvailableServices.COURSE_SERVICE.value,
                                    [AvailableOperations.GET_MULTIPLE.value,
                                     AvailableOperations.GET_SINGLE.value,
                                     AvailableOperations.GET_ME.value])
    GET_ACADEMIC_YEAR  = Permission(AvailableServices.ACADEMIC_YEAR_SERVICE.value,
                                    [AvailableOperations.GET_MULTIPLE.value,
                                     AvailableOperations.GET_SINGLE.value,
                                     AvailableOperations.GET_ME.value])

class AvailableRoles(AbstractEnumLoader):
    """
    Enumeration to provide the available roles.
    This is static data. It should be stored in the database at 
    startup if not already present.
    """
    ADMIN           = Role("Administrateur",
                           "Rôle administrateur. Dispose de toutes les permissions pour toutes les années académiques.",
                           None,
                           True)

    DPT_MANAGER     = Role("Responsable de département",
                           "Rôle pour gèrer un département. Dispose de toutes les permissions pour une année académique.",
                           None,
                           True)

    FMT_MANAGER     = Role("Responsable de formation",
                           "Rôle pour gèrer une formation. Dispose de toutes les permissions, en lecture seulement, pour une seule année académique.",
                           [AvailableGetPermissions.GET_ACCOUNT.value,
                            AvailableGetPermissions.GET_PROFILES.value,
                            AvailableGetPermissions.GET_SERVICE.value,
                            AvailableGetPermissions.GET_NODE.value,
                            AvailableGetPermissions.GET_UE.value,
                            AvailableGetPermissions.GET_ROLE.value,
                            AvailableGetPermissions.GET_AFFECTATION.value,
                            AvailableGetPermissions.GET_COURSE.value,
                            AvailableGetPermissions.GET_ACADEMIC_YEAR.value,
                            AvailableGetPermissions.GET_STATUS.value],
                           False)

    ED_SECRETARIAT  = Role("Secrétariat",
                           "Rôle pour le secrétariat. Dispose de toutes les permissions, en lecture seulement, pour une seule année académique.",
                           [AvailableGetPermissions.GET_ACCOUNT.value,
                            AvailableGetPermissions.GET_PROFILES.value,
                            AvailableGetPermissions.GET_SERVICE.value,
                            AvailableGetPermissions.GET_NODE.value,
                            AvailableGetPermissions.GET_UE.value,
                            AvailableGetPermissions.GET_ROLE.value,
                            AvailableGetPermissions.GET_AFFECTATION.value,
                            AvailableGetPermissions.GET_COURSE.value,
                            AvailableGetPermissions.GET_ACADEMIC_YEAR.value,
                            AvailableGetPermissions.GET_STATUS.value],
                           False)

    TEACHER         = Role("Professeur",
                           "Professeur. Ne dispose que des permissions de lecture pour les informations le concernant directement et pour les informations liées à ses affectations..",
                           [AvailableGetPermissions.GET_PROFILES.value,
                            AvailableGetPermissions.GET_AFFECTATION.value,
                            AvailableGetPermissions.GET_COURSE.value,
                            AvailableGetPermissions.GET_ACADEMIC_YEAR.value,
                            AvailableGetPermissions.GET_UE.value,
                            AvailableGetPermissions.GET_ROLE.value,
                            AvailableGetPermissions.GET_STATUS.value,
                            Permission(AvailableServices.ACCOUNT_SERVICE.value,
                                       [AvailableOperations.GET_ME.value])],
                           False)
    UNASSIGNED      = Role("Non assigné",
                           "Rôle par défaut. Ne dispose d'aucune permission.",
                           None,
                           False)
