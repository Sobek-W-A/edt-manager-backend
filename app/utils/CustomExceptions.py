"""
This module collects all custom exceptions that don't fit in any package very well.
"""

class MissingEnvironnmentException(Exception):
    """
    This Exception is meant to be used when a required environnment variable is not specified.
    """

    missing_variable: str

    def __init__(self, missing_variable: str):
        self.missing_variable = missing_variable

        super().__init__(f"The following environnment variable is missing: {self.missing_variable}")


class RequiredFieldIsNone(Exception):
    """
    This Exception is meant to be used when a required class attribute is None.
    """

    def __init__(self, message: str):
        super().__init__(message)
