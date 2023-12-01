from flask import Blueprint, jsonify, request, current_app, url_for

from ..models.session import Session
from ..models.web_page import WebPage

api = Blueprint('api', __name__)


def _webpage_to_api_response(session_id: str, wp: WebPage, host):
    wp_dict = wp.to_dict()
    wp_dict['url'] = host + url_for("demo.serve_html", session_id=session_id, webpage_id=wp._id)
    wp_dict['in_processing'] = wp.in_processing()
    return wp_dict

def _session_to_api_response(session: Session, host):
    session_dict = session.to_dict()
    session_dict["web_pages"] = [
        _webpage_to_api_response(session._id, wp, host=host)
        for wp in session.web_pages
    ]
    return session_dict


@api.route('/session', methods=['POST'])
def create_session():
    """Create session and generate the first version of the webpage"""
    data = request.json
    session = Session.create_new_session(data["requirements"])
    web_page = WebPage.create_new_web_page()
    
    messages = [current_app.message_type.user_message(session.initial_requirements)]
    result = current_app.engine.generate_code(messages)

    web_page.add_code(result.html(), result.css(), result.javascript())
    session.add_web_page(web_page)
    current_app.get_db_client().save_session(session)

    return jsonify(_session_to_api_response(session, host=current_app.config.get("WEB_APP_HOST")))


@api.route('/session/async', methods=['POST'])
def create_session_async():
    """Create session and generate the first version of the webpage"""
    data = request.json
    session = Session.create_new_session(data["requirements"])
    web_page = WebPage.create_new_web_page()
    session.add_web_page(web_page)

    get_db_func = current_app.get_db_client
    engine = current_app.engine
    message_type = current_app.message_type

    get_db_func().save_session(session)

    def generate_web_page():
        messages = [message_type.user_message(session.initial_requirements)]
        result = engine.generate_code(messages)

        web_page.add_code(result.html(), result.css(), result.javascript())
        get_db_func().save_session(session)

    current_app.task_runner.submit_task(generate_web_page)

    return jsonify(_session_to_api_response(session, host=current_app.config.get("WEB_APP_HOST")))


@api.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    session = current_app.get_db_client().load_from_db(session_id=session_id)

    return jsonify(_session_to_api_response(session, host=current_app.config.get("WEB_APP_HOST")))


@api.route('/session/<session_id>/webpage/<webpage_id>', methods=['GET'])
def get_webpage(session_id, webpage_id):
    session = current_app.get_db_client().load_from_db(session_id=session_id)
    if session is None:
        return 'session not found', 404

    for wp in session.web_pages:
        if wp._id == webpage_id:
            return jsonify(_webpage_to_api_response(session_id, wp, host=current_app.config.get("WEB_APP_HOST")))

    return 'webpage not found', 404
