# coding=utf-8
"""
一个用于Python的Mixin系统，允许在运行时注入代码和扩展现有类。
此模块提供了装饰器和实用程序，用于将代码注入方法、访问私有字段以及重定向方法调用。
"""

import inspect
import uuid
from functools import wraps
from threading import RLock
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union

# ==== 类型别名 ====
T = TypeVar('T')
TargetClassType = Union[type, object]


# ==== 工具函数 ====

def _set_attr(target_cls: TargetClassType, name: str, value: Any, force: bool = False) -> None:
    """
    在目标类或实例上设置一个属性。

    Args:
        target_cls (TargetClassType): 目标类或实例。
        name (str): 要设置的属性名。
        value (Any): 属性值。
        force (bool): 若为 True，使用 `type.__setattr__` 强制设置。

    Returns:
        None
    """
    if force:
        if isinstance(target_cls, type):
            type.__setattr__(target_cls, name, value)
        else:
            object.__setattr__(target_cls, name, value)
    else:
        setattr(target_cls, name, value)


def _get_attr(target_cls: TargetClassType, name: str, default: Optional[Any] = None, force: bool = False) -> Any:
    """
    从目标类或实例获取一个属性。

    Args:
        target_cls (TargetClassType): 要获取属性的类或实例。
        name (str): 属性的名称。
        default (Optional[Any]): 如果未找到属性，则返回的默认值。
        force (bool): 如果为True，则使用 `type.__getattribute__` 绕过元类限制。

    Returns:
        Any: 属性值或默认值。
    """
    if force:
        try:
            if isinstance(target_cls, type):
                return type.__getattribute__(target_cls, name)
            else:
                return object.__getattribute__(target_cls, name)
        except AttributeError:
            return default
    else:
        return getattr(target_cls, name, default)


# ==== 核心注解 ====

class At:
    """
    定义 Mixin 回调的注入点。

    Attributes:
        location (str): 注入点的位置 ('HEAD', 'TAIL', 'RETURN')。
        target (Optional[str]): 保留字段，供将来使用。
    """

    HEAD: str = "HEAD"
    TAIL: str = "TAIL"
    RETURN: str = "RETURN"
    CALL_SITE: str = "CALL_SITE"  # 保留供将来使用

    def __init__(self, location: str, target: Optional[str] = None) -> None:
        """
        初始化一个注入点。

        Args:
            location (str): 注入的位置 ('HEAD', 'TAIL', 'RETURN')。
            target (Optional[str]): 保留的目标。

        Returns:
            None
        """
        self.location = location
        self.target = target


class MixinMeta(type):
    """
    Mixin 类的元类。在创建 Mixin 类时自动应用 Mixins。"""

    def __init__(cls, name: str, bases: Tuple[type, ...], attrs: Dict[str, Any]):
        """
        初始化 Mixin 类并应用它。

        Args:
            name (str): Mixin 类的名称。
            bases (Tuple[type, ...]): Mixin 的基类。
            attrs (Dict[str, Any]): Mixin 类的属性。

        """
        super().__init__(name, bases, attrs)
        MixinManager.apply_mixin(cls)


class CallbackInfo:
    """
    回调信息的基类。

    Attributes:
        cancelled (bool): 如果为True，则表示操作被取消。
        return_value (Any): 取消时要使用的返回值。
    """

    def __init__(self, initial_value: Optional[Any] = None) -> None:
        """
        初始化回调信息。

        Args:
            initial_value (Optional[Any]): 初始返回值。

        Returns:
            None
        """
        self.return_value = initial_value
        self.cancelled = False

    def cancel(self) -> None:
        """
        取消操作。

        Returns:
            None
        """
        self.cancelled = True


class CallbackInfoReturnable(CallbackInfo):
    """
    支持设置返回值的回调信息。

    Attributes:
        return_set (bool): 指示是否已设置返回值。
    """

    def __init__(self, initial_value: Optional[Any] = None) -> None:
        """
        初始化可返回的回调信息。

        Args:
            initial_value (Any): 初始返回值。

        Returns:
            None
        """
        super().__init__(initial_value)
        self.return_set = False

    def set_return_value(self, value: Any) -> None:
        """
        设置返回值并取消原始操作。

        Args:
            value (Any): 要返回的值。

        Returns:
            None
        """
        self.return_value = value
        self.return_set = True
        self.cancel()


