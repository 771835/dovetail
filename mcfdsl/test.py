
def print_all_attributes(obj):
    # 获取实例自身的属性（包括 __dict__ 和 __slots__）
    attrs = {}
    try:
        attrs.update(vars(obj))  # 常规属性
    except TypeError:
        pass
    if hasattr(obj, '__slots__'):  # 处理 __slots__
        for slot in obj.__slots__:
            if hasattr(obj, slot):
                attrs[slot] = getattr(obj, slot)

    # 输出实例自身属性
    for attr, value in attrs.items():
        print(f"{attr}: {value}")

    # 获取通过 property 定义的动态属性
    for name in dir(type(obj)):
        if isinstance(getattr(type(obj), name), property):
            try:
                value = getattr(obj, name)
                print(f"{name} (property): {value}")
            except Exception as e:
                print(f"{name} (property): <无法获取值: {e}>")


