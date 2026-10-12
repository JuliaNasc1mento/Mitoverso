import os

class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "chave-mitoverso"
    )

    SQLALCHEMY_DATABASE_URI = "sqlite:///mitoverso.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False