from firebase_admin import credentials, initialize_app, firestore
from flask import Flask

from .firebase import FireBase
from .sqlite import SQLiteClient, init_db as init_sql

def init_db(app: Flask):
    if app.config.get("DB_BACKEND") == "firebase":
        # Initialize Firebase Admin
        cred = credentials.Certificate(app.config["DB_FIREBASE_CRED"])
        initialize_app(cred)
        firebase_client = firestore.client()
        client = FireBase(firebase_client)
        app.get_db_client = lambda : client
    else:
        db_path = app.config.get("DB_SQLITE_PATH", "mydatabase.db")
        init_sql(db_path)
        app.get_db_client = lambda : SQLiteClient.get_client(db_path)
