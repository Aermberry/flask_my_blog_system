from flask import Flask
from api.views import bp
from config import app_config
from packages.database_connecter import db
from packages.migrate_util import migrate_util
from packages.serializable_util import serializable

app = Flask(__name__)
app.register_blueprint(bp)
app.config.from_object('config')

db.init_app(app)
serializable.init_app(app)
migrate_util.init_app(app, db)

app.extensions

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(**app_config)
