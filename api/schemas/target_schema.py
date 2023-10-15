from marshmallow import validate, validates_schema, ValidationError
from marshmallow.fields import String
from models.target_do import TargetDO
from packages.serializable_util import serializable


class TargetSchema(serializable.SQLAlchemyAutoSchema):
    title = String(required=True, validate=[validate.Length(min=3)], error_messages={
        "required": "The title is required",
        "invalid": "The title and needs to be a string"
    })

    email = String(required=True, validate=[validate.Email()])

    @validates_schema()
    def validate_email(self, data, **kwargs):
        email = data.get("email")

        if TargetDO.query.filter_by(email=email).count:
            raise ValidationError(message={"email": f"Email{email} already exists."})

    class Meta:
        model = TargetDO
        load_instance = True
        exclude = ["id"]
