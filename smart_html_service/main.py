import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template

from smart_html_service.api.routes import api
from smart_html_service.demo.routes import demo
from smart_html_service.core.db import init_db
from smart_html_service.core.engine import init_engine
from smart_html_service.core.runner import init_runner
from smart_html_service.config import Config


app = Flask(__name__)
app.config.from_object(Config)

init_db(app)
init_engine(app)
init_runner(app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(demo, url_prefix='/demo')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')


if __name__ == '__main__':
    app.run(debug=True)

