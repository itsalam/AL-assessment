from src.models import db
from src.models.movie import Movie
from src.schema.movie import MovieSchema, MovieSearch
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask import jsonify

class MovieOperations:

    @staticmethod
    def get_all():
        return Movie.query.all()

    @staticmethod
    def add_movie(movie: Movie):
        db.session.add(movie)
        db.session.commit()
        return movie

    @staticmethod
    def del_movie(movieTitle):
        movie = Movie.query.get(movieTitle)
        if movie is None:
            return jsonify({"msg": "Movie was not found"}), 400
        db.session.delete(movie)
        db.session.commit()
        return movie

    @staticmethod
    def search_movie(movieSearch: MovieSearch):
        fields = dict(movieSearch)
        fields = [(field, value) for (field, value) in fields.items() if value is not None]
        return Movie.query.filter(and_(*[getattr(Movie, field).contains(value) for (field, value) in fields])).all()

    @staticmethod
    def query_expired_movies(start, end):
        return Movie.query.filter(and_(Movie.expiry_date >= start, Movie.expiry_date <= end)).all()

