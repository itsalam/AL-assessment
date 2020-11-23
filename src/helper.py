import datetime as dt
import re
from src.schema.movie import MovieSchema, MovieSearch
from marshmallow.exceptions import ValidationError
from src.models.movie import Movie
from flask import jsonify

def request_to_schema(request, toSearch = False):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    fields = ['title', 'genre', 'expiry_date', 'release_year']
    args = {}
    schema = MovieSchema() if not toSearch else MovieSearch()

    for field in fields: 
        arg = request.json.get(field, None)
        if not arg and not toSearch:
            return jsonify({"msg": "Missing {} parameter".format(field)}), 400
        if field is 'expiry_date' and arg != None:
            #This is a nightmare someone needs to make this a library 
            arg = dt.datetime(*[int(num) for num in re.compile("[/\:-]").split(arg)])
        args[field] = arg
    try:
        result = schema.dump(args)
    except ValidationError as e:
        return jsonify({"msg": "Errors with request body: {}".format(e)}), 400
    return result



def movie_dump(movie: Movie):
    return MovieSchema().dump(movie)