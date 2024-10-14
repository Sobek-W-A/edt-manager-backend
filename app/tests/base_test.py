from typing import Any
from unittest import TestCase
import jsonschema

class BaseTest(TestCase):

    def assertSchemaValidation(self, response: dict[str, Any], schema: dict[str, Any]):
        try:
            jsonschema.validate(response, schema)
        except jsonschema.ValidationError as e:
            self.fail(e)