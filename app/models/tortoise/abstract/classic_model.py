"""
This module provides a classic model.
It is used to simplify classes that only contains 2 fields : name and description, 
with the name being used as primary key. 
"""

from tortoise import Model
from tortoise.fields import Field, CharField, TextField

from app.models.tortoise.abstract.serializable_model import SerializableModel

class ClassicModel(SerializableModel):
    """
    Simple model.
    It is used to simplify classes that only contains 2 fields : name and description, 
    with the name being used as primary key. 
    """
    name         : Field[str] = CharField(pk=True, max_length=128)
    description  : Field[str] = TextField()

    class Meta(Model.Meta):
        """
        This class is used to indicate that the Table is abstract.
        """
        abstract : bool = True
