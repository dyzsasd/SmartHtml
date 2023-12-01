from datetime import datetime
import json
import sqlite3

from flask import g

from ...models.session import Session
from .base import DBClient

def get_db_connection(db_url):
    conn = sqlite3.connect(db_url)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_url):
    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sessions';")
    table_exists = cursor.fetchone()

    if not table_exists:
        print("initing sessions")
        cursor.execute('''
            CREATE TABLE sessions (
                id TEXT PRIMARY KEY,
                initial_requirements TEXT NOT NULL,
                web_pages TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_processing BOOL NOT NULL
            );
        ''')
        conn.commit()


class SQLiteClient(DBClient):
    @classmethod
    def get_client(cls, db_url):
        if 'db_client' not in g:
            conn = get_db_connection(db_url)
            g.db_client = cls(conn)
        return g.db_client

    def __init__(self, conn):
        self.conn = conn

    def save_session(self, session: Session):
        self.conn.execute(
            '''
                INSERT INTO sessions (id, initial_requirements, web_pages, created_at, updated_at, is_processing)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id)
                DO UPDATE SET web_pages=excluded.web_pages, updated_at=updated_at, is_processing=is_processing;
            ''', 
            (
                session._id, 
                session.initial_requirements, 
                json.dumps([wp.to_dict() for wp in session.web_pages]),
                session.created_at, 
                datetime.utcnow(),
                session.is_processing,
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
                "is_processing": session_data["is_processing"],
            })
        return None


get_client = SQLiteClient.get_client
