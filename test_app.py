import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db


class TestCase(unittest.TestCase):

    def setUp(self):
        # Note: tokens need to be modified in case of testing
        with open('assistant.token') as assistant_file:
            self.token_assistant = assistant_file.read()
        with open('producer.token') as producer_file:
            self.token_producer = producer_file.read()

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
    def test_get_movies_without_permission(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_movies_assistant(self):
        res = self.client().get('/movies', headers={
            "Authorization": 'bearer '+self.token_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # -- # '/actresses', methods=['GET'] # -- #
    def test_get_actresses_without_permission(self):
        res = self.client().get('/actresses')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_actresses_producer(self):
        res = self.client().get('/actresses', headers={
            "Authorization": 'bearer '+self.token_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # -- # '/actress', methods=['POST'] # -- #
    def test_create_new_actress(self):
        res = self.client().post('/actress', headers={
            "Authorization": 'bearer '+self.token_producer}, json=self.new_actress)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_unauthorized_create_new_actress(self):
        res = self.client().post('/actress', headers={
            "Authorization": 'bearer '+self.token_assistant}, json=self.new_actress)

        self.assertEqual(res.status_code, 401)

    def test_405_creation_with_id_not_allowed_actress(self):
        res = self.client().post('/actress/42', headers={"Authorization": 'bearer '+self.token_producer},
                                 json=self.new_actress)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # -- # '/movie', methods=['POST'] # -- #
    def test_create_new_movie(self):
        res = self.client().post('/movie', headers={
            "Authorization": 'bearer '+self.token_producer}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_unauthorized_create_new_movie(self):
        res = self.client().post('/movie', headers={
            "Authorization": 'bearer '+self.token_assistant}, json=self.new_movie)

        self.assertEqual(res.status_code, 401)

    def test_404_creation_with_id_not_allowed_movie(self):
        res = self.client().post('/movie/42', headers={"Authorization": 'bearer '+self.token_producer},
                                 json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # -- # '/actress/<int:actress_id>', methods=['DELETE'] # -- #
    def test_delete_actress(self):
        new_id = self.client().post('/actress', headers={"Authorization": 'bearer '+self.token_producer},
                                    json=self.new_actress).json['created']
        res = self.client().delete(f'/actress/{new_id}', headers={"Authorization": 'bearer '+self.token_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_actress_does_not_exist(self):
        res = self.client().delete('/actress/42', headers={"Authorization": 'bearer '+self.token_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # -- # '/actress/<int:actress_id>', methods=['PATCH'] # -- #
    def test_patch_actress(self):
        new_id = self.client().post('/actress', headers={"Authorization": 'bearer '+self.token_producer},
                                    json=self.new_actress).json['created']
        res = self.client().patch(f'/actress/{new_id}', headers={"Authorization": 'bearer '+self.token_producer},
                                  json=self.modify_actress)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_creation_not_allowed(self):
        res = self.client().patch(f'/actress/42', headers={"Authorization": 'bearer '+self.token_producer},
                                  json=self.modify_actress)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


if __name__ == "__main__":
    unittest.main()
