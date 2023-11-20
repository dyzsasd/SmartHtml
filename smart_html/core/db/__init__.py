from flask import Flask

from .firebase import FireBase
from .sqlite import SQLiteClient

def init_db(app: Flask):
    db_config = app.config.get("db", {})
    if db_config.get("backend") == "firebase":
        app.get_db_client = lambda : FireBase.get_client(db_config["firebase_cred_file"])
    else:
        app.get_db_client = lambda : SQLiteClient.get_client(db_config.get("sqlite_path", "mydatabase.db"))
