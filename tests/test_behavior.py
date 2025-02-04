"""
this file contains test related to the normal behavior of the routes
permission system is tested in test_security.py
"""

from typing import Any
from requests import Response
from utils.appTestCase import AppTestCase


class TestBehavior(AppTestCase):

    def test_get_account_unauthenticated(self):
        response: Response = self.call_api("GET", "/account", use_auth=False)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.reason, "Unauthorized")

        body: dict[str, Any] = response.json()

        self.assertEqual(body["detail"], "Not authenticated")

    def test_get_account(self):
        response: Response = self.call_api("GET", "/account", use_auth=True)
        body: dict[str, Any] = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertSchemaValidation(body, "tests/schemas/list_account.schema.json")

    def test_get_account_by_id(self):
        response: Response = self.call_api("GET", "/account/1", use_auth=True)
        body: dict[str, Any] = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertSchemaValidation(body, "tests/schemas/user.schema.json")

    def test_post_account(self):
        data: dict[str, str | int] = {
            "username": "testuser",
            "password": "securepassword",
        }
        response: Response = self.call_api("POST", "/account", use_auth=True, body=data)

        body: dict[str, Any] = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertSchemaValidation(body, "tests/schemas/post_account.schema.json")

    def test_patch_account(self):
        data: dict[str, str | int] = {"username": "updateduser"}
        response: Response = self.call_api(
            "PATCH", "/account/1", use_auth=True, body=data
        )
        self.assertEqual(response.status_code, 205)

    # def test_delete_account(self):
    #     response: Response = self.call_api("DELETE", "/account/1", use_auth=True)
    #     self.assertEqual(response.status_code, 204)

    def test_get_profile(self):
        response: Response = self.call_api("GET", "/profile", use_auth=True)
        body: dict[str, Any] = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertSchemaValidation(body, "tests/schemas/list_profile.schema.json")

    def test_get_profile_by_id(self):
        response: Response = self.call_api("GET", "/profile/1", use_auth=True)
        body: dict[str, Any] = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertSchemaValidation(body, "tests/schemas/profile.schema.json")

    def test_get_profile_me(self):
        response: Response = self.call_api("GET", "/profile/me", use_auth=True)
        body: dict[str, Any] = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertSchemaValidation(body, "tests/schemas/profile.schema.json")

    def test_post_profile(self):
        data: dict[str, str | int] = {
            "academic_year": 2021,
            "firstname": "jhon",
            "lastname": "doe",
            "mail": "example@mail.com",
            "quota": 0,
        }
        response: Response = self.call_api("POST", "/profile", use_auth=True, body=data)
        body: dict[str, Any] = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertSchemaValidation(body, "tests/schemas/post_profile.schema.json")

    def test_patch_profile(self):
        data: dict[str, str | int] = {"firstname": "new name"}
        response: Response = self.call_api(
            "PATCH", "/profile/1", use_auth=True, body=data
        )
        self.assertEqual(response.status_code, 205)

    # def test_delete_profile(self):
    #     response: Response = self.call_api("DELETE", "/profile/1", use_auth=True)
    #     self.assertEqual(response.status_code, 204)
