"""
This module provides classes that makes Enum loading easier.
Provides a LoadableData class that should be inherited by classes that need to be 
loaded to the database and also provides an AbstractEnumLoader class that should be
inherited by Enum classes that need to be loaded to the database.
"""

from abc import ABC, ABCMeta, abstractmethod
import enum

from app.utils.printers import print_info


class LoadableData(ABC):
    """
    This class is used to provide a method to load the data to the database.
    """
    @abstractmethod
    async def load_to_db(self) -> None:
        """
        This method is used to load the data to the database.
        """

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
    async def load_enum_to_db(cls, model_name: str) -> None:
        """
        This method loads all instances of the enum to the database.
        """
        for element in cls:
            await element.value.load_to_db()

        print_info(f"{len(cls)} instances loaded for {model_name}.")
