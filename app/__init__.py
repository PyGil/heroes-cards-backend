from flask import Flask
from config import Config

from app.extensions import db, migrate, jwt
from app.api import api


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    api.init_app(app)

    return app
