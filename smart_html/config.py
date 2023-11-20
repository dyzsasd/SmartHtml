import os

from dotenv import load_dotenv


load_dotenv()

config = {
    "db": {
        "backend": os.getenv("db_backend", "sqlite"),
        "sqlite_path": "mydatabase.db",
        "firebase_cred_file": os.getenv('firebase_cred_file'),
    },
    "engine": {
        "app_key": os.getenv('openai_key')
    }
}