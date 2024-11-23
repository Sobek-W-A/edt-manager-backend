"""
This module describes statuses that can be assigned to profiles.
These are used to determine the coefficients that needs to be applied
when we need to calculate the total of hours dispensed.
"""

from app.models.tortoise.abstract.academic_year import AcademicYear
from app.models.tortoise.abstract.classic_model import ClassicModel

class StatusInDB(AcademicYear, ClassicModel):
    """
    This model represents a status that can be assigned to a profile.
    """

    class Meta(AcademicYear.Meta, ClassicModel.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table    : str = "Status"
        abstract : bool = False
