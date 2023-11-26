from marshmallow import validate, validates_schema, ValidationError
from marshmallow.fields import String
from models.user_do import UserDo, Role
from packages.serializable_util import serializable


class UserSchema(serializable.SQLAlchemyAutoSchema):
    name = String(required=True, validate=[validate.Length(min=3)], error_messages={
        "required": "The name is required",
        "invalid": "The name is invalid and needs to be a string",
    })
    email = String(required=True, validate=[validate.Email()])

    @validates_schema
    def validate_email(self, data, **kwargs):
        email = data.get("email")

        if UserDo.query.filter_by(email=email).count():
            raise ValidationError(f"Email {email} already exists.")

    class Meta:
        model = UserDo
        load_instance = True
        exclude = ["id", "_password"]


class UserCreateSchema(UserSchema):
    password = String(
        required=True,
        validate=[validate.Regexp(r"^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,}$",
                                  error="The password need to be at least 8 characters long, and have at least 1 of each of the following: lowercase letter, uppercase letter, special character, number."
                                  )],
    )


class RoleSchema(serializable.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
