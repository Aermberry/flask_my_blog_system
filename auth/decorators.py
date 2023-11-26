from functools import wraps

from flask import make_response
from flask_jwt_extended import get_current_user


def auth_role(role):
    def wrapper(fn):
        @wraps(fn)
        # *args通过元组收集参数,**kwargs通过字典收集参数,都可以实现不定长参数的功能。
        def decorator(*args, **kwargs):
            current_user = get_current_user()
            # 这行代码是一个判断变量类型的简写方法:
            #
            # role是一个参数,它可能是列表类型,也可能是单个值类型。
            #
            # 使用isinstance判断role是否为list:
            #
            # - 如果role是list类型,直接赋值给roles变量:
            #
            # roles = role
            #
            # - 如果role不是list类型,将它包装成一个单元素列表后再赋值给roles变量:
            #
            # roles = [role]
            #
            # 这样保证了roles变量一定是一个列表:
            #
            # - 如果role原本是列表,roles将直接使用这个列表
            # - 如果role是单值,roles将它包装成一个单元素列表
            #
            # 这比正常情况下要更复杂一些:
            #
            # ```python
            # if isinstance(role, list):
            #   roles = role
            # else:
            #   roles = [role]
            # ```
            #
            # 用一条语句实现了同样的逻辑,代码更简练。
            #
            # 所以这个一行代码的目的是:
            #
            # - 根据role的类型判断是否需要对它进行列表转化
            # - 保证roles一定是列表,方便后续使用
            #
            # 简化了类型判断的同时实现变量标准化。
            roles = role if isinstance(role, list) else [role]

            # all()函数,判断循环的所有结果是否一致
            # 判断是否都满足所有的权限，如果有一个权限缺失，都失败
            if all(not current_user.has_role(r) for r in roles):
                return make_response({"msg": f"Missing any of roles {','.join(roles)}"}, 403)
            return fn(*args, **kwargs)

        return decorator

    return wrapper
