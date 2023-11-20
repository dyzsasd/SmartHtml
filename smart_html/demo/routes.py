from flask import Blueprint, Response

from ..models.web_page import WebPage
from ..core.db import sqlite as db
from ..config import config

demo = Blueprint('demo', __name__)
db_url = config["db"]["url"]


def find_web_page(session_id: str, webpage_id: str) -> WebPage:
    session = db.get_client(db_url).load_from_db(session_id=session_id)
    if session is None:
        return None

    for wp in session.web_pages:
        if wp._id == webpage_id:
            return wp
    return None


@demo.route('/session/<session_id>/webpage/<webpage_id>/page.html')
def serve_html(session_id, webpage_id):
    web_page = find_web_page(session_id, webpage_id)
    if web_page:
        return Response(web_page.html, mimetype='text/html')
    return 'Demo not found', 404

@demo.route('/session/<session_id>/webpage/<webpage_id>/scripts.js')
def serve_javascript(session_id, webpage_id):
    web_page = find_web_page(session_id, webpage_id)
    if web_page:
        return Response(web_page.javascript, mimetype='application/javascript')
    return 'scripts.js not found', 404

@demo.route('/session/<session_id>/webpage/<webpage_id>/styles.css')
def serve_css(session_id, webpage_id):
    web_page = find_web_page(session_id, webpage_id)
    if web_page:
        return Response(web_page.css, mimetype='text/css')
    return 'stypes.css not found', 404
