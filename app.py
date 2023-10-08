import os

from dotenv import load_dotenv, dotenv_values
from flask import Flask

app = Flask(__name__)

load_dotenv()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


host = os.environ.get("APP_HOST", "0.0.0.0")
port = os.environ.get("FLASK_DEVELOPMENT_PORT", 8000)
debug = os.environ.get("FLASK_DEBUG", False)

if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug)

env_config = dotenv_values("./env/.env")

app_config = {
    "host": env_config.get("APP_HOST", "0.0.0.0"),
    "port": env_config.get("FLASK_DEVELOPMENT_PORT", 8000),
    "debug": env_config.get("FLASK_DEBUG", False)
}

if __name__ == '__main__':
    app.run(**app_config)
