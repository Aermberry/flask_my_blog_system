from importlib.resources import Resource

from flask import jsonify

from api.schemas.user_schema import UserSchema
from models.user_do import UserDo


class UserResources(Resource):

    def get(self, target_id):
        target=""
        schema: UserSchema = UserSchema()

        return jsonify(schema.dump(target))
