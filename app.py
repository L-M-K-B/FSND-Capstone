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
    app = Flask(__name__)
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

    # -- # requests for movie table # -- #
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

    # -- # requests for actresses table # -- #
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

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
