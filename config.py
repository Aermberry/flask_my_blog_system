import os
from datetime import timedelta

from dotenv import dotenv_values

# host = os.environ.get("APP_HOST", "0.0.0.0")
# port = os.environ.get("FLASK_DEVELOPMENT_PORT", 8000)
# debug = os.environ.get("FLASK_DEBUG", False)

# if __name__ == '__main__':
#     app.run(host=host, port=port, debug=debug)

env_config = dotenv_values("./env/.env")
database_config = dotenv_values("./env/.env.db_connection")

app_config = {
    "host": env_config.get("APP_HOST", "0.0.0.0"),
    "port": env_config.get("FLASK_DEVELOPMENT_PORT", 8000),
    "debug": env_config.get("FLASK_DEBUG", True)
}

SQLALCHEMY_DATABASE_URI = database_config.get("SQLALCHEMY_DATABASE_URI")

UPLOAD_FOLDER = env_config.get("UPLOAD_FOLDER")

JWT_SECRET_KEY = env_config.get("JWT_SECRET_KEY")
JWT_TOKEN_LOCATION = ["headers"]
JWT_IDENTITY_CLAIM = "user_id"  # default == sub
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
