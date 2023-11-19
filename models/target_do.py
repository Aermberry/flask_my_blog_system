from packages.database_connecter import db


# @dataclass
class TargetDO(db.Model):
    # id: int
    # title: str
    # image_url: str
    # description: str
    # summary: str
    # key_point_list: dict

    __tablename__ = "targets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=False)
    key_point_list = db.Column(db.JSON, nullable=True)
    user_name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False)
