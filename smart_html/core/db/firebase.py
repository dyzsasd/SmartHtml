import firebase_admin
from firebase_admin import credentials, firestore
from flask import g

from ...models.session import Session
from .base import DBClient


class FireBase(DBClient):
    @classmethod
    def get_client(cls, cred_file):
        if 'db_client' not in g:
            # Initialize Firebase Admin
            cred = credentials.Certificate(cred_file)
            firebase_admin.initialize_app(cred)

            # Get Firestore database instance
            firebase_client = firestore.client()
            g.db_client = cls(firebase_client)
        return g.db_client

    def __init__(self, firebase_client):
        self.firebase_client = firebase_client

    def save_session(self, session: Session):
        sessions_ref = self.firebase_client.collection('sessions')
        sessions_ref.document(session._id).set(session.to_dict())

    def load_from_db(self, session_id):
        sessions_ref = self.firebase_client.collection('sessions')
        doc = sessions_ref.document(session_id).get()
        if doc.exists:
            return Session.from_dict(doc.to_dict())
        return None
