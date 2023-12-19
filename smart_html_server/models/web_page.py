from datetime import datetime
import uuid

from smart_html_server.utils.mixin import JsonMixin
from .comment import WebPageComment


class WebPage(JsonMixin):
    @classmethod
    def create_new_web_page(cls):
        return cls(str(uuid.uuid4()))

    def __init__(self, _id: str, created_at=datetime.utcnow(), updated_at=datetime.utcnow(), html=None, css=None, javascript=None, comments=None, parent=None):
        self._id = _id
        self.created_at = created_at
        self.updated_at = updated_at
        self.html = html
        self.css = css
        self.javascript = javascript
        self.comments = comments
        self.parent = parent

    def add_code(self, html, css, javascript):
        self.html = html
        self.css = css
        self.javascript = javascript
        self.updated_at = datetime.utcnow()

    def add_comments(self, comments: WebPageComment):
        self.comments = comments

    def in_processing(self):
        return self.html is None
