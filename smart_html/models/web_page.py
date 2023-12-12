from datetime import datetime
import uuid

from smart_html.utils.mixin import JsonMixin
from .comment import WebPageComment


class WebPage(JsonMixin):
    @classmethod
    def create_new_web_page(cls):
        return cls(str(uuid.uuid4()))

    def __init__(self, _id: str):
        self._id = _id
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        self.html = None
        self.css = None
        self.javascript = None
        self.comments = None

    def add_code(self, html, css, javascript):
        self.html = html
        self.css = css
        self.javascript = javascript
        self.updated_at = datetime.utcnow()

    def add_comments(self, comments: WebPageComment):
        self.comments = comments

    def in_processing(self):
        return self.html is None
