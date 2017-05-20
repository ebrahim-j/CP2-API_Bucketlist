import json
import unittest
from app import db
from app.models import User
from . test_base_setup import BaseTestCase

class TestAuthentication(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.client = self.app.test_client()
        user = User(username='ebrahimj')
        user.encrypt_password('pass123')
        self.data = {"username": "therock", "password": "pass"}
        db.session.add(user)
        db.session.commit()


    def test_register_user_successfully(self):
        response = self.client.post(
            '/api/auth/register', headers=self.request_headers(), data=json.dumps(self.data))
        print(response)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)[
                         "message"], "user created successfully")

    def test_register_with_existing_username(self):
        response = self.client.post(
            '/api/auth/register', headers=self.request_headers(), data=json.dumps(self.data))
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            '/api/auth/register', headers=self.request_headers(), data=json.dumps(self.data))
        result = json.loads(response.data)['error']
        self.assertTrue("Username already exists" in result)

    def test_login_successfully(self):
        response = self.client.post("/api/auth/register", data=json.dumps(
            self.data), headers=self.request_headers())
        print(response)
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            "/api/auth/login", data=json.dumps(self.data), headers=self.request_headers)
        result = json.loads(response.data)
        self.assertTrue("login successful" in result["message"])

    def test_login_with_wrong_data(self):
        response = self.client.post("/api/auth/register", data=json.dumps(
            self.data), headers=self.request_headers())
        self.assertEqual(response.status_code, 201)
        invalid_credentials = {"username": "ibrahim", "password": "wrongpass"}
        response = self.client.post(
            "/api/auth/login", data=json.dumps(invalid_credentials), headers=self.request_headers())
        data = json.loads(response.get_data(as_text=True))["error"]
        self.assertTrue("Invalid login credentials" in data)