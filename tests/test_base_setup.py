import unittest
from app import create_app, db


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def request_headers(self, token=None):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        if token:
            headers.update({'Authorization': token})
        return headers
