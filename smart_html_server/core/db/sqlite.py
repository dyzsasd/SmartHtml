from datetime import datetime
import json
import sqlite3
import threading

from ...models.session import Session
from .base import DBClient

def get_db_connection(db_url):
    conn = sqlite3.connect(db_url)
    conn.row_factory = sqlite3.Row
    return conn


class SQLiteClient(DBClient):
    thread_local = threading.local()

    @classmethod
    def get_client(cls, db_url):
        if not hasattr(cls.thread_local, "db_client"):
            conn = get_db_connection(db_url)
            cls.thread_local.db_client = cls(conn)
        return cls.thread_local.db_client

    def __init__(self, conn):
        self.conn = conn

    def save_session(self, session: Session):
        self.conn.execute(
            '''
                INSERT INTO sessions (id, initial_requirements, web_pages, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(id)
                DO UPDATE SET
                    web_pages=excluded.web_pages,
                    updated_at=excluded.updated_at;
            ''', 
            (
                session._id, 
                session.initial_requirements, 
                json.dumps([wp.to_dict() for wp in session.web_pages]),
                session.created_at, 
                datetime.utcnow(),
            ),
        )
        self.conn.commit()

    def load_from_db(self, session_id):
        session_data = self.conn.execute('SELECT * FROM sessions WHERE id = ?', (session_id,)).fetchone()
        if session_data:
            web_pages = json.loads(session_data['web_pages'])

            return Session.from_dict({
                "id": session_data['id'],
                "initial_requirements": session_data['initial_requirements'],
                "web_pages": web_pages,
                "created_at": session_data['created_at'],
            })
        return None


get_client = SQLiteClient.get_client
