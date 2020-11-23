import os
from flask import Flask
from flask_marshmallow import Marshmallow
from src.auth.auth import add_auth_config
from flask_sqlalchemy import SQLAlchemy

def create_app():

    service = Flask(__name__)
    add_auth_config(service)
    service.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
    db = SQLAlchemy(service)
    ma = Marshmallow(service)

    from src.blueprint import movie_service
    service.register_blueprint(movie_service, url_prefix='/api')
    return service