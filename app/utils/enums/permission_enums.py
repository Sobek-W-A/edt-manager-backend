"""
This module provides Enums to help manage permissions.
These are basically static data that needs to be stored in database at creation.
They are used to check if a user has the permission to perform a certain operation 
on a certain service.
"""
import enum

class Operation():
    """
    Describes what an Operation is
    """
    operation_name: str
    operation_description: str

    def __init__(self, operation_name: str, operation_description: str):
        self.operation_name = operation_name
        self.operation_description = operation_description

class Service():
    """
    Describes what a Service is
    """
    service_name: str
    service_description: str

    def __init__(self, service_name: str, service_description: str):
        self.service_name = service_name
        self.service_description = service_description

class Permission():
    """
    Describes what a permission is.
    """
    service:    Service
    operations: list[Operation]

    def __init__(self, service: Service, operations: list[Operation]):
        self.service = service
        self.operations = operations

class Role():
    """
    Describes what a role is.
    """
    role_name: str
    role_description: str
    permissions: list[Permission]

    def __init__(self, role_name: str, role_description: str, permissions: list[Permission]):
        self.role_name = role_name
        self.role_description = role_description
        self.permissions = permissions

# Enums
class AvailableOperations(enum.Enum):
    """
    Enumeration to provide the available CRUD operations on the available services.
    """
    CREATE = Operation("Create", "Operations that correspond to creation of a resource")
    GET    = Operation("Get",    "Operations that correspond to retrieval of a resource")
    UPDATE = Operation("Update", "Operations that correspond to an update of a resource")
    DELETE = Operation("Delete", "Operations that correspond to deletion of a resource")


class AvailableServices(enum.Enum):
    """
    Enumeration to provide the available services.
    """
    PROFILE_SERVICE    = Service("Profile Service", "Service that manages profiles.")
    ACCOUNT_SERVICE = Service("Account Service", "Service that manages accounts and logging.")


class AvailablePermissions(enum.Enum):
    """
    Class that provides the available permissions.
    """
    CRUD_PROFILE    = Permission(AvailableServices.PROFILE_SERVICE.value,
                           [AvailableOperations.CREATE.value, AvailableOperations.GET.value,
                            AvailableOperations.UPDATE.value, AvailableOperations.DELETE.value])
    CRUD_SERVICE = Permission(AvailableServices.ACCOUNT_SERVICE.value,
                           [AvailableOperations.CREATE.value, AvailableOperations.GET.value,
                            AvailableOperations.UPDATE.value, AvailableOperations.DELETE.value])
class AvailableRoles(enum.Enum):
    """
    Class that provides the available roles.
    """
    ADMIN = Role("Administrator", "Role that corresponds to the administrator of the system.", [AvailablePermissions.CRUD_PROFILE.value])
