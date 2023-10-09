from flask_restful import Resource, abort
from flask import jsonify, request
from targets import targets


class Target(Resource):
    @staticmethod
    def get_target_by_id(target_list, target_id):
        return next((target for target in target_list if target['id'] == target_id), None);

    def get(self, target_id):
        target = self.get_target_by_id(target_list=targets, target_id=target_id)
        return jsonify(target)

    def delete(self, target_id):
        target = None

        for index, target in enumerate(targets):
            if target.get('id') == target_id:
                target = target
                # targets.pop(index)
                print(index)

        if target is None:
            abort(404)

        return jsonify({"message": "delete successful", "target": target})

    def put(self, target_id):
        data = request.json

        target = None
        for i, u in enumerate(targets):
            if u.get("id") == target_id:
                targets[i] = {**u, **data}
                target = targets[i]

        if target is None:
            abort(404)

        return {"msg": "target updated", "user": target}

    def patch(self, target_id):
        data = request.json

        target = None
        for i, u in enumerate(targets):
            if u.get("id") == target_id:
                target = targets[i]
                target.update(data)

        if target is None:
            abort(404)

        return {"msg": "target modify", "user": target}


class TargetList(Resource):
    def get(self):
        return jsonify(targets)

    def post(self):
        target = request.json
        target_id = targets[-1].get('id')
        target = {
            'id': target_id + 1,
            **target
        }

        targets.append(target)

        return jsonify({"message": "create ok", "target": target})
