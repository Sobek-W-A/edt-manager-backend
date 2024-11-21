"""
This module contains the Tag class.
"""
class Tag():
    """
    This class represents a Tag object.
    It is used to categorize the different endpoints of the API in the documentation.
    """

    name: str
    description: str

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def export(self) -> dict[str, str]:
        """
        This method exports the Tag object to a dictionary.
        """
        return {
            "name": self.name,
            "description": self.description
        }
