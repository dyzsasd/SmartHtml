from flask import Blueprint, jsonify, request, current_app

from ..models.session import Session
from ..models.web_page import WebPage

api = Blueprint('api', __name__)
@api.route('/session', methods=['POST'])
def create_session():
    """Create session and generate the first version of the webpage"""
    data = request.json
    session = Session.create_new_session(data["requirements"])
    
    messages = [current_app.message_type.user_message(session.initial_requirements)]
    result = current_app.engine.generate_code(messages)
    
    web_page = WebPage.create_new_web_page(result.html(), result.css(), result.javascript())
    session.add_web_page(web_page)
    current_app.get_db_client().save_session(session)
    
    return jsonify(session.to_dict())


@api.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    session = current_app.get_db_client().load_from_db(session_id=session_id)
    
    return jsonify(session.to_dict())
