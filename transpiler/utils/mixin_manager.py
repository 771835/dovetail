# coding=utf-8
import inspect
import uuid
from functools import wraps


# ==== 核心注解定义 ====
class At:
    """定义代码注入点"""
    __slots__ = ('location', 'target')

    HEAD = "HEAD"
    TAIL = "TAIL"
    RETURN = "RETURN"
    CALL_SITE = "CALL_SITE"  # 保留字段但暂不实现

    def __init__(self, location, target=None):
        self.location = location  # 'HEAD', 'TAIL', 'RETURN'
        self.target = target  # 保留字段


class MixinMeta(type):
    """Mixin元类，自动处理注入逻辑"""

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        MixinManager.apply_mixin(cls)


class CallbackInfo:
    """回调基本信息"""
    __slots__ = ('cancelled',)

    def __init__(self):
        self.cancelled = False

    def cancel(self):
        """取消操作"""
        self.cancelled = True


class CallbackInfoReturnable(CallbackInfo):
    """支持返回值操作的回调类"""
    __slots__ = ('return_value', 'return_set', 'uuid')

    def __init__(self, initial_value=None):
        super().__init__()
        self.return_value = initial_value
        self.return_set = False
        self.uuid = uuid.uuid4()

    def set_return_value(self, value):
        """设置返回值并取消原操作"""
        self.return_value = value
        self.return_set = True
        self.cancel()


class _Accessor:
    """访问器描述符，用于访问私有字段"""
    __slots__ = ('field_name',)

    def __init__(self, field_name):
        self.field_name = field_name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.field_name)

    def __set__(self, instance, value):
        setattr(instance, self.field_name, value)


class MixinManager:
    """Mixin注册管理器"""
    _mixin_classes = []
    _is_applied = False  # 添加状态标记

    @classmethod
    def register_mixin(cls, mixin_cls):
        """注册Mixin类"""
        if mixin_cls not in cls._mixin_classes:
            cls._mixin_classes.append(mixin_cls)

    @classmethod
    def apply_all(cls):
        """应用所有注册的Mixin"""
        if not cls._is_applied:
            for mixin_cls in cls._mixin_classes[:]:
                cls.apply_mixin(mixin_cls)
            cls._is_applied = True

    @classmethod
    def apply_mixin(cls, mixin_cls):
        """将单个Mixin应用到目标类"""
        target_class = getattr(mixin_cls, '__mixin_target__', None)
        if not target_class:
            return

        # 处理字段访问器
        accessors = {}
        for attr_name, attr_value in vars(mixin_cls).items():
            if isinstance(attr_value, _Accessor):
                accessors[attr_name] = attr_value

        # 添加访问器到目标类
        for attr_name, accessor in accessors.items():
            setattr(target_class, attr_name, accessor)

        # 收集注入方法
        callbacks = []
        # 收集Invokers
        invokers = {}
        normal_methods = []

        for attr_name in dir(mixin_cls):
            # 跳过特殊方法和保留属性
            if attr_name.startswith('__') and attr_name.endswith('__'):
                continue

            attr = getattr(mixin_cls, attr_name)

            # 1. 收集Inject方法
            if hasattr(attr, '__mixin_inject__'):
                callbacks.append(attr.__mixin_inject__)

            # 2. 收集Invoker方法
            elif hasattr(attr, '__mixin_invoker__'):
                invokers[attr_name] = attr

            # 3. 收集普通方法
            elif inspect.isfunction(attr):
                normal_methods.append((attr_name, attr))

        # 将普通方法添加到目标类（检测名称冲突）
        for method_name, method in normal_methods:
            # 跳过已存在的引用
            if hasattr(target_class, method_name):
                continue

            # 绑定方法到目标类
            setattr(target_class, method_name, method)

        # 按目标方法分组
        method_map = {}
        for cb in callbacks:
            method_name = cb['target_method_name']
            if method_name not in method_map:
                method_map[method_name] = []
            method_map[method_name].append(cb)

        # 应用方法注入
        for method_name, callbacks in method_map.items():
            orig_method = getattr(target_class, method_name, None)
            if not orig_method:
                continue

            cancellable = any(cb['cancellable'] for cb in callbacks)

            # 创建注入包装函数
            def create_injected_method(cg, cancel_flag, orig_method_raw):
                @wraps(orig_method_raw)
                def injected_method(*args, **kwargs):
                    ci = CallbackInfoReturnable() if cancel_flag else CallbackInfo()

                    # 处理HEAD注入 (使用正确的回调分组)
                    for cb in cg:
                        if cb['at'].location == At.HEAD:
                            cb['handler'](ci, *args, **kwargs)

                            if ci.cancelled and cancel_flag:
                                return ci.return_value

                    # 执行原始方法
                    result = orig_method_raw(*args, **kwargs) if not ci.cancelled else ci.return_value

                    # 设置返回值
                    if cancel_flag and not ci.cancelled:
                        ci.return_value = result

                    # 处理TAIL注入
                    if not ci.cancelled:
                        for cb in cg:
                            if cb['at'].location == At.TAIL:
                                cb['handler'](ci, *args, **kwargs)
                                if ci.cancelled and cancel_flag:
                                    return ci.return_value

                    # 处理RETURN注入
                    if not ci.cancelled and cancel_flag:
                        for cb in cg:
                            if cb['at'].location == At.RETURN:
                                cb['handler'](ci, *args, **kwargs)  # 普通函数用原始参数

                        if ci.return_set:
                            result = ci.return_value

                    return result

                return injected_method

            # 设置新的注入方法
            injected_wrapper = create_injected_method(callbacks, cancellable, orig_method)
            setattr(target_class, method_name, injected_wrapper)

        # 添加Invoker到目标类
        for method_name, handler in invokers.items():
            # 使用invoker_前缀避免命名冲突
            handler_name = f"invoker_{method_name}"
            if hasattr(target_class, handler_name):
                continue

            # 创建invoker包装
            @wraps(handler)
            def invoker(self, *args, **kwargs):
                return handler(self, *args, **kwargs)

            setattr(target_class, handler_name, invoker)


