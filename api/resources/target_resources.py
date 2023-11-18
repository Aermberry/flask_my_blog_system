from typing import Optional

from flask import jsonify, request
from flask_restful import Resource
from sqlalchemy import desc

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
        schema: TargetSchema = TargetSchema()

        return jsonify(schema.dump(target))

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
        title_filter = request.args.get("title")
        sorts = request.args.get("sort")

        targets_query = TargetDO.query

        if title_filter:
            # ilike() 是 SQLAlchemy 的方法，用于执行大小写不敏感的模糊匹配。
            # in_() 是 SQLAlchemy 的方法，用于执行包含操作。它允许你检查某个值是否包含在给定列表中。
            #  users_query.filter(User.email.in_(email_filter.split(",")))
            # email_filter.split(",") 是将 email_filter 字符串按逗号分隔的操作。它将逗号分隔的邮箱地址字符串拆分为一个邮箱地址列表。
            # "sos222@gamil.com,sao2023@gmail.com"->["sos222@gamil.com","sao2023@gmail.com"]
            # == 是 SQLAlchemy 中的比较操作符，表示等于。
            # users_query = users_query.filter(User.age == age_filter)
            targets_query = targets_query.filter(TargetDO.title.ilike(f"%{title_filter}%"))

        if sorts:
            for sort in sorts.split(","):
                # `descending = sort[0] == "-"` 这行代码用于判断排序条件是否为降序。在 HTTP 请求参数中，排序条件通常以字符串形式传递，如果排序条件以 "-"
                # 开头，表示降序排序。所以，这行代码检查排序条件的第一个字符是否是 "-"，如果是，就将 `descending` 设为 `True`，表示降序排序；否则，设为 `False`，表示升序排序。
                # 例如，如果排序条件参数 `sort` 的值为 `"-age"`，那么 `descending` 将被设置为 `True`，表示按年龄降序排序。如果 `sort` 的值为 `"name"`，那么
                # `descending` 将被设置为 `False`，表示按姓名升序排序。
                #
                # 这是一种常见的约定，用来在排序条件中指示排序方向。如果要降序排序，前面加一个 "-"，如果不带 "-"，默认为升序排序。
                descending = sort[0] == "-"
                if descending:
                    # 这行代码用于获取排序字段的属性。在这里，`sort` 是排序条件的字符串，通常是从 HTTP 请求参数中获取的。通常，排序条件的字符串以 "-" 开头表示降序，然后后面跟着字段名，例如
                    # `-age` 表示按年龄降序排序，`name` 表示按姓名升序排序。 这行代码的作用是将 `sort` 字符串中的 "-" 去除，然后获取与字段名对应的 SQLAlchemy 模型类
                    # `User` 中的属性。这样，`field` 就包含了要用于排序的字段的属性。
                    #
                    # 例如，如果 `sort` 为 `"-age"`，那么 `sort[1:]` 就是 `"age"`，然后 `getattr(User, sort[1:])` 就会获取 `User` 模型中名为
                    # `age` 的属性，用于排序。
                    #
                    # 总结起来，这行代码是将排序条件中的字段名提取出来，然后获取与之对应的 SQLAlchemy 模型属性，以便在排序查询中使用。
                    field = getattr(TargetDO, sort[1:])
                    targets_query = targets_query.order_by(desc(field))
                else:
                    field = getattr(TargetDO, sort)
                    targets_query = targets_query.order_by(field)

        target_list = targets_query.all()
        # target_list = TargetDO.query.all()
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
