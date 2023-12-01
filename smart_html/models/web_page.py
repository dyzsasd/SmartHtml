from datetime import datetime
from typing import List
import uuid


class WebPage(object):
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

    def add_code(self, html, css, javascript):
        self.html = html
        self.css = css
        self.javascript = javascript
        self.updated_at = datetime.utcnow()

    def in_processing(self):
        return self.html is None

    def to_dict(self):
        """Serialize the object to dict."""
        return {
            "id": self._id,
            "html": self.html,
            "css": self.css,
            "javascript": self.javascript,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, dict):
        obj = cls(dict['id'])
        obj.created_at = datetime.fromisoformat(dict["created_at"])
        obj.updated_at = datetime.fromisoformat(dict["updated_at"])
        obj.html = dict.get("html")
        obj.css = dict.get("css")
        obj.javascript = dict.get("javascript")
        return obj
