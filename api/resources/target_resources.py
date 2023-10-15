from typing import Optional

from flask import jsonify, request
from flask_restful import Resource

from api.schemas.target_schema import TargetSchema
from models.target_do import TargetDO
from packages.database_connecter import db


class TargetResource(Resource):
    @staticmethod
    def get_target_by_id(target_id) -> Optional[TargetDO]:
        # return next((target for target in target_list if target['id'] == target_id), None)

        return TargetDO.query.get_or_404(target_id)

    def get(self, target_id):
        target = self.get_target_by_id(target_id=target_id)
        return jsonify(target)

    def delete(self, target_id):
        # target = None

        # for index, target in enumerate(targets):
        #     if target.get('id') == target_id:
        #         target = target
        #         # targets.pop(index)
        #         print(index)
        #
        # if target is None:
        #     abort(404)
        # target = self.get_target_by_id(target_id)
        target = TargetDO.query.get_or_404(target_id)

        db.session.delete(target)
        db.session.commit()

        return jsonify({"message": "delete successful"})

    def put(self, target_id):
        data: dict = request.json

        schema: TargetSchema = TargetSchema()
        target = TargetDO.query.get_or_404(target_id)
        target_do: TargetDO = schema.load(data, instance=target)

        # target = None

        # target = self.get_target_by_id(target_id)
        #
        # target.title = data["title"]
        # target.image_url = data["image_url"]
        # target.description = data["description"]
        # target.summary = data["summary"]
        # target.key_point_list = data["key_point_list"]

        db.session.add(target_do)
        db.session.commit()

        # for i, u in enumerate(targets):
        #     if u.get("id") == target_id:
        #         targets[i] = {**u, **data}
        #         target = targets[i]
        #
        # if target is None:
        #     abort(404)

        return {"msg": "target updated", "data": schema.dump(target)}

    def patch(self, target_id):
        data: dict = request.json

        schema = TargetSchema(partial=True)
        target = TargetDO.query.get_or_404(target_id)

        target_do = schema.load(data, instance=target)

        # target = None
        # for i, u in enumerate(targets):
        #     if u.get("id") == target_id:
        #         target = targets[i]
        #         target.update(data)
        #
        # if target is None:
        #     abort(404)

        # target: TargetDO = self.get_target_by_id(target_id)

        # modify

        # for key, value in data.items():
        #     setattr(target, key, value)
        db.session.add(target_do)
        db.session.commit()

        return jsonify({"msg": "target modify", "user": schema.dump(target_do)})


class TargetListResource(Resource):
    def get(self):
        target_list = TargetDO.query.all()
        schema = TargetSchema(many=True)
        return {"data": schema.dump(target_list)}

    def post(self):
        # data = request.json

        schema = TargetSchema()
        target_do = schema.load(request.json)

        db.session.add(target_do)
        db.session.commit()

        # return jsonify({"message": target})

        # target_id = targets[-1].get('id')
        # target = {
        #     'id': target_id + 1,
        #     **target
        # }
        #
        # targets.append(target)

        # target = TargetDO(
        #     title=data.get("title"),
        #     image_url=data.get("image_url"),
        #     description=data.get("description"),
        #     summary=data.get("summary"),
        #     key_point_list=data.get("key_point_list")
        # )

        #
        # db.session.add(target)
        # db.session.commit()

        return jsonify({"message": "create ok", "target": schema.dump(target_do)})
