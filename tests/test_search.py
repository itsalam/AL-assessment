from tests import BaseTest, byte_to_json, dummy_movie
from datetime import date, timedelta
from src.models import db
from src.schema.movie import MovieSchema
import json

class SearchTest(BaseTest):

    def test_search_title(self):
        movie = dummy_movie()
        movie_to_not_find = dummy_movie(title="somethingElse")
        db.session.add(movie)
        db.session.add(movie_to_not_find)
        db.session.commit()
        
        result = self.search_movie({'title': movie.title})
        self.assert200(result)

        movies = byte_to_json(result.data)['movies']
        
        self.assertEquals(json.dumps(movies[0], sort_keys=True), json.dumps(MovieSchema().dump(movie), sort_keys=True))

    def test_search_datetime(self):
        today = date.today()
        not_today = date.today() - timedelta(days=3)
        today_movie = dummy_movie(expiry_date=today)
        today_movie2 = dummy_movie(title="today2", expiry_date=today)
        not_today_movie = dummy_movie(title="not today", expiry_date=not_today)
        db.session.add(today_movie)
        db.session.add(today_movie2)
        db.session.add(not_today_movie)
        db.session.commit()
        
        result = self.search_movie({'expiry_date': today.isoformat()})
        self.assert200(result)

        movies = byte_to_json(result.data)['movies']
        self.assertEquals(len(movies), 2)

    def test_search_multi_fields(self):
        title_to_search = "find me"
        genre_to_search = "find me too"
        movie_to_search = dummy_movie(title=title_to_search, genre=genre_to_search)
        movie_to_not_find = dummy_movie(title="somethingElse")
        db.session.add(movie_to_search)
        db.session.add(movie_to_not_find)
        db.session.commit()
        
        result = self.search_movie({'title': title_to_search, 'genre': genre_to_search})
        self.assert200(result)
        
        movies = byte_to_json(result.data)['movies']
        self.assertEquals(json.dumps(movies[0], sort_keys=True), json.dumps(MovieSchema().dump(movie_to_search), sort_keys=True))
