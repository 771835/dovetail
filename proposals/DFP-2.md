# DFP 2: IR 设计与规范

> 原DFP3(现[DFP10000](DFP-10000.md))附录一

## 状态

- [ ] Draft
- [ ] Proposed
- [ ] Accepted
- [ ] Rejected
- [ ] Deferred
- [ ] Implemented (版本: )
- [x] Active
- [ ] Abandoned (版本: )

## 提案信息

**作者**: 771835 <2790834181@qq.com>  
**创建日期**: 2025-11-09  
**最新更新**: 2025-12-28

## 设计目标

1. 作为AST和最终Minecraft命令之间的中间层
2. 支持观察者模式进行优化和转换
3. 低级化但不至于过度细分
4. 保留足够信息用于生成高效命令
5. 支持序列化和反序列化

## 技术规范

### IR基本指令集

#### 控制流指令

| 指令          | 参数                                | 备注                  |
|-------------|-----------------------------------|---------------------|
| JUMP        | scope                             | 无条件跳转到指定作用域         |
| COND_JUMP   | cond_var true_scope [false_scope] | 条件跳转到作用域（提供双目标）     |
| FUNCTION    | func                              | 函数定义                |
| RETURN      | [value]                           | 从函数返回（可选返回值）        |
| CALL        | result func [args...]             | 函数调用                |
| SCOPE_BEGIN | name type                         | 作用域开始标记（可标记为函数、循环等） |
| SCOPE_END   | name type                         | 作用域结束标记             |
| BREAK       | scope_name                        | 跳出指定循环              |
| CONTINUE    | scope_name                        | 终止当前循环迭代，继续下次迭代     |

#### 变量操作

| 指令       | 参数                   | 备注                    |
|----------|----------------------|-----------------------|
| DECLARE  | variable             | 声明变量                  |
| ASSIGN   | target source        | 赋值操作                  |
| UNARY_OP | result op operand    | 一元运算（如 `-a`, `!b`）    |
| OP       | result op left right | 二元运算（如 `a+b`, `c*d`）  |
| COMPARE  | result op left right | 比较运算（如 `a>b`, `c==d`） |
| CAST     | result type value    | 显式类型转换                |

#### 面向对象指令

| 指令          | 参数                          | 备注      |
|-------------|-----------------------------|---------|
| CLASS       | class                       | 声明类结构   |
| NEW_OBJ     | result class [args...]      | 创建对象实例  |
| GET_FIELD   | result obj property         | 获取对象属性值 |
| SET_FIELD   | obj property value          | 设置对象属性值 |
| CALL_METHOD | result obj method [args...] | 调用对象方法  |

### 关键实现细节

#### 1. 变量管理

- 所有变量强制显式声明
- 所有变量强制手动类型转换，特殊指令除外
- 变量作用域通过SCOPE_BEGIN和SCOPE_END指令显式声明

#### 2. 控制流实现

##### if-else 示例

```dovetail
if (cond_var) {
    # if块代码
} else {
    # else块代码
}
# 转换成ir:

IROpCode.SCOPE_BEGIN(operands=['if_0', <StructureType.CONDITIONAL: 'conditional'>], line=-1, column=-1)
    # if块代码
IROpCode.SCOPE_END(operands=['if_0', <StructureType.CONDITIONAL: 'conditional'>], line=-1, column=-1)
IROpCode.SCOPE_BEGIN(operands=['else_0', <StructureType.CONDITIONAL: 'conditional'>], line=-1, column=-1)
    # else块代码
IROpCode.SCOPE_END(operands=['else_0', <StructureType.CONDITIONAL: 'conditional'>], line=-1, column=-1)
IROpCode.COND_JUMP(operands=[Variable(name='cond__var', dtype=BOOLEAN, var_type=<VariableType.COMMON: 'common'>), 'if_0', 'else_0'], line=-1, column=-1)
```

##### 传统for循环示例

