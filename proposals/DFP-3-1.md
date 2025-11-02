# IR (Intermediate Representation) 设计

## IR设计目标

1. 作为AST和最终Minecraft命令之间的中间层
2. 支持观察者模式进行优化和转换
3. 低级化但不至于过度细分
4. 保留足够信息用于生成高效命令
5. 支持序列化和反序列化

## IR基本指令集

### 控制流指令

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

### 变量操作

| 指令       | 参数                   | 备注                    |
|----------|----------------------|-----------------------|
| DECLARE  | variable             | 声明变量                  |
| ASSIGN   | target source        | 赋值操作                  |
| UNARY_OP | result op operand    | 一元运算（如 `-a`, `!b`）    |
| OP       | result op left right | 二元运算（如 `a+b`, `c*d`）  |
| COMPARE  | result op left right | 比较运算（如 `a>b`, `c==d`） |
| CAST     | result type value    | 显式类型转换                |

### 面向对象指令

| 指令          | 参数                          | 备注      |
|-------------|-----------------------------|---------|
| CLASS       | class                       | 声明类结构   |
| NEW_OBJ     | result class [args...]      | 创建对象实例  |
| GET_FIELD   | result obj property         | 获取对象属性值 |
| SET_FIELD   | obj property value          | 设置对象属性值 |
| CALL_METHOD | result obj method [args...] | 调用对象方法  |

## 关键实现细节

### 1. 变量管理

- 所有变量强制显式声明
- 所有变量强制手动类型转换，特殊指令除外
- 变量作用域通过SCOPE_BEGIN和SCOPE_END指令显式声明

### 2. 控制流实现

#### if-else 示例

```dovetail
if (cond_var) {
    # if块代码
} else {
    # else块代码
}
# 转换成ir层:
SCOPE_BEGIN(op='if_0', op=<StructureType.CONDITIONAL: 'conditional'>)
SCOPE_END()
SCOPE_BEGIN(op='else_0', op=<StructureType.CONDITIONAL: 'conditional'>)
SCOPE_END()
COND_JUMP(op=Variable(name='cond_var', dtype=<DataType.BOOLEAN: 'boolean'>, var_type=<VariableType.GENERAL: 'general'>), op='if_0', op='else_0')
```

#### 传统for循环示例

```dovetail
for (int i=0;i<3;i=i+1) {
    # 循环体
}
# 转换成ir层:
SCOPE_BEGIN(op='for_0', op=<StructureType.LOOP: 'loop'>)
    DECLARE(op=Variable(name='i', dtype=<DataType.INT: 'int'>, var_type=<VariableType.GENERAL: 'general'>))
    ASSIGN(op=Variable(name='i', dtype=<DataType.INT: 'int'>, var_type=<VariableType.GENERAL: 'general'>), op=Reference(value_type=<ValueType.LITERAL: 'literal'>, value=Literal(dtype=<DataType.INT: 'int'>, value=0)))
    SCOPE_BEGIN(op='for_0_check', op=<StructureType.LOOP_CHECK: 'loop_check'>)
        SCOPE_BEGIN(op='for_0_body', op=<StructureType.LOOP_BODY: 'loop_body'>)
            DECLARE(op=Variable(name='calc_1', dtype=<DataType.INT: 'int'>, var_type=<VariableType.GENERAL: 'general'>))
            OP(op=Variable(name='calc_1', dtype=<DataType.INT: 'int'>, var_type=<VariableType.GENERAL: 'general'>), op=<BinaryOps.ADD: '+'>, op=Reference(value_type=<ValueType.VARIABLE: 'variable'>, value=Variable(name='i', dtype=<DataType.INT: 'int'>, var_type=<VariableType.GENERAL: 'general'>)), op=Reference(value_type=<ValueType.LITERAL: 'literal'>, value=Literal(dtype=<DataType.INT: 'int'>, value=1)))
            ASSIGN(op=Variable(name='i', dtype=<DataType.INT: 'int'>, var_type=<VariableType.GENERAL: 'general'>), op=Reference(value_type=<ValueType.VARIABLE: 'variable'>, value=Variable(name='calc_1', dtype=<DataType.INT: 'int'>, var_type=<VariableType.GENERAL: 'general'>)))
            JUMP(op='for_0_check')
        SCOPE_END()
        DECLARE(op=Variable(name='bool_2', dtype=<DataType.BOOLEAN: 'boolean'>, var_type=<VariableType.GENERAL: 'general'>))
        COMPARE(op=Variable(name='bool_2', dtype=<DataType.BOOLEAN: 'boolean'>, var_type=<VariableType.GENERAL: 'general'>), op=<CompareOps.LT: '<'>, op=Reference(value_type=<ValueType.VARIABLE: 'variable'>, value=Variable(name='i', dtype=<DataType.INT: 'int'>, var_type=<VariableType.GENERAL: 'general'>)), op=Reference(value_type=<ValueType.LITERAL: 'literal'>, value=Literal(dtype=<DataType.INT: 'int'>, value=3)))
        COND_JUMP(op=Variable(name='bool_2', dtype=<DataType.BOOLEAN: 'boolean'>, var_type=<VariableType.GENERAL: 'general'>), op='for_0_body', op=None)           COND_JUMP(op=Variable(name='bool_2', dtype=<DataType.BOOLEAN: 'boolean'>, var_type=<VariableType.GENERAL: 'general'>), op='for_0_check', op=None)
    SCOPE_END()
SCOPE_END()
JUMP(op='for_0')
```

