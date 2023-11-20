from ...models.session import Session

class DBClient(object):
    def save_session(self, session: Session):
        raise NotImplementedError("save_session not implemented")

    def load_from_db(self, session_id) -> Session:
        raise NotImplementedError("load_from_db not implemented")