```dovetail
for (int i=0;i<3;i=i+1) {
    # 循环体
}
# 转换成ir:
# int i=0
IROpCode.DECLARE(operands=[Variable(name='i', dtype=INT, var_type=<VariableType.COMMON: 'common'>)], line=-1, column=-1)
IROpCode.ASSIGN(operands=[Variable(name='i', dtype=INT, var_type=<VariableType.COMMON: 'common'>), Reference(value_type=<ValueType.LITERAL: 'literal'>, value=Literal(dtype=INT, value=0))], line=-1, column=-1)
IROpCode.SCOPE_BEGIN(operands=['for_0_check', <StructureType.LOOP_CHECK: 'loop_check'>], line=-1, column=-1)
    IROpCode.SCOPE_BEGIN(operands=['for_0_body', <StructureType.LOOP_BODY: 'loop_body'>], line=-1, column=-1)
        # i=i+1
        IROpCode.DECLARE(operands=[Variable(name='calc_1', dtype=INT, var_type=<VariableType.COMMON: 'common'>)], line=-1, column=-1)
        IROpCode.OP(operands=[Variable(name='calc_1', dtype=INT, var_type=<VariableType.COMMON: 'common'>), <BinaryOps.ADD: '+'>, Reference(value_type=<ValueType.VARIABLE: 'variable'>, value=Variable(name='i', dtype=INT, var_type=<VariableType.COMMON: 'common'>)), Reference(value_type=<ValueType.LITERAL: 'literal'>, value=Literal(dtype=INT, value=1))], line=-1, column=-1)
        IROpCode.ASSIGN(operands=[Variable(name='i', dtype=INT, var_type=<VariableType.COMMON: 'common'>), Reference(value_type=<ValueType.VARIABLE: 'variable'>, value=Variable(name='calc_1', dtype=INT, var_type=<VariableType.COMMON: 'common'>))], line=-1, column=-1)
    IROpCode.SCOPE_END(operands=['for_0_body', <StructureType.LOOP_BODY: 'loop_body'>], line=-1, column=-1)
    # i<3
    IROpCode.DECLARE(operands=[Variable(name='result_variable_2', dtype=BOOLEAN, var_type=<VariableType.COMMON: 'common'>)], line=-1, column=-1)
    IROpCode.COMPARE(operands=[Variable(name='result_variable_2', dtype=BOOLEAN, var_type=<VariableType.COMMON: 'common'>), <CompareOps.LT: '<'>, Reference(value_type=<ValueType.VARIABLE: 'variable'>, value=Variable(name='i', dtype=INT, var_type=<VariableType.COMMON: 'common'>)), Reference(value_type=<ValueType.LITERAL: 'literal'>, value=Literal(dtype=INT, value=3))], line=-1, column=-1)
    IROpCode.COND_JUMP(operands=[Variable(name='result_variable_2', dtype=BOOLEAN, var_type=<VariableType.COMMON: 'common'>), 'for_0_body', None], line=-1, column=-1)
    IROpCode.COND_JUMP(operands=[Variable(name='result_variable_2', dtype=BOOLEAN, var_type=<VariableType.COMMON: 'common'>), 'for_0_check', None], line=-1, column=-1)
IROpCode.SCOPE_END(operands=['for_0_check', <StructureType.LOOP_CHECK: 'loop_check'>], line=-1, column=-1)
IROpCode.JUMP(operands=['for_0_check'], line=-1, column=-1)
```

## 兼容性影响

1. 保持指令简洁但表达能力完整
2. 便于进行各种优化(常量折叠、死代码消除等)
3. 支持高级语言特性到低级命令的转换

## 变更日志

- 2025-11-09 独立为一篇单独的提案
- 2025-12-28 修改了项目信息以适应最新格式

## 附录

### 参数类型定义表

#### 基础符号类 (Symbol)

```python
class Symbol(ABC):
    @abstractmethod
    def get_name(self) -> str: ...
```

#### 类定义 (Class)

