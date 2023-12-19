from datetime import datetime
from typing import List
import uuid

from smart_html_server.utils.mixin import JsonMixin
from .web_page import WebPage


class Session(JsonMixin):
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
