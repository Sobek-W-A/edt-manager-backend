"""
This module contains the Course and Profile related enums to load in the database.
CAREFUL : These models are dependent of the AcademicYear model. They will have a default
value there.
"""

import datetime

from app.models.tortoise.course_type import CourseTypeInDB
from app.models.tortoise.status import StatusInDB
from app.utils.enums.enum_loaders import AbstractEnumLoader, LoadableData


CURRENT_YEAR: int = datetime.datetime.now().year


class Course(LoadableData):
    """
    Describes what a CourseType is.
    """
    course_type_name: str
    course_type_description: str

    def __init__(self, course_type_name: str, course_type_description: str):
        self.course_type_name = course_type_name
        self.course_type_description = course_type_description

    async def load_to_db(self) -> None:
        """
        This method is used to load the course type to the database.
        """
        await CourseTypeInDB.create(name=self.course_type_name,
                                    description=self.course_type_description,
                                    academic_year=CURRENT_YEAR)

class Status(LoadableData):
    """
    Describes what a Status is.
    """
    status_name         : str
    status_description  : str
    quota               : int

    def __init__(self, status_name: str, status_description: str, quota: int):
        self.status_name = status_name
        self.status_description = status_description
        self.quota = quota

    async def load_to_db(self) -> None:
        """
        This method is used to load the status to the database.
        """
        await StatusInDB.create(name=self.status_name,
                                description=self.status_description,
                                quota=self.quota,
                                academic_year=CURRENT_YEAR)


class AvailableCourseTypes(AbstractEnumLoader):
    """
    Enum that defines the different Course Types.
    """
    CM  = Course("CM", "Cours Magistral")
    TD  = Course("TD", "Travaux Dirigés")
    TP  = Course("TP", "Travaux Pratiques")
    EI  = Course("EI", "Enseignement d'Intégration")
    TPL = Course("TPL", "Travaux Pratiques Libres")

class AvailableStatus(AbstractEnumLoader):
    """
    Enum that defines the different Status that can be assigned to profiles.
    """
    MANAGER     = Status("Manager", "Manager de l'application.", 160)
    DPT_MANAGER = Status("Responsable de Département", "Responsable de département.", 160)
    TEACHER     = Status("Enseignant", "Enseignant.", 160)
    INDIVIDUAL  = Status("Vacataire", "Personnel vacataire.", 160)
