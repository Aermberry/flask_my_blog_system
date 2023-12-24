from flask import Flask

import manage
from api.views import bp
from auth.views import auth_bluerprint
from config import app_config
from packages.cache import cache
from packages.database_connecter import db
from packages.authentication import jwt
from packages.migrate_util import migrate_util
from packages.serializable_util import serializable

app = Flask(__name__)
app.register_blueprint(blueprint=bp)
app.register_blueprint(blueprint=auth_bluerprint)
app.config.from_object('config')

db.init_app(app)
migrate_util.init_app(app, db)
serializable.init_app(app)
app.cli.add_command(manage.target_cli)
jwt.init_app(app)
cache.init_app(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# if __name__ == '__main__':
#     app.run(**app_config)
