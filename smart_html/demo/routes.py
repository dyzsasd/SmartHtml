from bs4 import BeautifulSoup
from flask import Blueprint, Response, current_app, render_template

from ..models.session import Session
from ..models.web_page import WebPage

demo = Blueprint('demo', __name__, template_folder="templates", static_folder='static')

def find_web_page(session_id: str, webpage_id: str) -> WebPage:
    session = current_app.get_db_client().load_from_db(session_id=session_id)
    if session is None:
        return None

    for wp in session.web_pages:
        if wp._id == webpage_id:
            return wp
    return None


@demo.route('/session/<session_id>/webpage/<webpage_id>/page.html')
def serve_html(session_id, webpage_id):
    web_page = find_web_page(session_id, webpage_id)

    if web_page is None:
        return 'Demo not found', 404

    if web_page.in_processing():
        return render_template("coding_hacker.html", session_id = session_id, webpage_id = webpage_id)

    if web_page:
        html_content = web_page.html
        soup = BeautifulSoup(html_content, 'html.parser')

        return Response(str(soup), mimetype='text/html')
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
