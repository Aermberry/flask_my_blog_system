from flask import Blueprint
from flask_restful import Api
from api.resources.target_resources import TargetList, Target

bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(bp, errors=bp.errorhandler)

api.add_resource(TargetList, '/targets')
api.add_resource(Target, '/targets/<int:target_id>')
