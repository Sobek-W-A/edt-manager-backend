"""
this file test the response time per command under reasonable to heavy load
output have to be manually checked
"""

import time
from typing import Any

from utils.appTestCase import AppTestCase


class TestPerformance(AppTestCase):

    MAX_RESPONSE_TIME = 2100

    def measure_response_time(
        self, method: str, url: str, *, use_auth: bool, body: dict[str, Any] = {}):
        start_time = time.time()
        self.call_api(method, url, use_auth=use_auth, body=body)
        end_time = time.time()

        response_time = (end_time - start_time) * 1000
        
        self.assertLessEqual(
            response_time,
            self.MAX_RESPONSE_TIME,
            f"Response time for {method} {url} exceeded limit: {response_time:.2f} ms",
        )

    def test_get_account(self):
        self.measure_response_time("GET", "/account", use_auth=True)

    def test_get_account_by_id(self):
        self.measure_response_time("GET", "/account/1", use_auth=True)

    def test_post_account(self):
        data = {"username": "testuser", "password": "securepassword"}
        self.measure_response_time("POST", "/account", use_auth=False, body=data)

    def test_patch_account(self):
        data = {"username": "updateduser"}
        self.measure_response_time("PATCH", "/account/1", use_auth=True, body=data)

    def test_post_auth_login(self):
        data = {"username": "testuser", "password": "securepassword"}
        self.measure_response_time("POST", "/auth/login", use_auth=False, body=data)

    def test_post_auth_logout(self):
        self.measure_response_time("POST", "/auth/logout", use_auth=True)

    def test_post_auth_refresh(self):
        self.measure_response_time("POST", "/auth/refresh", use_auth=True)

    def test_get_profile(self):
        self.measure_response_time("GET", "/profile", use_auth=True)

    def test_get_profile_by_id(self):
        self.measure_response_time("GET", "/profile/1", use_auth=True)

    def test_get_profile_me(self):
        self.measure_response_time("GET", "/profile/me", use_auth=True)

    def test_post_profile(self):
        data = {"name": "New Profile"}
        self.measure_response_time("POST", "/profile", use_auth=True, body=data)

    def test_patch_profile(self):
        data = {"name": "Updated Profile"}
        self.measure_response_time("PATCH", "/profile/1", use_auth=True, body=data)

