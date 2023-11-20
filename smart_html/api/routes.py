from flask import Blueprint, jsonify, request

from ..models.session import Session
from ..models.web_page import WebPage
from ..core.db import sqlite as db
from ..core.engine import openai as engine
from ..config import config

api = Blueprint('api', __name__)
engine_instance = engine.engine_cls(config["engine"]["app_key"])
db_url = config["db"]["url"]


@api.route('/session', methods=['POST'])
def create_session():
    """Create session and generate the first version of the webpage"""
    data = request.json
    session = Session.create_new_session(data["requirements"])
    
    messages = [engine.message_type.user_message(session.initial_requirements)]
    result = engine_instance.generate_code(messages)
    
    web_page = WebPage.create_new_web_page(result.html(), result.css(), result.javascript())
    session.add_web_page(web_page)
    db.get_client(db_url).save_session(session)
    
    return jsonify(session.to_dict())


@api.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    session = db.get_client(db_url).load_from_db(session_id=session_id)
    
    return jsonify(session.to_dict())