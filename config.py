import os
from dotenv import load_dotenv
import secrets
from pathlib import Path
from urllib.parse import quote_plus

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
SQLITE_DATABASE_PATH = BASE_DIR / "instance" / "mitoverso.db"

class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "chave-mitoverso"
    )

    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(16))
    CURRENT_DATABASE = os.getenv("CURRENT_DATABASE", "sqlite").lower()

    if CURRENT_DATABASE == "sqlite":
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_DATABASE_PATH}"
    elif CURRENT_DATABASE == "mysql":
        SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USERNAME}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    elif CURRENT_DATABASE == "postgresql":
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False