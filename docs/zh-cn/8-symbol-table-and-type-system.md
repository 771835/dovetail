# 符号表与类型系统

## 符号基类

所有符号继承 [dovetail/core/symbols/base.py](dovetail/core/symbols/base.py) 中的 `Symbol` 抽象基类：

```python
class Symbol(ABC):
    def get_name(self) -> str: ...  # 符号名称

    def get_dtype(self) -> DataTypeBase: ...  # 数据类型
```

带注解的符号还混入 `AnnotationMixin`，提供：

```python
def has_annotation(name) -> bool


    def get_flags(name) -> set[str]

    def get_metadata(name) -> dict

    def all_flags() -> set[str]  # 汇总所有注解 flags（优化器/后端统一入口）
```

## 符号类型

| 符号类           | 文件                       | 说明                           |
|---------------|--------------------------|------------------------------|
| `Variable`    | `symbols/variable.py`    | 变量（含类型、变量类别）                 |
| `Function`    | `symbols/function.py`    | 函数（含参数列表、返回类型、函数类别）          |
| `Parameter`   | `symbols/parameter.py`   | 函数参数                         |
| `Literal`     | `symbols/literal.py`     | 字面量（int/string/boolean/null） |
| `Reference`   | `symbols/reference.py`   | 对其他符号的引用                     |
| `Class`       | `symbols/class_.py`      | 类定义                          |
| `Structure`   | `symbols/structure.py`   | 结构体定义                        |
| `Enumeration` | `symbols/enumeration.py` | 枚举定义                         |
| `Typedef`     | `symbols/typedef.py`     | 类型别名                         |

### Function 符号

```python
@define(slots=True)
class Function(Symbol, AnnotationMixin):
    name: str
    params: list[Parameter]
    return_type: DataTypeBase
    function_type: FunctionType  # FUNCTION / LIBRARY / BUILTIN / METHOD / EXTERN
    annotations: dict[str, AnnotationAttachment]
```

`FunctionType` 枚举：

| 值                        | 说明                |
|--------------------------|-------------------|
| `FUNCTION`               | 用户定义函数            |
| `FUNCTION_UNIMPLEMENTED` | 前向声明，未实现          |
| `LIBRARY`                | 从库加载的函数           |
| `BUILTIN`                | 编译器内置函数           |
| `METHOD`                 | 类方法               |
| `EXTERN`                 | `@extern` 导入的外部函数 |

## 数据类型系统

### 基本类型（PrimitiveDataType）

| 枚举值         | 名称          | 可用于变量声明     |
|-------------|-------------|-------------|
| `INT`       | `int`       | ✅           |
| `STRING`    | `string`    | ✅           |
| `BOOLEAN`   | `boolean`   | ✅           |
| `VOID`      | `void`      | ❌           |
| `NULL_TYPE` | `null`      | ❌           |
| `UNDEFINED` | `undefined` | ❌（仅编译错误时使用） |
| `FUNCTION`  | `function`  | ✅           |

**子类型关系**：`BOOLEAN` 是 `INT` 的子类型，可强制转换。

### 复合类型

```python
class ListType(DataTypeBase):  # list<T>

    class ArrayType(DataTypeBase):  # array<T>  / int[N]

    class MapType(DataTypeBase):  # map<K, V>
```

### 变量类别（VariableType）

影响生成命令中的生命周期管理：

| 值           | 说明              |
|-------------|-----------------|
| `PARAMETER` | 函数参数变量          |
| `COMMON`    | 普通局部变量          |
| `RETURN`    | 函数返回值变量（不被优化删除） |

### 作用域类型（StructureType）

| 值             | 说明      |
|---------------|---------|
| `GLOBAL`      | 全局作用域   |
| `FUNCTION`    | 函数作用域   |
| `CLASS`       | 类定义作用域  |
| `LOOP_CHECK`  | 循环条件作用域 |
| `LOOP_BODY`   | 循环体作用域  |
| `CONDITIONAL` | 条件语句作用域 |
| `INTERFACE`   | 接口定义作用域 |