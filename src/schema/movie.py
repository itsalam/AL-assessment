from datetime import datetime
from marshmallow import Schema, fields, validate, post_load
from src.models.movie import Movie

def validate_release_year(n):
    return n < datetime.now().year

class MovieSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1))
    genre = fields.Str(required=True, validate=validate.Length(min=1))
    release_year = fields.Number(required=True, validate= validate_release_year)
    expiry_date = fields.Date(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return Movie(**data)

class MovieSearch(Schema):
    title = fields.Str(validate=validate.Length(min=1))
    genre = fields.Str(validate=validate.Length(min=1))
    release_year = fields.Integer(validate= validate_release_year)
    expiry_date = fields.Date()

    @post_load
    def make_search(self, data, **kwargs):
        return MovieSearch(**data)
