from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Test_Config, ProductionConfig
from flask_cors import CORS



api = Api()
db = SQLAlchemy()
auth = HTTPBasicAuth()
ma = Marshmallow()
migrate = Migrate()



def create_app(config=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    api.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from .Oauth import oauth, gauth
    oauth.init_app(app)
    app.register_blueprint(gauth)


    return app


from blogapi import auth, user, posts, Oauth
