from firebase_admin import firestore
from flask import g

from ...models.session import Session
from .base import DBClient


class FireBase(DBClient):
    @classmethod
    def get_client(cls):
        if 'db_client' not in g:
            # Get Firestore database instance
            firebase_client = firestore.client()
            g.db_client = cls(firebase_client)
        return g.db_client

    def __init__(self, firebase_client):
        self.firebase_client = firebase_client

    def save_session(self, session: Session):
        sessions_ref = self.firebase_client.collection('sessions')
        sessions_ref.document(session._id).set(session.to_json())

    def load_from_db(self, session_id):
        sessions_ref = self.firebase_client.collection('sessions')
        doc = sessions_ref.document(session_id).get()
        if doc.exists:
            return Session.from_json(doc.to_json())
        return None
