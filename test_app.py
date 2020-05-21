import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db

class TestCase(unittest.TestCase):

    def setUp(self):
        self.token_assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNhQ1YtZ01rd2RFMnZhSFQ5MjdMcyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbG1rYi1jYXBzdG9uZS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViODIzZGFkMGZhMWUwYmZlZWYxMjU3IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODkzNTAzNzMsImV4cCI6MTU4OTM1NzU3MywiYXpwIjoid2R3NkRjcTRrZnNZVmt1djM0YU1OMnlDa1pKYTdTU0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInJlYWQ6YWN0cmVzc2VzIiwicmVhZDptb3ZpZXMiXX0.MA2dZhZ82Jd1wwqPN_UagnefV1_kGj7GOQ06SopwcZpvAlV2gBTVLcKdjbUt5QhOsDY5v2X1yPLnL-RiIKo3BWQMnAMnzCdlK2B0k2kVtZXq_Ref6yD7o-FSW3vQ_u_mWMEiwTk80HRqULZwHymKxqx1OmFpV9mtcD7TYaJQS9AsOELgRtYEoKqpocFeSYnueR9qF3cVOaJbP_tzU-nxY5fy_0dKX6dFZxAQix6Al9ZvsRtXuuO2s7_DyOwjaOdoT7V8jkf9_U9KuED46joK3_j9ip6SYsUXlq0JQg7tMP1BYhsfbLAg5CpFTo5JjNRwgJnT9PQ_iY6Y2rkCtsZxbg'
        self.token_producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNhQ1YtZ01rd2RFMnZhSFQ5MjdMcyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbG1rYi1jYXBzdG9uZS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViODI0YTdkMGZhMWUwYmZlZWYxMzBmIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODkxMjc0NDIsImV4cCI6MTU4OTEzNDY0MiwiYXpwIjoid2R3NkRjcTRrZnNZVmt1djM0YU1OMnlDa1pKYTdTU0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RyZXNzZXMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdHJlc3NlcyIsImRlbGV0ZTptb3ZpZSIsIm1vZGlmeTphY3RyZXNzZXMiLCJtb2RpZnk6bW92aWUiLCJyZWFkOmFjdHJlc3NlcyIsInJlYWQ6bW92aWVzIl19.U8j9cjOiD449Zzmuuj62h6WdYqced7DTx7A8xz5mnJyfdv0McSJkCcYBK6AOb7SqlsoOjjBlRwVKcvhJcbXUD-CxbDx_LKQ2aysve3aQQBaLyNrHVaByiiGHsTVplvxjS0aoazPO-8vzJzQXdp4zUSDxkoqnoMeCXAhDGbpbkQ1Y6Y9JcGUCUDb0LfpSzGqkXnGd2gPh3onRbrUrVnZdk9ujt9PR_tQgxa5DJiumJxf6FWlACYDI666AmAg1LJxcITkjjftDc8Qk42Fx_szj7WF-pf5iYGiK2GCEj9x1waSf6F1pf8eoKAs_izxx1F2LwdvVleZTrxnvAATo81dYFA'
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

    def test_405_creation_not_allowed(self):
        res = self.client().post('/actress/42', headers={"Authorization": 'bearer '+self.token_producer}
                                 , json=self.new_actress)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # -- # '/actress/<int:actress_id>', methods=['DELETE'] # -- #
    def test_delete_actress(self):
        new_id = self.client().post('/actress', headers={"Authorization": 'bearer '+self.token_producer}
                                    , json=self.new_actress).json['created']
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