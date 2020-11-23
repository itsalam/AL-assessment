from tests import BaseTest, byte_to_json, dummy_movie
import json
from src.schema.movie import MovieSchema
from src.models import db

class CRUDtest(BaseTest):
    

    def test_get_all_movies(self):
        jwt = byte_to_json(self.get_auth_point())['access_token']
        result = self.get_all_movies()
        self.assert200(result)
    
    def test_get_all_movies_no_entry(self):
        movie = dummy_movie()
        db.session.add(movie)
        db.session.commit()
        movies = byte_to_json(self.get_all_movies().data)['movies']
        self.assertEquals(movies[0], MovieSchema().dump(movie))

    def test_get_all_movies_with_entry(self):
        movie = dummy_movie()
        db.session.add(movie)
        db.session.commit()
        movies = byte_to_json(self.get_all_movies().data)['movies']
        self.assertEquals(movies[0], MovieSchema().dump(movie))

    def test_get_all_movies_multiple_entry(self):
        movieA = dummy_movie()
        movieB = dummy_movie(title="test2")
        db.session.add(movieA)
        db.session.add(movieB)
        db.session.commit()
        movies = byte_to_json(self.get_all_movies().data)['movies']
        self.assertEqual(movies[0], MovieSchema().dump(movieA))
        self.assertEqual(movies[1], MovieSchema().dump(movieB))


    def test_insert_movie(self, movie=dummy_movie()):
        result = self.insert_movie()
        self.assert200(result)

    def test_insert_bad_movie(self):
        movie ={"blahblahblah":"bleh"}
        jwt = byte_to_json(self.get_auth_point())['access_token']
        result = self.client.post("/api/", 
            headers={   "Content-Type": "application/json", 
                        "Authorization": "Bearer {}".format(jwt)
            },
            data=json.dumps(movie)
        )
        self.assert400(result)

    def test_insert_same(self):
        movieA = dummy_movie()
        movieB = dummy_movie()
        
        resultA = self.insert_movie(movieA)
        self.assert200(resultA)
        
        resultB = self.insert_movie(movieB)
        self.assert400(resultB)

    def test_insert_multiple(self):
        movies = [dummy_movie(), dummy_movie(title="test2")]
        for movie in movies:
            result = self.insert_movie(movie)
            self.assert200(result)

        movies_found = byte_to_json(self.get_all_movies().data)['movies']
        for i, movie in enumerate(movies):
            self.assertEquals(json.dumps(movies_found[i], sort_keys=True), json.dumps(MovieSchema().dump(movie), sort_keys=True))



    def test_delete_movie(self):
        targetTitle = 'deletethismovie'
        movieEntries = 5
        moviesToNotDelete = [ dummy_movie("title{}".format(i)) for i in range(5) ]
        
        for movie in moviesToNotDelete + [dummy_movie(targetTitle)]:
            db.session.add(movie)
        db.session.commit()

        allMovies = byte_to_json(self.get_all_movies().data)['movies']
        assert(len(allMovies) == movieEntries + 1)

        result = self.delete_movie(targetTitle)
        allMovies = byte_to_json(self.get_all_movies().data)['movies']
        self.assert200(result)
        
        assert(len(allMovies) == movieEntries)
        for movie in allMovies:
            self.assertNotEqual(movie['title'], targetTitle)