class _Accessor:
    """
    用于访问私有字段的内部类。

    Attributes:
        _field_name (str): 要访问的私有字段的名称。
    """
    __slots__ = ('_field_name',)

    METADATA_ATTRS: set = {
        '__mixin_target__',
        '__mixin_force__',
        '__class__',
        '__dict__'
    }

    def __init__(self, field_name: str) -> None:
        """
        初始化字段的访问器。

        Args:
            field_name (str): 要访问的私有字段的名称。

        Returns:
            None
        """
        self._field_name = field_name

    def __get__(self, instance: Optional[Any], owner: Optional[Type] = None) -> Any:
        """
        获取私有字段的值。

        Args:
            instance (Optional[Any]): 要获取字段的实例。
            owner (Optional[Type]): 所有者类。

        Returns:
            Any: 字段的值。
        """
        if instance is None:
            return self
        return object.__getattribute__(instance, self._field_name)

    def __set__(self, instance: Any, value: Any) -> None:
        """
        设置私有字段的值。

        Args:
            instance (Any): 要设置字段的实例。
            value (Any): 要设置的值。

        Returns:
            None
        """
        object.__setattr__(instance, self._field_name, value)


class MixinManager:
    """管理 Mixins 的注册和应用。"""
    _lock = RLock()

    @classmethod
    def register_mixin(cls, mixin_cls: type) -> None:
        """
        注册一个 Mixin 并将其应用于目标类。

        Args:
            mixin_cls (type): 要注册的 Mixin 类。

        Returns:
            None
        """
        with cls._lock:
            cls.apply_mixin(mixin_cls)

    @classmethod
    def apply_mixin(cls, mixin_cls: type) -> None:
        """
        将单个 Mixin 应用于其目标类。

        Args:
            mixin_cls (type): 要应用的 Mixin 类。

        Returns:
            None
        """
        try:
            target_class: Optional[type] = object.__getattribute__(mixin_cls, '__mixin_target__')
            force_mixin: bool = object.__getattribute__(mixin_cls, '__mixin_force__')
        except AttributeError:
            return

        if not target_class:
            return

        # 应用访问器
        accessors: Dict[str, _Accessor] = {
            attr_name: attr_value
            for attr_name, attr_value in vars(mixin_cls).items()
            if isinstance(attr_value, _Accessor)
        }
        for attr_name, accessor in accessors.items():
            _set_attr(target_class, attr_name, accessor, force=True)

        # 收集回调、调用器和普通方法
        callbacks: List[Dict[str, Any]] = []
        invokers: Dict[str, Callable] = {}
        normal_methods: List[Tuple[str, Callable]] = []

        for attr_name in dir(mixin_cls):
            if attr_name.startswith("__") and attr_name.endswith("__"):
                continue

            attr = _get_attr(mixin_cls, attr_name, force=force_mixin)

            if hasattr(attr, '__mixin_inject__'):
                callbacks.append(attr.__mixin_inject__)
            elif hasattr(attr, '__mixin_invoker__'):
                invokers[attr_name] = attr
            elif inspect.isfunction(attr):
                normal_methods.append((attr_name, attr))

        # 应用普通方法
        for method_name, method in normal_methods:
            if not hasattr(target_class, method_name):
                _set_attr(target_class, method_name, method, force_mixin)

        # 按方法名分组回调
        method_map: Dict[str, List[Dict[str, Any]]] = {}
        for cb in callbacks:
            method_name = cb['target_method_name']
            if method_name not in method_map:
                method_map[method_name] = []
            method_map[method_name].append(cb)

        # 注入回调到目标方法
        for method_name, callbacks_group in method_map.items():
            orig_method = _get_attr(target_class, method_name, force=force_mixin)
            if not orig_method:
                continue

            cancellable = any(cb['cancellable'] for cb in callbacks_group)

            def make_injected_method(
                    callback_group: List[Dict[str, Any]],
                    is_cancellable: bool,
                    original_method: Callable
            ) -> Callable:
                """
                工厂函数，用于创建带注入的闭包方法。

                Args:
                    callback_group (List[Dict[str, Any]]): 回调函数列表。
                    is_cancellable (bool): 是否支持取消。
                    original_method (Callable): 原始方法。

                Returns:
                    Callable: 注入后的方法。
                """

                @wraps(original_method)
                def injected_method(*args, **kwargs) -> Any:
                    """
                    注入后的实际方法。

                    Returns:
                        Any: 方法执行结果。
                    """
                    ci = CallbackInfoReturnable() if is_cancellable else CallbackInfo()

                    # HEAD阶段
                    for cb in callback_group:
                        if cb['at'].location == At.HEAD:
                            cb['handler'](ci, *args, **kwargs)
                            if ci.cancelled and is_cancellable:
                                return ci.return_value

                    # 执行原始方法（如果未被取消）
                    if not ci.cancelled:
                        result = original_method(*args, **kwargs)
                        if is_cancellable:
                            ci.return_value = result
                    else:
                        result = ci.return_value

                    # TAIL阶段
                    if not ci.cancelled:
                        for cb in callback_group:
                            if cb['at'].location == At.TAIL:
                                cb['handler'](ci, *args, **kwargs)
                                if ci.cancelled and is_cancellable:
                                    return ci.return_value

                    # RETURN阶段
                    if not ci.cancelled:
                        return_callbacks = [cb for cb in callback_group if cb['at'].location == At.RETURN]
                        for cb in return_callbacks:
                            cb['handler'](ci, *args, **kwargs)

                    return result

                return injected_method

            injected_wrapper = make_injected_method(callbacks_group, cancellable, orig_method)
            _set_attr(target_class, method_name, injected_wrapper, force_mixin)

        # 应用调用器
        for method_name, handler in invokers.items():
            handler_name = f"_mixin_invoker_{method_name}_{uuid.uuid4().hex[:8]}"
            if not hasattr(target_class, handler_name):
                def make_invoker(handler_func: Callable) -> Callable:
                    """
                    创建调用器函数。

                    Args:
                        handler_func (Callable): 处理函数。

                    Returns:
                        Callable: 调用器函数。
                    """

                    @wraps(handler_func)
                    def invoker(self, *args, **kwargs) -> Any:
                        """
                        调用器实际函数。

                        Returns:
                            Any: 函数执行结果。
                        """
                        return handler_func(self, *args, **kwargs)

                    return invoker

                invoker_func = make_invoker(handler)
                _set_attr(target_class, handler_name, invoker_func, force_mixin)


