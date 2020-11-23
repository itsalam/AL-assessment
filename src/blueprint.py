from flask import Blueprint, request, jsonify
import os
from src.auth.auth import login
from flask_jwt_extended import jwt_required
from src.operations.movie import MovieOperations
from src.models.movie import Movie
from src.schema.movie import MovieSearch, MovieSchema
from src.helper import request_to_schema

movie_service = Blueprint('api', __name__)

@movie_service.route("/")
@jwt_required
def greeting():
    query = MovieOperations.get_all()
    return {"movies": [MovieSchema().dump(movie) for movie in query]}, 200

@movie_service.route("/", methods=["POST"])
@jwt_required
def insertMovie():
    try: 
        result = request_to_schema(request)
        result = MovieSchema().load(result)
        if not isinstance(result, Movie):
            return result, 400
        result = MovieOperations.add_movie(result)
        return MovieSchema().dump(result), 200
    except Exception as e:
        return {"msg": "Movie could not be added: {}".format(e)}, 400
    

@movie_service.route("/", methods=["DELETE"])
@jwt_required
def deleteMovie():
    title = request.json.get("title", None)
    if not isinstance(title, str):
        return {"msg": "Missing title parameter"}, 400
    result = MovieOperations.del_movie(title)
    if not isinstance(result, Movie):
        return result
    return MovieSchema().dump(result), 200

@movie_service.route("/expiredMovies", methods=["GET"])
@jwt_required
def expiredMovies():
    fields = { i: request.json.get(i, None) for i in ["from", "to"]}
    for (field, value) in fields.items():
        if value is None:
            return {"msg": "Field {} is Missing".format(field)}, 400 
    if fields["from"] > fields["to"]:
        return {"msg": "Query invalid, 'from' date is after 'to' date."}, 400
    query = MovieOperations.query_expired_movies(fields["from"], fields["to"])
    return {"movies": [MovieSchema().dump(movie) for movie in query]} , 200

@movie_service.route("/search", methods=["GET"])
@jwt_required
def searchMovies():
    search = request_to_schema(request, toSearch=True)
    query = MovieOperations.search_movie(search)
    return {"movies": [MovieSchema().dump(movie) for movie in query]}, 200

@movie_service.route("/token", methods=['POST'])
def returnToken():
    return login(request)

# # if __name__ == "__main__":
# #     app.run(host='0.0.0.0')
# movie_service.run()