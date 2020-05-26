import os
from sqlalchemy import Column, String, Integer, DateTime, ARRAY, ForeignKey
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DATABASE_URL = os.environ['DATABASE_URL']


def setup_db(app, database_path=DATABASE_URL):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.delete
    db.create_all()

    new_movie = Movie(title="Hidden Figures", release_date="2016-12-25T00:00:00.000Z", country="USA")
    new_movie.insert()

    new_actress = Actress(name='Taraji P Henson', birth_date='1970-09-11T00:00:00.000Z', gender='female',
                          movies=[new_movie.id])
    new_actress.insert()


# -------------------------------------------- #
# Models.
# -------------------------------------------- #

class Movie(db.Model):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(DateTime)
    country = Column(String(120))

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


class Actress(db.Model):
    __tablename__ = 'actress'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_date = Column(DateTime)
    gender = Column(String(120))
    movies = Column(ARRAY(Integer, ForeignKey('movie.id')))

    def __init__(self, name, birth_date, gender, movies):
        self.name = name
        self.birth_date = birth_date
        self.gender = gender
        self.movies = movies

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
            'movies': self.movies,
        }
