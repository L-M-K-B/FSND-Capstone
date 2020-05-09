import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS

from models import setup_db, Movie, Actress


# ##--------------------------------------------------## #
# ##--------------------- helpers --------------------## #
# ##--------------------------------------------------## #

def create_dict(query_res):
    res_dict = {}

    for single_res in query_res:
        res_dict[single_res.id] = single_res.title or single_res.name

    return res_dict


# ##--------------------------------------------------## #
# ##--------------------------------------------------## #
# ##--------------------------------------------------## #

def create_app():
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS  ')
        return response

    @app.route('/')
    def welcome():
        return 'This is the Capstone start page'

    # -- # requests movie table # -- #
    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies = Movie.query.all()

        if len(movies) == 0:
            abort(404)

        movies_dict = create_dict(movies)

        return jsonify({
            'success': True,
            'movies': movies_dict
        }), 200

    # -- # requests actresses table # -- #
    @app.route('/actresses', methods=['GET'])
    def get_actresses():
        actresses = Actress.query.all()

        if len(actresses) == 0:
            abort(404)

        actresses_list = [actress.format() for actress in actresses]

        return jsonify({
            'success': True,
            'actresses': actresses_list
        }), 200

    # -- # posts a new actress # -- #
    @app.route('/actress', methods=['POST'])
    def create_new_actress():
        actress = request.get_json()

        try:
            new_actress = Actress(**actress)
            new_actress.insert()

            return jsonify({
                'success': True,
                'created': new_actress.id
            })
        except SQLAlchemyError:
            abort(405)

    # -- # deletes an actress # -- #
    @app.route('/actress/<int:actress_id>', methods=['DELETE'])
    def delete_actress(actress_id):
        try:
            actress = Actress.query.filter(Actress.id == actress_id).one_or_none()

            if not actress:
                abort(422)

            actress.delete()

            return jsonify({
                'success': True,
                'deleted': actress_id,
            })
        except SQLAlchemyError:
            abort(422)

    # -- # modifies an actress # -- #
    @app.route('/actress/<int:actress_id>', methods=['PATCH'])
    def update_actress(actress_id):
        actress = Actress.query.filter(Actress.id == actress_id).one_or_none()

        if not actress:
            abort(404)

        data = request.get_json()

        if not data:
            abort(404)

        try:
            actress.name = data['name']
        except KeyError:
            pass

        try:
            actress.birth_date = data['birth_date']
        except KeyError:
            pass

        try:
            actress.gender = data['gender']
        except KeyError:
            pass

        try:
            actress.movies = data['movies']
        except KeyError:
            pass

        try:
            actress.update()

        except SQLAlchemyError:
            abort(422)

        return jsonify({
            'success': True,
            'actress': [actress.format()]
        }), 200

    # -- # Error Handlers # -- #
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
