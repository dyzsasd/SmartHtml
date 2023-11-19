from datetime import datetime
from typing import List
import uuid


class WebPage(object):
    @classmethod
    def create_new_web_page(cls, html, css, javascript):
        return cls(str(uuid.uuid4()),  html, css, javascript, datetime.utcnow())

    def __init__(self, _id: str, html: str, css: str, javascript: str, created_at: datetime):
        self._id = _id
        self.html = html
        self.css = css
        self.javascript = javascript
        self.created_at = created_at

    def to_dict(self):
        """Serialize the object to dict."""
        return {
            "id": self._id,
            "html": self.html,
            "css": self.css,
            "javascript": self.javascript,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, dict):
        return cls(
            dict['id'],
            dict["html"],
            dict["css"],
            dict["javascript"],
            datetime.fromisoformat(dict["created_at"]),
        )