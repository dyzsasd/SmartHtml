from bs4 import BeautifulSoup
from flask import Blueprint, Response, current_app

from ..models.web_page import WebPage
from ..config import config

demo = Blueprint('demo', __name__)

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
    if web_page:
        html_content = web_page.html
        soup = BeautifulSoup(html_content, 'html.parser')

        # Add feedback.js to the HTML head
        new_script_tag = soup.new_tag("script", src="/feedback.js")
        soup.head.append(new_script_tag)

        # Add an additional HTML block to the body
        new_html_block = BeautifulSoup('<div>Your additional HTML block here</div>', 'html.parser')
        soup.body.append(new_html_block)

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
