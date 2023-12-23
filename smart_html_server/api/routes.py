from flask import Blueprint, jsonify, request, current_app, url_for

from ..models.comment import WebPageComment, GlobalComment, ElementComment
from ..models.session import Session
from ..models.web_page import WebPage

api = Blueprint('api', __name__)


def _webpage_to_api_response(session_id: str, wp: WebPage, host):
    wp_dict = wp.to_json()
    wp_dict['url'] = host + \
        url_for("demo.serve_html", session_id=session_id, webpage_id=wp._id)
    wp_dict['in_processing'] = wp.in_processing()
    return wp_dict


def _session_to_api_response(session: Session, host):
    session_dict = session.to_json()
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

    messages = [
        current_app.message_type.user_message(session.initial_requirements)
    ]
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


@api.route('/session/<session_id>/webpage/<webpage_id>/comments', methods=['PUT'])
def add_comments(session_id, webpage_id):
    data = request.json

    global_comment = GlobalComment(data['global'])
    element_comments = [
        ElementComment(_id, value)
        for _id, value in data['element_comments'].items()
    ]

    comments = WebPageComment(global_comment, element_comments)

    session = current_app.get_db_client().load_from_db(session_id=session_id)
    if session is None:
        return 'session not found', 404

    for wp in session.web_pages:
        if wp._id == webpage_id:
            wp.comments = comments
            current_app.get_db_client().save_session(session)
            return jsonify(_webpage_to_api_response(session_id, wp, host=current_app.config.get("WEB_APP_HOST")))

    return 'webpage not found', 404


@api.route("/session/<session_id>/webpage/<webpage_id>/update", methods=['PUT'])
def update_webpage(session_id, webpage_id):
    session = current_app.get_db_client().load_from_db(session_id=session_id)
    if session is None:
        return 'session not found', 404

    current_webpage = None
    generated_webpage = None
    for wp in session.web_pages:
        if wp._id == webpage_id:
            current_webpage = wp
        if wp.parent == webpage_id:
            generated_webpage = wp

    if current_webpage is None:
        return 'webpage not found', 404

    if generated_webpage is not None:
        jsonify(_webpage_to_api_response(session_id, generated_webpage, host=current_app.config.get("WEB_APP_HOST")))

    if current_webpage.comments is None:
        return 'no comments found for the webpage, cannot generate new version', 406

    generated_webpage = WebPage.create_new_web_page()
    generated_webpage.parent = current_webpage._id
    session.add_web_page(generated_webpage)

    get_db_func = current_app.get_db_client
    engine = current_app.engine
    message_type = current_app.message_type

    get_db_func().save_session(session)

    def generate_web_page():
        prompt = _update_prompt(session, web_page=current_webpage)
        messages = [message_type.user_message(prompt)]
        result = engine.generate_code(messages)

        generated_webpage.add_code(
            result.html(), result.css(), result.javascript())

        get_db_func().save_session(session)

    current_app.task_runner.submit_task(generate_web_page)
    return jsonify(_webpage_to_api_response(session_id, generated_webpage, host=current_app.config.get("WEB_APP_HOST")))


def _update_prompt(session: Session, web_page: WebPage):
    comments = web_page.comments

    element_feedback = '\n'.join(
        [f"node id={e._id}: {e.text}" for e in comments.element_comments])
    global_feedback = comments.global_comment.text

    prompt = f"""
    the user's initial requirements is:
    {session.initial_requirements}
    a previous version of the code has been generated:
    html:
    {web_page.html or ""}
    css:
    {web_page.css or ""}
    javascript:
    {web_page.javascript or ""}
    Here is user's feedback on entire webpage
    {global_feedback}
    Here is user's feedbacks on specific nodes of html
    {element_feedback}
    Please create a new web page based on the user's suggestions, and provide only the complete HTML, CSS, and JavaScript code.
    """

    return prompt
