from flask import Flask, render_template

from smart_html_server.api.routes import api
from smart_html_server.demo.routes import demo
from smart_html_server.core.db import init_db
from smart_html_server.core.engine import init_engine
from smart_html_server.core.runner import init_runner
from smart_html_server.config import Config


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
