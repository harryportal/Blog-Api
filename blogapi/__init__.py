from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from .config import Test_Config
from flask_httpauth import HTTPBasicAuth

api = Api()
db = SQLAlchemy()
auth = HTTPBasicAuth()

def create_app(config=Test_Config):
    app = Flask(__name__)
    app.config.from_object(config)
    api.init_app(app)
    db.init_app(app)
    return app

