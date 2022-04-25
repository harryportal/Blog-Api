from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Test_Config

api = Api()
db = SQLAlchemy()
auth = HTTPBasicAuth()
ma = Marshmallow()
migrate = Migrate()


def create_app(config=Test_Config):
    app = Flask(__name__)
    app.config.from_object(config)
    api.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    return app


from blogapi import auth, user
