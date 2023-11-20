from sqlalchemy import text
from app import db, app

sql = open("target.sql", "r", encoding="utf-8")
statement = sql.read()

with app.app_context():
    db.session.execute(text(statement))
    db.session.commit()
