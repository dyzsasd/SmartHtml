from flask import Flask

from smart_html.api.routes import api
from smart_html.demo.routes import demo
from smart_html.core.db import init_db
from smart_html.config import config


app = Flask(__name__)
app.config.from_object(config)

init_db(app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(demo, url_prefix='/demo')

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)

