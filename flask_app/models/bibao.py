def print_msg():
    # print_msg 是外围函数
    msg = "zen of python"

    def printer():
        # printer 是嵌套函数
        print(msg)

    return printer


another = print_msg()


# 输出 zen of python
# another()


# def adder(x):
#     def wrapper(y):
#         return x + y
#
#     return wrapper
#
#
# # print(adder(5))
# adder5 = adder(5)
# # 输出 15
# print(adder5(10))
# # 输出 11
# # adder5(6)
