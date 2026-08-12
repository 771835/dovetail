# coding=utf-8
from dovetail.core.enums import PrimitiveDataType
from dovetail.core.errors import report, Errors
from dovetail.core.instructions import IRCast, IRCall, IRJump
from dovetail.core.lib.lib_factory import LibraryBase, library_func, builtin_func
from dovetail.core.lib.library import LibraryContext
from dovetail.core.symbols import Reference, Variable, Literal
from dovetail.utils.naming import NameDecorator


class Builtins(LibraryBase):
    def __init__(self, context: LibraryContext):
        self.context = context
        self.error_reporter = context.error_reporter
        self.emitter = context.emitter
        self.symbol_resolver = context.symbol_resolver
        self._init(context)

    @builtin_func()
    def exec(self, command: str) -> None:...

    @builtin_func()
    def tellraw_text(self, target: str, msg: str) -> None:...

    @builtin_func()
    def tellraw_json(self, target: str, json: str) -> None:...

    @library_func(returns=int, name="int")
    def _int(self, value: int | str | bool):
        value: Reference[Variable | Literal]  # 真实类型
        if value.dtype == PrimitiveDataType.INT:
            return value.value
        result: Variable = self.emitter.create_temp_var_declared(PrimitiveDataType.INT, "to_int")
        self.emitter.emit(IRCast(result, PrimitiveDataType.INT, value))
        return result

    @library_func(returns=str, name="str")
    def _str(self, value: int | str | bool):
        value: Reference[Variable | Literal]  # 真实类型
        if value.dtype == PrimitiveDataType.STRING:
            return value.value
        result: Variable = self.emitter.create_temp_var_declared(PrimitiveDataType.STRING, "to_str")
        self.emitter.emit(IRCast(result, PrimitiveDataType.STRING, value))
        return result

    @library_func(name="print")
    def _print(self, msg: int | str | bool):
        msg: Reference[Variable | Literal]  # 真实类型
        tellraw_text = self._get_function("tellraw_text")
        if tellraw_text is None:
            self.error_reporter.report(
                Errors.SymbolResolution,
                "函数",
                "tellraw_text"
            )
            return None

        self.emitter.emit(
            IRCall(
                None,
                tellraw_text,
                {
                    "target": Reference.literal("@a"),
                    "msg": msg
                }
            )
        )
        return None

    @library_func(name="_call")
    def _call(self, scope: str):
        scope: Reference[Literal]
        if not scope.is_literal() or scope.get_dtype() != PrimitiveDataType.STRING:
            report(
                Errors.InvalidSyntax,
                "跳转目标必须是字面量字符串"
            )
            return None

        scope_name = str(scope.value.value)

        current_scope = self.symbol_resolver.scope_stack[-1]

        if current_scope.resolve_scope(scope_name) is None:
            self.error_reporter.report(
                Errors.InvalidControlFlow,
                f"跳转目标 '{scope_name}' 不存在"
            )
            return None

        self.emitter.emit(IRJump(scope_name))

        return None

    def __str__(self) -> str:
        return "built-in"

    def get_variables(self):
        _n = NameDecorator.normalize
        return {
            Variable(_n("__namespace__"), PrimitiveDataType.STRING, mutable=False):
                Reference.literal(self.context.config.namespace),
            Variable(_n("__minecraft_version__"), PrimitiveDataType.STRING, mutable=False):
                Reference.literal(self.context.config.version.display_version),
        }
