from sqlalchemy import Column

from packages.database_connecter import db


class TokenBlockList(db.Model):
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    jti = Column(db.String(36), nullable=False, unique=True)
    token_type = Column(db.String(10), nullable=False)
    # users是表名
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    revoked_at = db.Column(db.DateTime)
    expires = db.Column(db.DateTime, nullable=False)

    # 单向关联
    # 创建一个user属性 单向关联到UserDo表，即可以通过user访问UserDo表，而UserDo表无法访问TokenBlocklist表
    # UserDo是类型名字
    user = db.relationship("UserDo")
