from sqlalchemy import Column
from sqlalchemy.ext.hybrid import hybrid_property

from packages.database_connecter import db
from packages.password_hash import pwd_context


class UserDo(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.Integer)
    _password = Column("password", db.String(255), nullable=False)

    # 自定义混合属性
    @hybrid_property
    def password(self):
        return self._password

    # 为自定义的混合属性password，添加setter方法
    # 对传入的密码值进行哈希处理，然后将处理后的值存储在底层的 _password 字段中
    # 在 `UserDo` 类中，`password` 并不是一个直接的数据库列（字段），而是一个混合属性（hybrid property）。
    # 混合属性是一种结合了 Python 对象属性和数据库字段的特殊属性，它允许你定义在对象层面的属性逻辑，并在数据库层面的映射。
    #
    # 让我们详细解释：
    #
    # 1. **数据库列（字段）：**
    #    - `id`, `name`, `email`, `age`, 和 `_password` 是数据库表中的实际列（字段）。
    #    这些列映射到数据库表中的相应列，并存储相应的数据类型。
    #
    # 2. **混合属性 `password`：**
    #    - `password` 是一个由 `@hybrid_property` 装饰器创建的混合属性。
    #    这种属性在对象实例中行为类似于常规属性，但它可以具有自定义的 getter 和 setter 方法。
    #    - 在这里，`password` 的 getter 方法返回底层的 `_password` 字段的值，允许你像访问普通属性一样访问密码。
    #    - `password` 的 setter 方法定义了在设置密码属性时执行的逻辑。
    #    在这里，它使用 `pwd_context.hash` 对密码进行哈希处理，然后将哈希值存储在底层的 `_password` 字段中。
    #
    # 所以，虽然 `password` 在表面上看起来像一个普通的属性，但它实际上通过混合属性的方式，
    # 将密码逻辑（哈希处理等）和数据库存储逻辑结合在一起。在使用 `UserDo` 对象时，
    # 你可以像处理其他属性一样使用 `password`，而在数据库中，它将存储在 `_password` 列中。
    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)
