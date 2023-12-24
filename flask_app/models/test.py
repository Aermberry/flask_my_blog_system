# def use(level):
#     def use_logging(func):
#         def wrapper(name):
#             print("%s is running" % func.__name__)
#             return func(name)  # 把 foo 当做参数传递进来时，执行func()就相当于执行foo()
#
#         return wrapper
#
#     return use_logging
#
#
# # @use("one")
def foo(name):
    print("i am %s" % name)
#
#
# # foo = use_logging(foo)  # 因为装饰器 use_logging(foo) 返回的时函数对象 wrapper，这条语句相当于  foo = wrapper
# # foo(name="SuperMan")  # 执行foo(name)就相当于执行 wrapper(name)
#
# foo = use("one")(foo)
#
# # foo("superman")


def use_logging(func):
    def wrapper(name):
        print("%s is running" % func.__name__)
        return func(name)  # 把 foo 当做参数传递进来时，执行func()就相当于执行foo()

    return wrapper


foo = use_logging(foo)
print(foo)
# foo("name")