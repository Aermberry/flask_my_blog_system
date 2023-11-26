from flask import Blueprint, request, jsonify
from flask_jwt_extended import (create_access_token,
                                jwt_required,
                                get_jwt_identity,
                                create_refresh_token,
                                get_jwt,
                                get_current_user)

from marshmallow import ValidationError

from api.schemas.user_schema import UserCreateSchema, UserSchema
from flask import current_app as app
from auth.helpers import add_token_to_database, revoke_token, is_token_revoke

from models.user_do import UserDo

from packages.authentication import jwt
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

    add_token_to_database(access_token)
    add_token_to_database(refresh_token)

    return {"access_token": access_token, "refresh_token": refresh_token}


@auth_bluerprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)

    add_token_to_database(access_token)

    return {"access_token": access_token}, 200


@auth_bluerprint.route("/revoke_access", methods=["DELETE"])
@jwt_required()
def revoke_access_token():
    jti = get_jwt()["jti"]
    user_id = get_jwt_identity()
    revoke_token(jti, user_id)
    return jsonify({"message": "token revoked"}), 200


@auth_bluerprint.route("/revoke_refresh", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    jti = get_jwt()["jti"]
    user_id = get_jwt_identity()
    revoke_token(jti, user_id)
    return jsonify({"message": "Refresh token revoked"}), 200


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    try:
        return is_token_revoke(jwt_payload)
    except Exception:
        return True


# 通过token获取当前的用户对象
# 通过实现 user_lookup_loader 从 JWT 中加载对象，可以使用get_current_user()获取当前用户对象
@jwt.user_lookup_loader
def load_user(jwt_headers, jwt_payload):
    user_id = jwt_payload[app.config.get("JWT_IDENTITY_CLAIM")]
    print(user_id)
    return UserDo.query.get(user_id)


@auth_bluerprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
