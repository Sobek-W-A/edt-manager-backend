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

        self.assertSchemaValidation(body, "tests/schemas/get_account.schema.json")
