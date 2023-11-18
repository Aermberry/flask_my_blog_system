from sqlalchemy.ext.hybrid import hybrid_property

from packages.database_connecter import db
from packages.password_hash import pwd_context


class UserDo(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.Integer)
    _password = db.column("password", db.String(255), nullable=False)

    # 自定义混合属性
    @hybrid_property
    def password(self):
        return self._password

    # 为自定义的混合属性password，添加setter方法
    # 对传入的密码值进行哈希处理，然后将处理后的值存储在底层的 _password 字段中
    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)
