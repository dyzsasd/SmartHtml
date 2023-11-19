from flask import Flask

from smart_html.api.routes import api
from smart_html.core.db import sqlite as db
from smart_html.config import config


app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api')
db.init_db(config["sqlite"]["url"])

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)