# ==== 用户可用的公共API ====
def Mixin(target_class):
    """类装饰器，声明Mixin目标类"""

    def apply_mixin(cls):
        cls.__mixin_target__ = target_class
        MixinManager.register_mixin(cls)
        return cls

    return apply_mixin


def Inject(method_name: str, at: At, cancellable=False):
    """方法装饰器，声明注入点"""

    def decorator(func):
        func.__mixin_inject__ = {
            'target_method_name': method_name,  # 明确使用目标方法名
            'at': at,
            'cancellable': cancellable,
            'handler': func
        }
        return func

    return decorator


def Accessor(field_name):
    """字段访问器装饰器"""
    return _Accessor(field_name)


def Invoker():
    """调用器装饰器，用于动态调用私有方法"""

    def decorator(func):
        func.__mixin_invoker__ = True
        return func

    return decorator


def MethodRedirect(old_class: type, old_method: str, new_class: type, new_method: str):
    """
    方法重定向器
    :param old_class: 原始方法所在类
    :param old_method: 原始方法名
    :param new_class: 新方法所在类
    :param new_method: 新方法名
    """
    new_func = getattr(new_class, new_method, None)
    if new_func:
        setattr(old_class, old_method, new_func)


# ==== 自动初始化 ====
def enable_mixins():
    """启用Mixin系统（在模块最后调用）"""
    MixinManager.apply_all()


# ====== 测试代码 ======
if __name__ == "__main__":
    # ====== Player类定义 ======
    class Player:
        def __init__(self, name):
            self.name = name
            self._health = 100
            self._position = (0, 0, 0)
            self._inventory = []
            self._is_admin = False

        def take_damage(self, amount):
            self._health -= amount
            print(f"{self.name} took {amount} damage! Health: {self._health}")
            return self._health

        def move(self, x, y, z):
            self._position = (x, y, z)
            print(f"{self.name} moved to {self._position}")

        def add_item(self, item):
            self._inventory.append(item)
            print(f"Added {item} to inventory. Total: {len(self._inventory)}")
            return True

        def give_item(self, item):
            print(f"{self.name} gave {item} to someone")
            return True

        def show_inventory(self):
            print("=== Inventory ===")
            return self._inventory


    # ====== Mixin扩展 ======
    @Mixin(Player)
    class PlayerExtensions:

        # 访问器
        health = Accessor('_health')
        position = Accessor('_position')
        admin_status = Accessor('_is_admin')

        # 注入点
        @Inject("take_damage", At(At.HEAD), cancellable=True)
        def damage_injection(self, ci):
            if self.admin_status:
                ci.cancel()
                print(f"⚡ {self.name} is immune to damage!")

        # Invoker方法
        @Invoker()
        def add_items(self, items):
            """批量添加物品"""
            print(f"Adding {len(items)} items...")
            return [self.add_item(item) for item in items]

        # 新增方法
        def heal(self, amount):
            """治疗玩家"""
            self.health += amount
            print(f"✨ {self.name} healed by {amount}. Health: {self.health}")

        def teleport(self, x, y, z):
            """瞬移到指定位置"""
            print(f"🔥 {self.name} teleported to ({x}, {y}, {z})")
            self.position = (x, y, z)


    # ====== 方法重定向 ======
    class CustomInventorySystem:
        @staticmethod
        def formatted_inventory(player):
            """格式化的库存显示方法"""
            print(f"======= {player.name}'s Inventory =======")
            print(f"Items({len(player._inventory)}):")
            for i, item in enumerate(player._inventory, 1):
                print(f"  {i}. {item}")
            return player._inventory


    # 重定向原始库存显示方法
    MethodRedirect(
        old_class=Player,
        old_method="show_inventory",
        new_class=CustomInventorySystem,
        new_method="formatted_inventory"
    )

    # ==== 应用所有Mixin ====
    enable_mixins()

    print("===== Player Mixin Demo =====")

    # 创建普通玩家
    player = Player("Steve")

    # 创建管理员玩家
    admin_player = Player("Admin")
    admin_player.admin_status = True

    # 测试功能
    print("\n--- Testing Normal Player ---")
    player.take_damage(10)
    player.heal(5)
    player.teleport(100, 64, 200)

    print("\n--- Adding Items ---")
    player.invoker_add_items(["Sword", "Shield", "Apple"])

    print("\n--- Show Inventory ---")
    player.show_inventory()

    print("\n--- Give Item ---")
    player.give_item("Sword")

    print("\n--- Testing Admin Player ---")
    admin_player.take_damage(50)  # 应该免疫伤害
    admin_player.invoker_add_items(["Diamond Sword", "Golden Apple"])

    print("\n===== Demo Completed =====")
