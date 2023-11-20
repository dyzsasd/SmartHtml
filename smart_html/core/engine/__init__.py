from flask import Flask

from .openai import OpenAIEngine, OpenAIMessage

def init_engine(app: Flask):
    app.engine = OpenAIEngine(app.config["ENGINE_OPENAI_APP_KEY"])
    app.message_type = OpenAIMessage
