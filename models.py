from sqlalchemy import Column, String, Integer, DateTime, ARRAY, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

database_path = "postgres://laura@localhost:5432/capstone"

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()

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
