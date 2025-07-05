# coding=utf-8
import io
import sys


def print_all_attributes(obj, color=True, print_output=True):
    """带返回值支持的属性打印函数

    Args:
        obj: 要分析的对象
        color: 是否启用颜色输出 (默认启用)
        print_output: 是否打印输出内容 (默认打印)

    Returns:
        当 return_output=True 时返回完整输出字符串
    """
    buffer = io.StringIO()
    COLOR = {}  # 颜色配置字典 # NOQA

    def setup_colors(use_color):
        """配置颜色方案"""
        nonlocal COLOR
        if use_color:
            COLOR = {  # NOQA
                'reset': '\033[0m',
                'title': '\033[34m',  # 蓝色
                'section': '\033[33m',  # 黄色
                'name': '\033[32m',  # 绿色
                'value': '\033[37m',  # 白色
                'error': '\033[31m',  # 红色
                'prop': '\033[36m'  # 青色
            }
        else:
            COLOR = {k: '' for k in ['reset', 'title', 'section', 'name', 'value', 'error', 'prop']}  # NOQA

    def write(line):
        """统一写入方法"""
        buffer.write(line + '\n')

    # 主逻辑
    setup_colors(color)
    header = f" 对象属性分析 [{type(obj).__name__}] "
    write(f"{COLOR['title']}{'=' * 30}{header}{'=' * 30}{COLOR['reset']}")

    # 收集属性逻辑
    def collect_attributes():
        try:
            instance_attrs = vars(obj).copy()
        except TypeError:
            instance_attrs = {}

        slots_attrs = {}
        if hasattr(obj, '__slots__'):
            for slot in obj.__slots__:
                if hasattr(obj, slot):
                    slots_attrs[slot] = getattr(obj, slot)

        properties = {}
        for name in dir(type(obj)):
            attr = getattr(type(obj), name)
            if isinstance(attr, property):
                try:
                    properties[name] = getattr(obj, name)
                except Exception as e:
                    properties[name] = f"<错误: {str(e)}>"

        return instance_attrs, slots_attrs, properties

    instance_attrs, slots_attrs, properties = collect_attributes()

    # 统一打印逻辑
    def print_attr_set(title, attrs, is_property=False):
        write(f"{COLOR['section']}■ {title}{COLOR['reset']}")
        if not attrs:
            write(f"  {COLOR['value']}(无){COLOR['reset']}")
            return

        for name, value in attrs.items():
            if isinstance(value, str) and value.startswith("<错误:"):
                value_str = f"{COLOR['error']}{value}{COLOR['reset']}"
            else:
                value_str = f"{COLOR['value']}{repr(value)}{COLOR['reset']}"

            marker = f"{COLOR['prop']}↳{COLOR['reset']}" if is_property else "•"
            write(f"  {marker} {COLOR['name']}{name}{COLOR['reset']}: {value_str}")

    # 分块输出
    print_attr_set("实例属性", instance_attrs)
    print_attr_set("Slots 属性", slots_attrs)
    print_attr_set("动态属性", properties, is_property=True)
    write(f"{COLOR['title']}{'=' * 80}{COLOR['reset']}")

    # 获取输出内容
    output = buffer.getvalue()

    # 根据参数决定是否打印
    if print_output:
        sys.stdout.write(output)

    return output
