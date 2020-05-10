import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db

class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgres://laura@localhost:5432/capstone-test"
        setup_db(self.app, self.database_path)

        self.new_movie = {
            'title': 'Hidden Figures',
            'release_date': '2016-12-25T00:00:00.000Z',
            'country': 'USA'
        }

        self.new_actress = {
            'name': 'Sofia Helin',
            'birth_date': '1972-04-25T00:00:00.000Z',
            'gender': 'female',
            'movies': []
        }

        self.modify_actress = {
            'birth_date': '2072-04-25T00:00:00.000Z'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    # -- # '/movies', methods=['GET'] # -- #
    def test_get_movies(self):
        self.client().post('/movie', json=self.new_movie)
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # -- # '/actresses', methods=['GET'] # -- #
    def test_get_actresses(self):
        self.client().post('/actress', json=self.new_actress)
        res = self.client().get('/actresses')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # -- # '/actress', methods=['POST'] # -- #
    def test_create_new_actress(self):
        res = self.client().post('/actress', json=self.new_actress)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_creation_not_allowed(self):
        res = self.client().post('/actress/42', json=self.new_actress)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # -- # '/actress/<int:actress_id>', methods=['DELETE'] # -- #
    def test_delete_actress(self):
        new_id = self.client().post('/actress', json=self.new_actress).json['created']
        res = self.client().delete(f'/actress/{new_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_actress_does_not_exist(self):
        res = self.client().delete('/actress/42')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # -- # '/actress/<int:actress_id>', methods=['PATCH'] # -- #
    def test_patch_actress(self):
        new_id = self.client().post('/actress', json=self.new_actress).json['created']
        res = self.client().patch(f'/actress/{new_id}', json=self.modify_actress)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_creation_not_allowed(self):
        res = self.client().patch(f'/actress/42', json=self.modify_actress)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

if __name__ == "__main__":
    unittest.main()