from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from marshmallow import ValidationError

from api.schemas.user_schema import UserCreateSchema, UserSchema
from models.user_do import UserDo
from packages.database_connecter import db
from packages.password_hash import pwd_context

auth_bluerprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bluerprint.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return {"msg": "Missing JSON in request "}

    schema = UserCreateSchema()
    user = schema.load(request.json)

    db.session.add(user)
    db.session.commit()

    schema = UserSchema()

    return {"msg": "User created", "user": schema.dump(user)}


@auth_bluerprint.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return {"msg": "Missing JSON in request "}
    email = request.json.get("email")
    password = request.json.get("password")
    if not email or not password:
        return {"msg": f"Missing password or email"}, 400

    user = UserDo.query.filter_by(email=email).first()

    if not user or not pwd_context.verify(password, user.password):
        return {"msg": "Missing password or email"}, 400

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return {"access_token": access_token, "refresh_token": refresh_token}


@auth_bluerprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return {"access_token": access_token}, 200


@auth_bluerprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
