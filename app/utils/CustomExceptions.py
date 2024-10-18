class MissingEnvironnmentException(Exception):

    missing_variable: str

    def __init__(self, missing_variable: str):
        self.missing_variable = missing_variable

        super().__init__(f"The following environnment variable is missing: {self.missing_variable}")

