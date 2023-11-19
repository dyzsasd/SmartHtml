from datetime import datetime
from typing import List
import uuid

from .web_page import WebPage

class Session(object):
    @classmethod
    def create_new_session(cls, initial_requierments):
        return cls(str(uuid.uuid4()), initial_requierments, list(), datetime.utcnow())

    def __init__(self, _id: str, initial_requirements: str, web_pages: List[WebPage], created_at: datetime):
        self._id = _id
        self.initial_requirements = initial_requirements
        self.web_pages = web_pages
        self.created_at = created_at

    def add_web_page(self, web_page: WebPage):
        self.web_pages.append(web_page)

    def to_dict(self):
        """Serialize the object to dict."""
        web_page_jsons = [
            {
                **web_page.to_dict(),
                **{"url": "/".join(["", "demo", "session", self._id, "webpage", web_page._id])}
            }
            for web_page in self.web_pages
        ]
        return {
            "id": self._id,
            "initial_requirements": self.initial_requirements,
            "web_pages": web_page_jsons,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, dict):
        return cls(
            dict['id'],
            dict["initial_requirements"],
            [WebPage.from_dict(web_page_dict) for web_page_dict in dict.get('web_pages', [])],
            datetime.fromisoformat(dict["created_at"]),
        )