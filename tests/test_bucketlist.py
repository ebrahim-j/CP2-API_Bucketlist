import unittest
import json
from app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Sleep'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
        """This helper method helps register a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/api/v1/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        """This helper method helps log in a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/api/v1/auth/login', data=user_data)

    def test_bucketlist_creation(self):
        """Test API can create a bucketlist (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create a bucketlist by making a POST request
        res = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Sleep', str(res.data))

    def test_bucketlist_create_with_no_name(self):
        """Test API does NOT create an empty name bucketlist"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': ''})
        self.assertEqual(res.status_code, 400)
        self.assertIn('Bucketlist must have name', str(res.data))

    def test_api_can_get_all_bucketlists(self):
        """Test API can get all bucketlists (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create a bucketlist by making a POST request
        res = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(res.status_code, 201)

        # get all the bucketlists that belong to the test user by making a GET
        # request
        res = self.client().get(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('Sleep', str(res.data))

    def test_get_api_with_no_bucketlists(self):
        """Test API cannot get a bucketlist when not there (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # try to get all the bucketlists that belong to the test user by making a GET
        # request
        res = self.client().get(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue('No bucketlist yet', str(res.data))

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get a single bucketlist by using it's id."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)

        # assert that the bucketlist is created
        self.assertEqual(rv.status_code, 201)
        # get the response data in json format
        results = json.loads(rv.data.decode())

        result = self.client().get(
            '/api/v1/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        # assert that the bucketlist is returned given its ID
        self.assertEqual(result.status_code, 200)
        self.assertIn('Sleep', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test API can edit an existing bucketlist. (PUT request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # first, we create a bucketlist by making a POST request
        rv = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Sleep, repeat'})
        self.assertEqual(rv.status_code, 201)
        # get the json with the bucketlist
        results = json.loads(rv.data.decode())

        # then, we edit the created bucketlist by making a PUT request
        rv = self.client().put(
            '/api/v1/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data={
                "name": "Sleep, eat, repeat"
            })
        self.assertEqual(rv.status_code, 200)

        # finally, we get the edited bucketlist to see if it is actually
        # edited.
        results = self.client().get(
            '/api/v1/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Sleep, eat', str(results.data))

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucketlist. (DELETE request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Sleep, eat'})
        self.assertEqual(rv.status_code, 201)
        # get the bucketlist in json
        results = json.loads(rv.data.decode())

        # delete the bucketlist we just created
        res = self.client().delete(
            '/api/v1/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(res.status_code, 200)

        # Test to see if it exists, should return a 404
        result = self.client().get(
            '/api/v1/bucketlists/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def test_creates_item(self):
        """ Test API can add item to a bucketlist"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # Create a bucketlist
        rv = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Sleep, eat'})
        self.assertEqual(rv.status_code, 201)

        results = json.loads(rv.data.decode())

        # add item to the created bucketlist
        item_data = {'name': 'Eat good food'}
        res = self.client().post(
            '/api/v1/bucketlists/{}/items/'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token), data=item_data)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Eat good food', str(res.data))

    def test_create_item_with_no_name(self):
        """ Test API can add item to a bucketlist"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # Create a bucketlist
        rv = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Sleep, eat'})
        self.assertEqual(rv.status_code, 201)

        results = json.loads(rv.data.decode())

        # add item to the created bucketlist
        item_data = {'name': ''}
        res = self.client().post(
            '/api/v1/bucketlists/{}/items/'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token), data=item_data)
        self.assertEqual(res.status_code, 400)
        self.assertIn('Item must have name', str(res.data))

    def test_delete_bucketlist_item(self):
        """ Test API can delete a bucketlist item by ID"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # Create a bucketlist
        rv = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Sleep, eat'})
        self.assertEqual(rv.status_code, 201)

        results = json.loads(rv.data.decode())

        # add item to the created bucketlist
        item_data = {'name': 'Eat good food'}
        res = self.client().post(
            '/api/v1/bucketlists/{}/items/'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token), data=item_data)
        self.assertEqual(res.status_code, 201)
        item_id = json.loads(res.data.decode())['id']

        response = self.client().delete('/api/v1/bucketlists/{}/items/{}'.format(
            results['id'], item_id), headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 200)

    def test_item_update(self):
        """Test API can update an item"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # Create a bucketlist
        rv = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Sleep, eat'})
        self.assertEqual(rv.status_code, 201)

        results = json.loads(rv.data.decode())

        # add item to the created bucketlist
        item_data = {'name': 'Eat good food'}
        res = self.client().post(
            '/api/v1/bucketlists/{}/items/'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token), data=item_data)
        self.assertEqual(res.status_code, 201)

        item_id = json.loads(res.data.decode())['id']

        response = self.client().put('/api/v1/bucketlists/{}/items/{}'.format(
            results['id'], item_id), headers=dict(Authorization="Bearer " + access_token), data={'name': 'Eat healthy'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Eat healthy', str(response.data))

    def test_item_edit_with_no_name(self):
        """Test API does NOT update item with an empty name"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # Create a bucketlist
        rv = self.client().post(
            '/api/v1/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Sleep, eat'})
        self.assertEqual(rv.status_code, 201)

        results = json.loads(rv.data.decode())

        # add item to the created bucketlist
        item_data = {'name': 'Eat good food'}
        res = self.client().post(
            '/api/v1/bucketlists/{}/items/'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token), data=item_data)
        self.assertEqual(res.status_code, 201)

        item_id = json.loads(res.data.decode())['id']

        response = self.client().put('/api/v1/bucketlists/{}/items/{}'.format(
            results['id'], item_id), headers=dict(Authorization="Bearer " + access_token), data={'name': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Item name not valid', str(response.data))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
