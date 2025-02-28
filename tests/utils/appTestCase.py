import json
from typing import Any, Mapping, TypeAlias, Union
import unittest

import jsonschema
import requests

json_type: TypeAlias = Union[str, int, float, bool, None, Mapping[str, 'json_type'], list['json_type']]

class AppTestCase(unittest.TestCase):

    BASE_URL: str = "http://localhost:8000"
    _access_token: str = ""
    _refresh_token: str = ""

    @classmethod
    def authenticate(cls):
        credentials = {
            "username": "admin",
            "password": "CodeMaster123"
        }

        auth: dict[str, str] = requests.request("POST", f"{cls.BASE_URL}/auth/login", data=credentials).json()

        cls._access_token = auth["access_token"]
        cls._refresh_token = auth["refresh_token"]

    @classmethod
    def setUpClass(cls) -> None:

        # resolver = jsonschema.RefResolver(base_uri="file://.", referrer=None)

        cls.authenticate()


    def assertSchemaValidation(self, response: json_type, schema_path: str) -> None:
        try:
            with open(schema_path) as file:
                schema = json.load(file)
            jsonschema.validate(response, schema)
        except jsonschema.ValidationError as e:
            self.fail(e)


    def call_api(self, method: str, route: str, *, use_auth: bool = False, body: dict[str, Any] = {}) -> requests.Response:
        if use_auth:
            header = {
                "Authorization": f"bearer {self._access_token}"
            }
        else:
            header = {}

        return requests.request(method, f"{self.BASE_URL}{route}", headers=header, json=body)






    