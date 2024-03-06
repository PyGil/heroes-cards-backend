import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI") or "sqlite:///" + os.path.join(
        basedir, "database", "app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_VALIDATE = True
    JWT_SECRET_KEY = os.getenv("FLASK_JWT_SECRET_KEY")
