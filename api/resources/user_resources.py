from flask_restful import Resource
from api.schemas.user_schema import RoleSchema
from constants import ONE_WEEK
from models.user_do import Role
from packages.cache import cache


class UserResources(Resource):

    def get(self, target_id):
        pass


class RoleList(Resource):
    @cache.cached(ONE_WEEK, key_prefix="user_roles")
    def get(self):
        roles = Role.query.all()
        schema = RoleSchema(many=True)
        return {
            "results": schema.dump(roles)
        }
