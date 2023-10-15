from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from api.resources.image_resources import ImageListResources, ImageResources
from api.resources.target_resources import TargetListResource, TargetResource

bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(bp, errors=bp.errorhandler)

api.add_resource(TargetListResource, '/targets')
api.add_resource(TargetResource, '/targets/<int:target_id>')
api.add_resource(ImageListResources, '/images')
api.add_resource(ImageResources, '/images/<string:image_name>')


@bp.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
