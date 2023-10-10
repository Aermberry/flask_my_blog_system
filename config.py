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
