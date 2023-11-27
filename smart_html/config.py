import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    DB_BACKEND = os.getenv("db_backend", "sqlite")
    DB_SQLITE_PATH = "mydatabase.db"

    DB_FIREBASE_CRED = os.getenv('firebase_cred_file')
    if DB_BACKEND == "firebase" and not DB_FIREBASE_CRED:  # DB_FIREBASE_CRED is empty or None
        raise RuntimeError(
            "firebase_cred_file is missing, please check .env or environment settings")

    ENGINE_OPENAI_APP_KEY = os.getenv('openai_key')
    if not ENGINE_OPENAI_APP_KEY:  # ENGINE_OPENAI_APP_KEY is empty or None
        raise RuntimeError("openai_key is missing, please check .env or environment settings")

    WEB_APP_HOST = os.getenv('web_app_host')
