import os
import tempfile
import pytest
import werkzeug
import json
from datetime import date, timedelta
from dotenv import load_dotenv
from flask_testing import TestCase
from src import create_app
from src.models import db
from src.models.movie import Movie
from src.schema.movie import MovieSchema

werkzeug.cached_property = werkzeug.utils.cached_property
load_dotenv("tests/test.env")

##helpers
def byte_to_json(byte_data):
    json_data = byte_data.decode('utf8').replace("'", '"')
    data = json.loads(json_data)
    return data

def dummy_movie(title="testTitle", genre="testgenre", release_year="2000", expiry_date= date.today()):
    return Movie(title, genre, release_year, expiry_date)

class BaseTest(TestCase):
    
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    TESTING = True
    render_templates = False

    def create_app(self):
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI '] = os.environ["SQLALCHEMY_DATABASE_URI"]
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def get_auth_point(self):
        result = self.client.post("/api/token", content_type="application/json", data=json.dumps({"username":"testusername"}), follow_redirects=True)
        return result.data

    def get_all_movies(self):
        jwt = byte_to_json(self.get_auth_point())['access_token']
        result = self.client.get("/api/", headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(jwt)})
        return result

    def get_expired_movies(self, start, end):
        jwt = byte_to_json(self.get_auth_point())['access_token']
        result = self.client.get("/api/expiredMovies", 
            headers={   "Content-Type": "application/json", 
                        "Authorization": "Bearer {}".format(jwt)
            },
            data=json.dumps({'from': start.isoformat(), 'to': end.isoformat()})
        )
        return result

    def delete_movie(self, title):
        jwt = byte_to_json(self.get_auth_point())['access_token']
        result = self.client.delete("/api/", 
            headers={   "Content-Type": "application/json", 
                        "Authorization": "Bearer {}".format(jwt)
            },
            data=json.dumps({"title": title})
        )
        return result

    def insert_movie(self, movie=dummy_movie()):
        jwt = byte_to_json(self.get_auth_point())['access_token']
        result = self.client.post("/api/", 
            headers={   "Content-Type": "application/json", 
                        "Authorization": "Bearer {}".format(jwt)
            },
            data=MovieSchema().dumps(movie)
        )
        return result

    def search_movie(self, query):
        jwt = byte_to_json(self.get_auth_point())['access_token']
        result = self.client.get("/api/search", 
            headers={   "Content-Type": "application/json", 
                        "Authorization": "Bearer {}".format(jwt)
            },
            data=json.dumps(query)
        )
        return result
