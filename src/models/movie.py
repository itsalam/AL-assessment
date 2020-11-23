import datetime
from datetime import date
from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow
from src.models import db

class Movie(db.Model):

    __tablename__ = "movies"

    title = db.Column(db.String(50), primary_key=True, unique=True)
    genre = db.Column(db.String(25))
    release_year = db.Column(db.Integer)
    expiry_date =  db.Column(db.DateTime)

    def __init__(self, title, genre, release_year, expiry_date):
        self.title = title
        self.genre = genre
        self.release_year = release_year
        self.expiry_date = expiry_date
