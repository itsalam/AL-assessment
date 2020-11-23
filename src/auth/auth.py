import os
import datetime
from flask import jsonify
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    JWTManager, create_access_token,
    get_jwt_identity
)

def add_auth_config(app):
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=30)
    jwt = JWTManager(app)

def login(request):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

