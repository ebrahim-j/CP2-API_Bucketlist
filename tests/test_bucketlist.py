import unittest
import os
import json
from app import create_app, db
from app.models import User, Bucketlist, Item
from . test_base_setup import BaseTestCase

class TestBucketListAPI(BaseTestCase):

    def setUp(self):
        super().setUp()
        user = User(username='ebrahimj')
        user.encrypt_password('pass123')
        db.session.add(user)
        db.session.commit()
        bucketlist = Bucketlist(name='Sleep', created_by=user.id)
        db.session.add(bucketlist)
        item = Item(bucketlist_id=bucketlist.id, name='Have dreams')
        db.session.add(item)
        db.session.commit()
        self.client = self.app.test_client()
        token = user.generate_auth_token().decode('utf-8')
        self.auth_token = "Bearer {}".format(token)

    def test_create_bucketlist(self):
        data = {"name": "play football"}
        response = self.client.post(
            "/api/bucketlists/", headers=self.request_headers(self.auth_token), data=json.dumps(data))
        print(response.data)
        self.assertEqual("created bucketlist", json.loads(response.data)["message"])
        # self.assertEqual(response.status_code, 201)

    def test_create_bucketlist_without_authentication(self):
        data = {"name": "play football"}
        response = self.client.post(
            "/api/bucketlists/", headers=self.request_headers(), data=json.dumps(data))
        self.assertEqual(response.status_code, 401)

    def test_create_bucketlist_with_existing_name(self):
        data = {"name": "play football"}
        response = self.client.post(
            "/api/bucketlists/", headers=self.request_headers(self.auth_token), data=json.dumps(data))
        self.assertTrue(response.status_code == 201)
        response = self.client.post(
            "/api/bucketlists/", headers=self.request_headers(self.auth_token), data=json.dumps(data))
        result = str(response.data)
        self.assertTrue("bucketlist already exists" in result)

    def test_get_bucketlist(self):
        data = {"name": "play football"}
        response = self.client.post("/api/bucketlists/", headers=self.request_headers(self.auth_token), data=json.dumps(data))
        self.assertEqual(response.status_code, 201)
        response = self.client.get(
            "/api/bucketlists/1/", headers=self.request_headers(self.auth_token))
        result = str(response.data)
        self.assertTrue("play football" in result)
        self.assertEqual(response.status_code, 200)

    def test_get_bucketlists_without_authentication(self):
        response = self.client.get(
            "/api/bucketlists/", headers=self.request_headers())
        self.assertTrue(response.status_code == 401)

    def test_get_non_existent_bucketlist(self):
        data = {"name": "play football"}
        response = self.client.post("/api/bucketlists/", headers=self.request_headers(self.auth_token), data=json.dumps(data))
        self.assertEqual(response.status_code, 201)
        response = self.client.get(
            "/api/bucketlists/6/", headers=self.request_headers(self.auth_token))
        result = str(response.data)
        self.assertEqual("Bucketlist does not exist", json.loads(result)["error"])

    def test_update_bucketlist(self):
        data = {"name": "play football"}
        response = self.client.post("/api/bucketlists/", headers=self.request_headers(self.auth_token), data=json.dumps(data))
        self.assertEqual(response.status_code, 201)
        response = self.client.put("/api/bucketlists/1/", headers=self.request_headers(self.auth_token), data=json.dumps({"name": "Simulations"}))
        self.assertEqual(response.status_code, 200)
        result = json.loads(str(response.data))["message"]
        self.assertEqual("Successfully updated", result)

    def test_update_non_existent_bucketlist(self):
        data = {"name": "play football"}
        response = self.client.post("/api/bucketlists/", headers=self.request_headers(self.auth_token), data=json.dumps(data))
        self.assertEqual(response.status_code, 201)
        response = self.client.put("/api/bucketlists/8/", headers=self.request_headers(self.auth_token), data=json.dumps({"name": "Simulations"}))
        result = str(response.data)
        self.assertTrue("could not find the specified bucketlist" in result)

    def test_create_bucketlist_item(self):
        data = {"name": "play football"}
        response = self.client.post("/api/bucketlists/", headers=self.request_headers(self.auth_token), data=json.dumps(data))
        self.assertEqual(response.status_code, 201)
        item_data = {"name": "tackle hard"}
        response = self.client.post(
            "/api/bucketlists/1/items/", headers=self.request_headers(self.auth_token), data=json.dumps(item_data))
        self.assertEqual(response.status_code, 201)

    def test_update_bucketlist_item(self):
        data = {"name": "play football"}
        response = self.client.post("/api/bucketlists/", headers=self.request_headers(self.auth_token), data=json.dumps(data))
        self.assertEqual(response.status_code, 201)
        item_data = {"name": "tackle hard"}
        response = self.client.post(
            "/api/bucketlists/1/items/", headers=self.request_headers(self.auth_token), data=json.dumps(item_data))
        self.assertEqual(response.status_code, 201)
        response = self.client.put("/api/bucketlists/1/items/1/", headers=self.request_headers(self.auth_token), data=json.dumps({"name": "tackle smart"}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Successfully updated" in json.loads(response.get_data(as_text=True))["message"])

    def test_delete_bucketlist(self):
        data = {"name": "play football"}
        response = self.client.post("/api/bucketlists/", headers=self.request_headers(self.auth_token), data=json.dumps(data))
        self.assertEqual(response.status_code, 201)
        response = self.client.delete(
            "/api/bucketlists/1/", headers=self.request_headers(self.auth_token))
        self.assertTrue(
            "bucketlist deleted" in response.get_data(as_text=True))

    def test_delete_bucketlist_item(self):
        data = {"name": "play football"}
        response = self.client.post("/api/bucketlists/", headers=self.request_headers(self.auth_token), data=json.dumps(data))
        self.assertEqual(response.status_code, 201)
        item_data = {"name": "score a goal"}
        response = self.client.post(
            "/api/bucketlists/1/items/", headers=self.request_headers(self.auth_token), data=json.dumps(item_data))
        self.assertEqual(response.status_code, 201)
        response = self.client.delete(
            "/api/bucketlists/1/items/1/", headers=self.request_headers(self.auth_token))
        result = response.get_data(as_text=True)
        self.assertTrue("item deleted" in result)


if __name__ == "__main__":
    unittest.main()