# ==== 用户公共 API ====

def Mixin(target_class: type, force: bool = False) -> Callable[[type], type]:
    """
    类装饰器，用于声明一个 Mixin 及其目标类。

    Args:
        target_class (type): 要注入 Mixin 的类。
        force (force): 如果为True，则使用 `type.__setattr__` 绕过元类限制。

    Returns:
        Callable[[type], type]: 一个注册 Mixin 的装饰器函数。
    """

    def apply_mixin(cls: type) -> type:
        """
        将 Mixin 应用于目标类。

        Args:
            cls (type): 要应用的 Mixin 类。

        Returns:
            type: Mixin 类本身。
        """
        if force:
            type.__setattr__(cls, "__mixin_target__", target_class)
            type.__setattr__(cls, "__mixin_force__", force)
        else:
            cls.__mixin_target__ = target_class
            cls.__mixin_force__ = force
        MixinManager.register_mixin(cls)
        return cls

    return apply_mixin


def Inject(method_name: str, at: At, cancellable: bool = False) -> Callable[[Callable], Callable]:
    """
    方法装饰器，用于声明一个方法的注入点。

    Args:
        method_name (str): 目标类中要注入的方法名。
        at (At): 一个 `At` 实例，指定注入位置 (HEAD, TAIL, RETURN)。
        cancellable (bool): 如果为True，注入的方法可以取消原始操作。

    Returns:
        Callable[[Callable], Callable]: 标记方法为注入回调的装饰器函数。
    """

    def decorator(func: Callable) -> Callable:
        """
        装饰器函数。

        Args:
            func (Callable): 被装饰的函数。

        Returns:
            Callable: 装饰后的函数。
        """
        func.__mixin_inject__ = {
            'target_method_name': method_name,
            'at': at,
            'cancellable': cancellable,
            'handler': func
        }
        return func

    return decorator


def Accessor(field_name: str) -> _Accessor:
    """
    创建一个用于访问私有字段的描述符。

    Args:
        field_name (str): 要访问的字段名 (例如, '_private_field')。

    Returns:
        _Accessor: 一个 `_Accessor` 实例。
    """
    return _Accessor(field_name)