### 3. IR优化策略

1. **内存优化**：
    - 临时变量重用池
2. **性能优化**：
    - 常量折叠：`OP $t0 + 2 3` → `ASSIGN $t0 5`
    - 方法内联：`CALL_INLINE foo()` → 插入foo函数体

## IR转换示例

### 原始代码

```dovetail
func main() -> int {
    func add(a:int, b:int) -> int {
        return a + b
    }

    int r = add(1, 2);
    cmd(f"say ${r}")
}
```

### 生成IR

```dovetail
IROpCode.SCOPE_BEGIN(op='main', op=<StructureType.FUNCTION: 'function'>)
    IROpCode.SCOPE_BEGIN(op='add', op=<StructureType.FUNCTION: 'function'>)
        IROpCode.DECLARE(op=Variable(name='a', dtype=<DataType.INT: 'int'>, var_type=<VariableType.ARGUMENT: 'argument'>))
        IROpCode.DECLARE(op=Variable(name='b', dtype=<DataType.INT: 'int'>, var_type=<VariableType.ARGUMENT: 'argument'>))
        IROpCode.DECLARE(op=Variable(name='calc_0', dtype=<DataType.INT: 'int'>, var_type=<VariableType.RETURN: 'return'>))
        IROpCode.OP(op=Variable(name='calc_0', dtype=<DataType.INT: 'int'>, var_type=<VariableType.RETURN: 'return'>), op=<BinaryOps.ADD: '+'>, op=Reference(value_type=<ValueType.VARIABLE: 'variable'>, value=Variable(name='a', dtype=<DataType.INT: 'int'>, var_type=<VariableType.ARGUMENT: 'argument'>)), op=Reference(value_type=<ValueType.VARIABLE: 'variable'>, value=Variable(name='b', dtype=<DataType.INT: 'int'>, var_type=<VariableType.ARGUMENT: 'argument'>)))
        IROpCode.RETURN(op=Reference(value_type=<ValueType.VARIABLE: 'variable'>, value=Variable(name='calc_0', dtype=<DataType.INT: 'int'>, var_type=<VariableType.RETURN: 'return'>)))
    IROpCode.SCOPE_END()
    IROpCode.FUNCTION(op=Function(name='add', params=[Variable(name='a', dtype=<DataType.INT: 'int'>, var_type=<VariableType.ARGUMENT: 'argument'>), Variable(name='b', dtype=<DataType.INT: 'int'>, var_type=<VariableType.ARGUMENT: 'argument'>)], return_type=<DataType.INT: 'int'>))
    IROpCode.DECLARE(op=Variable(name='result_1', dtype=<DataType.INT: 'int'>, var_type=<VariableType.GENERAL: 'general'>))
    IROpCode.CALL(op=Variable(name='result_1', dtype=<DataType.INT: 'int'>, var_type=<VariableType.GENERAL: 'general'>), op=Function(name='add', params=[Variable(name='a', dtype=<DataType.INT: 'int'>, var_type=<VariableType.ARGUMENT: 'argument'>), Variable(name='b', dtype=<DataType.INT: 'int'>, var_type=<VariableType.ARGUMENT: 'argument'>)], return_type=<DataType.INT: 'int'>), op=[Reference(value_type=<ValueType.LITERAL: 'literal'>, value=Literal(dtype=<DataType.INT: 'int'>, value=1)), Reference(value_type=<ValueType.LITERAL: 'literal'>, value=Literal(dtype=<DataType.INT: 'int'>, value=2))])
    IROpCode.DECLARE(op=Variable(name='r', dtype=<DataType.INT: 'int'>, var_type=<VariableType.GENERAL: 'general'>))
    IROpCode.ASSIGN(op=Variable(name='r', dtype=<DataType.INT: 'int'>, var_type=<VariableType.GENERAL: 'general'>), op=Reference(value_type=<ValueType.VARIABLE: 'variable'>, value=Variable(name='result_1', dtype=<DataType.INT: 'int'>, var_type=<VariableType.GENERAL: 'general'>)))
    IROpCode.DECLARE(op=Variable(name='fstring_2', dtype=<DataType.STRING: 'string'>, var_type=<VariableType.GENERAL: 'general'>))
    IROpCode.DECLARE(op=Variable(name='fstring_3', dtype=<DataType.STRING: 'string'>, var_type=<VariableType.GENERAL: 'general'>))
    IROpCode.ASSIGN(op=Variable(name='fstring_3', dtype=<DataType.STRING: 'string'>, var_type=<VariableType.GENERAL: 'general'>), op=Reference(value_type=<ValueType.LITERAL: 'literal'>, value=Literal(dtype=<DataType.STRING: 'string'>, value='say $')))
    IROpCode.DECLARE(op=Variable(name='cast_4', dtype=<DataType.STRING: 'string'>, var_type=<VariableType.GENERAL: 'general'>))
    IROpCode.CAST(op=Variable(name='cast_4', dtype=<DataType.STRING: 'string'>, var_type=<VariableType.GENERAL: 'general'>), op=<DataType.STRING: 'string'>, op=Reference(value_type=<ValueType.VARIABLE: 'variable'>, value=Variable(name='r', dtype=<DataType.INT: 'int'>, var_type=<VariableType.GENERAL: 'general'>)))
    IROpCode.DECLARE(op=Variable(name='fstring_5', dtype=<DataType.STRING: 'string'>, var_type=<VariableType.GENERAL: 'general'>))
    IROpCode.OP(op=Variable(name='fstring_5', dtype=<DataType.STRING: 'string'>, var_type=<VariableType.GENERAL: 'general'>), op=<BinaryOps.ADD: '+'>, op=Reference(value_type=<ValueType.VARIABLE: 'variable'>, value=Variable(name='fstring_3', dtype=<DataType.STRING: 'string'>, var_type=<VariableType.GENERAL: 'general'>)), op=Reference(value_type=<ValueType.VARIABLE: 'variable'>, value=Variable(name='cast_4', dtype=<DataType.STRING: 'string'>, var_type=<VariableType.GENERAL: 'general'>)))
    IROpCode.RAW_CMD(op=Reference(value_type=<ValueType.VARIABLE: 'variable'>, value=Variable(name='fstring_5', dtype=<DataType.STRING: 'string'>, var_type=<VariableType.GENERAL: 'general'>)))
IROpCode.SCOPE_END()
IROpCode.FUNCTION(op=Function(name='main', params=[], return_type=<DataType.INT: 'int'>))
```

