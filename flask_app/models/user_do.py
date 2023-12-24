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

    # roles 是 UserDo 模型中定义的关系属性，表示一个用户可以关联多个角色。
    # back_populates 参数用于指定反向关系属性，确保两个模型类之间的关联在添加、删除对象时能够同步更新
    # 这里的back_populates="users" 是关联到Role的users属性
    # secondary="user_roles" 表示 UserDo 模型与 Role 模型之间的多对多关系是通过名为 user_roles 的中间表来实现的
    # 多对多关系需要使用一个中间表来保存两个模型之间的关联信息。这个中间表在数据库中是一个独立的表，它包含两个外键，分别指向参与关系的两个模型。
    roles = db.relationship("Role", secondary="user_roles", back_populates="users")

    # 这段 SQLAlchemy 代码对应的 SQL 查询如下：
    #
    # ```sql
    # SELECT COUNT(*) AS count_1
    # FROM roles
    # JOIN user_roles ON roles.id = user_roles.role_id
    # JOIN users ON users.id = user_roles.user_id
    # WHERE users.id = :param_1 AND roles.slug = :slug_1
    # ```
    #
    # 这个 SQL 查询执行了以下操作：
    #
    # 1. 使用 `JOIN` 连接了 `roles` 表和 `user_roles` 表，条件是 `roles.id = user_roles.role_id`。
    # 2. 再次使用 `JOIN` 连接了 `users` 表和 `user_roles` 表，条件是 `users.id = user_roles.user_id`。
    # 3. 使用 `WHERE` 子句筛选了满足条件 `users.id = :param_1` 和 `roles.slug = :slug_1` 的记录。
    # 4. 使用 `COUNT(*)` 计算符合条件的记录数量。
    #
    # 这个查询的目的是检查某个用户（通过 `users.id = :param_1`）是否拥有特定的角色（通过 `roles.slug = :slug_1`）。
    # 最终的结果是一个包含满足条件的记录数量的整数值。如果这个数量等于 1，则返回 `True`，表示用户具有该角色；否则返回 `False`，表示用户没有该角色。
    #
    #
    def has_role(self, role):
        return bool(
            Role.query
            .join(Role.users)
            .filter(UserDo.id == self.id)
            .filter(Role.slug == role)
            .count() == 1
        )

    # join方法 precisely 将Role表、UserDo表和user_roles表进行连结:
    #
    # - Role模型定义了关系属性users,指向UserDo模型,通过user_roles表连接。
    #
    # - 在has_role方法中,使用Role作为基表:
    #
    #   ````python
    #   Role.query
    #   ```
    #
    # - 然后调用join方法,传入关系属性users:
    #
    #   ````python
    #   .join(Role.users)
    #   ```
    #
    # - 这里Role.users实际指向的是user_roles表,因为关系属性指定了使用user_roles作为中间表。
    #
    # - 所以这行语句实现的效果就是:
    #
    #   将Role表左外连接到user_roles表上。
    #
    #   将user_roles表左外连接到UserDo表上。
    #
    # - 最终形成一个Role表、UserDo表和user_roles表的三表联接视图。
    #
    # 所以你可以理解为:
    #
    # join方法通过模型定义的关系属性,自动为我们构建了Role表、UserDo表和user_roles表三表的联结查询,同时添加其他过滤条件,就可以完成表关系的查询了。
    #
    # 把三张表关联起来查询,这就是join方法的核心作用。

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(36), nullable=False)
    slug = db.Column(db.String(36), nullable=False, unique=True)

    # users 是 Role 模型中定义的关系属性，表示一个角色可以关联多个用户。
    # back_populates 参数用于指定反向关系属性，确保两个模型类之间的关联在添加、删除对象时能够同步更新
    # 这里的back_populates="roles" 是关联到UserDo的roles属性
    # secondary 参数用于指定多对多关系的中间表（也称为关联表）。
    # secondary="user_roles" 表示 UserDo 模型与 Role 模型之间的多对多关系是通过名为 user_roles 的中间表来实现的
    # 多对多关系需要使用一个中间表来保存两个模型之间的关联信息。这个中间表在数据库中是一个独立的表，它包含两个外键，分别指向参与关系的两个模型。
    users = db.relationship("UserDo", secondary="user_roles", back_populates="roles")


# user_roles 表包含了 user_id 和 role_id 两个列，分别与 UserDo 模型和 Role 模型的主键相对应。
# 通过使用 secondary 参数，你告诉 SQLAlchemy 使用 user_roles 表来管理 UserDo 模型和 Role 模型之间的多对多关系。
# 这使得在处理多对多关系时，你可以通过 UserDo.roles 和 Role.users 这两个属性来访问彼此之间的关系。
class UserRole(db.Model):
    __tablename__ = "user_roles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), primary_key=True)