def Invoker() -> Callable[[Callable], Callable]:
    """
    方法装饰器，用于将一个方法作为公共方法添加到目标类。

    Returns:
        Callable[[Callable], Callable]: 一个装饰器函数。
    """

    def decorator(func: Callable) -> Callable:
        """
        装饰器函数。

        Args:
            func (Callable): 被装饰的函数。

        Returns:
            Callable: 装饰后的函数。
        """
        func.__mixin_invoker__ = True
        return func

    return decorator


def MethodRedirect(
        old_class: type,
        old_method: str,
        new_class: type,
        new_method: str,
        force: bool = False
):
    """
    将旧类上的方法调用重定向到新类上的方法。

    Args:
        old_class (type): 包含原始方法的类。
        old_method (str): 要替换的原始方法的名称。
        new_class (type): 包含新方法的类。
        new_method (str): 要调用的新方法的名称。
        force (bool): 如果为True，则使用 `type.__setattr__` 绕过元类限制。

    """
    new_func = _get_attr(new_class, new_method, force=force)
    if new_func:
        _set_attr(old_class, old_method, new_func, force)


# ====== 测试代码 ======
if __name__ == "__main__":
    # ====== Player 类定义 (使用冻结元类) ======
    class FreezeClassMeta(type):
        """元类，在类创建后阻止修改其结构。"""

        def __init__(cls, name: str, bases: Tuple[type, ...], attrs: Dict[str, Any]):
            """
            初始化元类。

            Args:
                name (str): 类名。
                bases (Tuple[type, ...]): 基类元组。
                attrs (Dict[str, Any]): 类属性字典。

            """
            super().__init__(name, bases, attrs)
            cls._frozen = True

        def __setattr__(cls, name: str, value: Any):
            """
            设置类属性。

            Args:
                name (str): 属性名。
                value (Any): 属性值。

            Raises:
                AttributeError: 如果类已被冻结。
            """
            if getattr(cls, '_frozen', False):
                raise AttributeError(f"无法修改已冻结的类 '{cls.__name__}'")
            super().__setattr__(name, value)


    class Player(metaclass=FreezeClassMeta):
        """
        演示用的简单玩家类。

        Attributes:
            name (str): 玩家名称。
            _health (int): 玩家生命值。
            _position (Tuple[int, int, int]): 玩家位置。
            _inventory (List[str]): 玩家库存。
            _is_admin (bool): 管理员状态。
        """

        def __init__(self, name: str):
            """
            初始化一个具有名称的玩家。

            Args:
                name (str): 玩家名称。

            """
            self.name = name
            self._health = 100
            self._position = (0, 0, 0)
            self._inventory = []
            self._is_admin = False

        def take_damage(self, amount: int) -> int:
            """
            受到伤害并减少生命值。

            Args:
                amount (int): 伤害量。

            Returns:
                int: 剩余生命值。
            """
            self._health -= amount
            print(f"{self.name} 受到 {amount} 点伤害! 生命值: {self._health}")
            return self._health

        def move(self, x: int, y: int, z: int):
            """
            将玩家移动到新位置。

            Args:
                x (int): X坐标。
                y (int): Y坐标。
                z (int): Z坐标。

            """
            self._position = (x, y, z)
            print(f"{self.name} 移动到了 {self._position}")

        def add_item(self, item: str) -> bool:
            """
            将物品添加到玩家的库存中。

            Args:
                item (str): 物品名称。

            Returns:
                bool: 添加成功返回True。
            """
            self._inventory.append(item)
            print(f"将 {item} 添加到库存。总计: {len(self._inventory)}")
            return True

        def give_item(self, item: str) -> bool:
            """
            将物品给予他人。

            Args:
                item (str): 物品名称。

            Returns:
                bool: 给予成功返回True。
            """
            print(f"{self.name} 给予了别人 {item}")
            return True

        def show_inventory(self) -> List[str]:
            """
            显示玩家当前的库存。

            Returns:
                List[str]: 玩家库存列表。
            """
            print("=== 库存 ===")
            return self._inventory


    # ====== Mixin 扩展 ======
    @Mixin(Player, force=True)
    class PlayerExtensions:
        """
        玩家类的扩展。

        Attributes:
            health (_Accessor): 生命值访问器。
            position (_Accessor): 位置访问器。
            admin_status (_Accessor): 管理员状态访问器。
        """

        health = Accessor('_health')
        position = Accessor('_position')
        admin_status = Accessor('_is_admin')

        @staticmethod
        @Inject("take_damage", At(At.HEAD), cancellable=True)
        def damage_injection(ci: CallbackInfoReturnable, self: 'Player', amount: int):
            """
            如果玩家是管理员，则防止受到伤害。

            Args:
                ci (CallbackInfoReturnable): 回调信息。
                self (Player): 玩家实例。
                amount (int): 伤害量。

            """
            if self.admin_status:
                ci.cancel()
                print(f"⚡ {self.name} 对伤害免疫！")

        def add_items(self, items: List[str]) -> List[bool]:
            """
            将多个物品添加到库存中。

            Args:
                items (List[str]): 物品列表。

            Returns:
                List[bool]: 添加结果列表。
            """
            print(f"正在添加 {len(items)} 个物品...")
            return [self.add_item(item) for item in items]

        def heal(self, amount: int):
            """
            治疗玩家。

            Args:
                amount (int): 治疗量。

            """
            self.health += amount
            print(f"✨ {self.name} 受到了 {amount} 点治疗。生命值: {self.health}")

        def teleport(self, x: int, y: int, z: int):
            """
            将玩家传送到新位置。

            Args:
                x (int): X坐标。
                y (int): Y坐标。
                z (int): Z坐标。

            """
            print(f"🔥 {self.name} 传送到了 ({x}, {y}, {z})")
            self.position = (x, y, z)


    @Mixin(Player, force=True)
    class PlayerExtensions2:
        """
        玩家类的另一组扩展。

        Attributes:
            admin_status (_Accessor): 管理员状态访问器。
        """
        admin_status = Accessor('_is_admin')

        @staticmethod
        @Inject("__init__", At(At.HEAD))
        def post_init(ci: CallbackInfo, self: 'Player', name: str):
            """
            为所有新的 Player 实例添加一个私有的 '_is_ban' 字段。

            Args:
                ci (CallbackInfo): 回调信息。
                self (Player): 玩家实例。
                name (str): 玩家名称。
            """
            self._is_ban = False

        @staticmethod
        @Inject("take_damage", At(At.HEAD), cancellable=True)
        def damage_injection(ci: CallbackInfoReturnable, self: 'Player', amount: int):
            """
            如果玩家被封禁，则防止受到伤害。

            Args:
                ci (CallbackInfoReturnable): 回调信息。
                self (Player): 玩家实例。
                amount (int): 伤害量。
            """
            if getattr(self, '_is_ban', False):
                ci.cancel()
                print(f"⚡ {self.name} 已经被ban了，你无法对其造成伤害!")

        @staticmethod
        def ban(player: 'Player'):
            """
            封禁一个玩家，防止他们受到伤害。

            Args:
                player (Player): 玩家实例。
            """
            if not player.admin_status:
                player._is_ban = True
                print(f"🚫 {player.name} 已被封禁!")
            else:
                print("你不能ban一个管理员")


    # ====== 方法重定向 ======
    class CustomInventorySystem:
        """用于显示玩家库存的新系统。"""

        @staticmethod
        def formatted_inventory(player: 'Player') -> List[str]:
            """
            显示玩家库存的格式化版本。

            Args:
                player (Player): 玩家实例。

            Returns:
                List[str]: 玩家库存列表。
            """
            print(f"======= {player.name} 的库存 =======")
            print(f"物品数量({len(player._inventory)}):")
            for i, item in enumerate(player._inventory, 1):
                print(f"  {i}. {item}")
            return player._inventory


    MethodRedirect(
        old_class=Player,
        old_method="show_inventory",
        new_class=CustomInventorySystem,
        new_method="formatted_inventory",
        force=True
    )

    print("===== Player Mixin 演示 =====")

    player = Player("爱丽丝")
    admin_player = Player("管理员")
    admin_player.admin_status = True
    admin_player.position = (114, 514, 1919)

    print("\n--- 测试普通玩家 (爱丽丝) ---")
    player.take_damage(10)
    player.heal(5)
    player.teleport(100, 64, 200)
    player.add_items(["剑", "盾牌", "苹果"])
    player.show_inventory()
    player.give_item("剑")
    player.ban()
    player.take_damage(1)
    player.take_damage(114)

    print("\n--- 测试管理员玩家 ---")
    admin_player.take_damage(50)
    admin_player.add_items(["钻石剑", "金苹果"])
    admin_player.ban()

    print("\n===== 演示完成 =====")
