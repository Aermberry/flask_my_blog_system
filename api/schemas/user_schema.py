from models.user_do import UserDo
from packages.serializable_util import serializable


class UserSchema(serializable.SQLAlchemyAutoSchema):
    class Meta:
        model = UserDo
        load_instance = True
        exclude = ["id", "_password"]