```python
@define(slots=True)
class Class(Symbol, DataTypeBase):
    name: str  # 类名
    methods: set[Function]  # 方法集合
    interface: Optional[Class]  # 实现的接口
    parent: Optional[Class]  # 父类
    properties: set[Reference[Variable]]  # 属性
    type: ClassType = ClassType.CLASS  # 类型（类/接口）

    def get_name(self) -> str: ...

    def is_subclass_of(self, other) -> bool: ...
```

#### 常量定义 (Constant)

```python
@define(slots=True)
class Constant(Symbol):
    name: str  # 常量名
    dtype: DataTypeBase  # 数据类型
    var_type: VariableType = VariableType.COMMON  # 变量类型

    def get_name(self) -> str: ...
```

#### 变量定义 (Variable)

```python
@define(slots=True)
class Variable(Symbol):
    name: str  # 变量名
    dtype: DataTypeBase  # 数据类型
    var_type: VariableType = VariableType.COMMON  # 变量类型

    def get_name(self) -> str: ...
```

#### 函数定义 (Function)

```python
@define(slots=True)
class Function(Symbol):
    name: str  # 函数名
    params: list[Parameter]  # 参数列表
    return_type: DataTypeBase  # 返回类型
    function_type: FunctionType = FunctionType.FUNCTION  # 函数类型
    annotations: list[str] = []

    def get_name(self) -> str: ...
```

#### 字面量定义 (Literal)

```python
@define(slots=True, frozen=True)
class Literal(Symbol):
    dtype: DataType  # 数据类型
    value: str | int | bool | None  # 字面量值

    def get_name(self) -> None: ...
```

#### 参数定义 (Parameter)

```python
@define(slots=True)
class Parameter(Symbol):
    var: Variable  # 参数变量
    optional: bool = False  # 是否可选
    default: Reference[Variable | Literal | Constant] = None  # 默认值

    def get_name(self) -> str: ...

    def get_data_type(self) -> DataTypeBase: ...
```

#### 引用定义 (Reference)

```python
@define(slots=True, hash=True)
class Reference(Symbol, Generic[T]):
    value_type: ValueType  # 引用值类型
    value: Variable | Constant | Literal | Function | Class  # 被引用的符号

    def get_name(self) -> str | None: ...

    def get_data_type(self) -> DataTypeBase: ...

    @classmethod
    def literal(cls, value): ...

    @classmethod
    def variable(cls, var_name, dtype: DataType, var_type: VariableType = VariableType.COMMON) -> Reference: ...
```

#### 枚举类型说明

**ValueType 枚举：**

- `LITERAL`: 字面量值，编译时已知
- `VARIABLE`: 变量值，运行时确定
- `CONSTANT`: 常量值，不可修改
- `FUNCTION`: 函数值，可调用对象
- `CLASS`: 类值，类型对象

**DataType 枚举：**

- `INT`: 整数类型，对应 Minecraft 计分板分数
- `STRING`: 字符串类型，用于命名和文本处理
- `BOOLEAN`: 布尔类型，内部表示为 0/1 整数
- `NULL`: 空值类型，表示未初始化或无效值
- `Function`: 函数类型(未使用)
- `Type`: 类型(未使用)

**VariableType 枚举：**

- `COMMON`: 普通局部变量
- `PARAMETER`: 函数参数变量
- `RETURN`: 函数返回值变量(不被优化)

**FunctionType 枚举：**

- `FUNCTION`: 用户定义的函数
- `BUILTIN`: 后端内建函数
- `METHOD`: 类方法函数
- `LIBRARY`: 从库加载的函数

**ClassType 枚举：**

- `CLASS`: 具体类，可实例化
- `INTERFACE`: 接口类，定义契约

**StructureType 枚举：**

- `GLOBAL`: 全局作用域
- `FUNCTION`: 函数作用域
- `CLASS`: 类定义作用域
- `LOOP_CHECK`: 循环条件检查作用域
- `LOOP_BODY`: 循环体执行作用域
- `INTERFACE`: 接口定义作用域
- `CONDITIONAL`: 条件语句作用域