import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    DB_BACKEND = os.getenv("db_backend", "sqlite")
    DB_SQLITE_PATH = "mydatabase.db"
    DB_FIREBASE_CRED = os.getenv('firebase_cred_file')

    ENGINE_OPENAI_APP_KEY = os.getenv('openai_key')