## 优点

1. 保持指令简洁但表达能力完整
2. 便于进行各种优化(常量折叠、死代码消除等)
3. 支持高级语言特性到低级命令的转换

## 附录

### 参数类型定义表

#### 基础符号类 (Symbol)

```dovetail
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
    constants: set[Reference[Constant]]  # 常量引用集合
    variables: set[Reference[Variable]]  # 变量引用集合
    type: ClassType = ClassType.CLASS  # 类型（类/接口）
```

#### 常量定义 (Constant)

```python

@define(slots=True)
class Constant(Symbol):
    name: str  # 常量名
    dtype: DataType | Class  # 数据类型
    var_type: VariableType = VariableType.COMMON  # 变量类型
```

#### 函数定义 (Function)

```python
@define(slots=True)
class Function(Symbol):
    name: str  # 函数名
    params: list[Parameter]  # 参数列表
    return_type: DataType | Class  # 返回类型
    function_type: FunctionType = FunctionType.FUNCTION  # 函数类型
```

#### 字面量定义 (Literal)

```python
@define(slots=True, frozen=True)
class Literal(Symbol):
    dtype: DataType  # 数据类型
    value: str | int | bool | None  # 字面量值
```

#### 参数定义 (Parameter)

```python
@define(slots=True)
class Parameter(Symbol):
    var: Variable  # 参数变量
    optional: bool = False  # 是否可选
    default: Reference[Variable | Literal | Constant] = None  # 默认值
```

#### 引用定义 (Reference)

```python
\

@define(slots=True, hash=True)
class Reference(Symbol, Generic[T]):
    value_type: ValueType  # 引用值类型
    value: T  # 被引用的符号

    # 支持的引用类型：
    # ValueType.LITERAL - 字面量引用
    # ValueType.VARIABLE - 变量引用  
    # ValueType.CONSTANT - 常量引用
    # ValueType.FUNCTION - 函数引用
    # ValueType.CLASS - 类引用
```

#### 变量定义 (Variable)

```python
@define(slots=True)
class Variable(Symbol):
    name: str  # 变量名
    dtype: DataType | Class  # 数据类型
    var_type: VariableType = VariableType.COMMON  # 变量类型
```

#### 枚举类型说明

**ValueType 枚举：**

- `LITERAL`: 字面量
- `VARIABLE`: 变量
- `CONSTANT`: 常量
- `FUNCTION`: 函数
- `CLASS`: 类

**DataType 枚举：**

- `INT`: 整数类型
- `STRING`: 字符串类型
- `BOOLEAN`: 布尔类型
- `NULL`: 空类型
- `Function`: 函数类型(不保证使用)

**VariableType 枚举：**

- `COMMON`: 普通变量
- `PARAMETER`: 函数参数
- `RETURN`: 返回值

**FunctionType 枚举：**

- `FUNCTION`: 普通函数
- `BUILTIN`: 内置函数
- `METHOD`: 类方法
- `LIBRARY`: 库函数