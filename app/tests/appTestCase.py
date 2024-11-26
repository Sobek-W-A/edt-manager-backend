import json
from typing import Mapping, TypeAlias, Union
import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import jsonschema

from app.main import app

json_type: TypeAlias = Union[str, int, float, bool, None, Mapping[str, 'json_type'], list['json_type']]

class AppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app

    def assertSchemaValidation(self, response: json_type, schema_path: str) -> None:
        try:
            schema = json.loads(schema_path)
            jsonschema.validate(response, schema)
        except jsonschema.ValidationError as e:
            self.fail(e)