from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

database_path = "postgres://laura@localhost:5432/trivia"

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


# -------------------------------------------- #
# Models.
# -------------------------------------------- #

class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    country = db.Column(db.String(120))

    def __init__(self, title, release_date, country):
        self.title = title
        self.release_date = release_date
        self.country = country

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'country': self.country,
        }


class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.DateTime)
    gender = db.Column(db.String(120))

    def __init__(self, name, birth_date, gender):
        self.name = name
        self.birth_date = birth_date
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_date': self.birth_date,
            'gender': self.gender,
        }
