import os

from sqlalchemy import text
from app import db, app

result = os.scandir("seed")

# sql = open("seed/target.sql", "r", encoding="utf-8")

with app.app_context():
    for item in result:
        if item.is_file:
            sql = open(item.path, "r", encoding="utf-8")
            statement = sql.read()
            db.session.execute(text(statement))

    db.session.commit()
