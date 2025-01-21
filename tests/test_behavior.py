"""
this file contains test related to the normal behavior of the routes
permission system is tested in test_security.py
"""

from utils.appTestCase import AppTestCase


class TestBehavior(AppTestCase):

    def test_get_account_unauthenticated(self):
        response = self.call_api("GET", "/account", use_auth=False)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.reason, "Unauthorized")

        body = response.json()

        self.assertEqual(body["detail"], "Not authenticated")

    def test_get_account(self):
        response = self.call_api("GET", "/account", use_auth=True)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertSchemaValidation(body, "tests/schemas/get_account.schema.json")

    def test_get_account_by_id(self):
        response = self.call_api("GET", "/account/1", use_auth=True)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertSchemaValidation(body, "tests/schemas/get_account_by_id.schema.json")

    def test_post_account(self):
        data = {"username": "testuser", "password": "securepassword"}
        response = self.call_api("POST", "/account", use_auth=False, body=data)
        body = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertSchemaValidation(body, "tests/schemas/post_account.schema.json")

    def test_patch_account(self):
        data = {"username": "updateduser"}
        response = self.call_api("PATCH", "/account/1", use_auth=True, body=data)
        self.assertEqual(response.status_code, 205)

    def test_delete_account(self):
        response = self.call_api("DELETE", "/account/1", use_auth=True)
        self.assertEqual(response.status_code, 204)

    def test_post_auth_login(self):
        data = {"username": "testuser", "password": "securepassword"}
        response = self.call_api("POST", "/auth/login", use_auth=False, body=data)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertSchemaValidation(body, "tests/schemas/auth_login.schema.json")

    def test_post_auth_logout(self):
        response = self.call_api("POST", "/auth/logout", use_auth=True)
        self.assertEqual(response.status_code, 204)

    def test_post_auth_refresh(self):
        response = self.call_api("POST", "/auth/refresh", use_auth=True)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertSchemaValidation(body, "tests/schemas/auth_refresh.schema.json")

    def test_get_profile(self):
        response = self.call_api("GET", "/profile", use_auth=True)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertSchemaValidation(body, "tests/schemas/get_profile.schema.json")

    def test_get_profile_by_id(self):
        response = self.call_api("GET", "/profile/1", use_auth=True)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertSchemaValidation(body, "tests/schemas/get_profile_by_id.schema.json")

    def test_get_profile_me(self):
        response = self.call_api("GET", "/profile/me", use_auth=True)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertSchemaValidation(body, "tests/schemas/get_profile_me.schema.json")

    def test_post_profile(self):
        data = {"name": "New Profile"}
        response = self.call_api("POST", "/profile", use_auth=True, body=data)
        body = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertSchemaValidation(body, "tests/schemas/post_profile.schema.json")

    def test_patch_profile(self):
        data = {"name": "Updated Profile"}
        response = self.call_api("PATCH", "/profile/1", use_auth=True, body=data)
        self.assertEqual(response.status_code, 205)

    def test_delete_profile(self):
        response = self.call_api("DELETE", "/profile/1", use_auth=True)
        self.assertEqual(response.status_code, 204)
