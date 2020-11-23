from tests import BaseTest, byte_to_json, dummy_movie
from datetime import date, timedelta
from src.models import db

class ExpirySearchTest(BaseTest):

    def test_expired_movies(self):
        today = date.today()
        db.session.add(dummy_movie(title="A"))
        db.session.add(dummy_movie(title="B", expiry_date=today - timedelta(days=2)))
        start, end = today - timedelta(days=1), today + timedelta(days=1)

        result = self.get_expired_movies(start, end)
        self.assert200(result)
        expiredMovies =  byte_to_json(result.data)['movies']
        allMovies = byte_to_json(self.get_all_movies().data)['movies']
        self.assertNotEqual(len(expiredMovies), len(allMovies))
    
    def test_expired_movies_bad_fields(self):
        today = date.today()
        start, end = today + timedelta(days=1), today - timedelta(days=1)
        result = self.get_expired_movies(start, end)
        self.assert400(result)