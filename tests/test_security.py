"""
this file test the permission system assuring that each route can only be accessed under desired permissions
"""

from utils.appTestCase import AppTestCase


class TestAuthorization(AppTestCase):

    def test_get_account_no_privileges(self):
        response = self.call_api("GET", "/account", use_auth=False)
        self.assertEqual(response.status_code, 401)

    def test_get_account_by_id_no_privileges(self):
        response = self.call_api("GET", "/account/1", use_auth=False)
        self.assertEqual(response.status_code, 401)

    def test_post_account_no_privileges(self):
        data = {"username": "testuser", "password": "securepassword"}
        response = self.call_api("POST", "/account", use_auth=False, body=data)
        self.assertEqual(response.status_code, 401)

    def test_patch_account_no_privileges(self):
        data = {"username": "updateduser"}
        response = self.call_api("PATCH", "/account/1", use_auth=False, body=data)
        self.assertEqual(response.status_code, 401)

    def test_delete_account_no_privileges(self):
        response = self.call_api("DELETE", "/account/1", use_auth=False)
        self.assertEqual(response.status_code, 401)

    def test_get_profile_no_privileges(self):
        response = self.call_api("GET", "/profile", use_auth=False)
        self.assertEqual(response.status_code, 401)

    def test_get_profile_by_id_no_privileges(self):
        response = self.call_api("GET", "/profile/1", use_auth=False)
        self.assertEqual(response.status_code, 401)

    def test_get_profile_me_no_privileges(self):
        response = self.call_api("GET", "/profile/me", use_auth=False)
        self.assertEqual(response.status_code, 401)

    def test_post_profile_no_privileges(self):
        data = {"name": "New Profile"}
        response = self.call_api("POST", "/profile", use_auth=False, body=data)
        self.assertEqual(response.status_code, 401)

    def test_patch_profile_no_privileges(self):
        data = {"name": "Updated Profile"}
        response = self.call_api("PATCH", "/profile/1", use_auth=False, body=data)
        self.assertEqual(response.status_code, 401)

    def test_delete_profile_no_privileges(self):
        response = self.call_api("DELETE", "/profile/1", use_auth=False)
        self.assertEqual(response.status_code, 401)
