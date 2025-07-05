# McFuncDSL IR (Intermediate Representation) 设计

## IR设计目标

1. 作为AST和最终Minecraft命令之间的中间层
2. 支持观察者模式进行优化和转换
3. 低级化但不至于过度细分
4. 保留足够信息用于生成高效命令
5. 支持序列化和反序列化
6. 支持作为库被使用而不需分发原始代码

## IR基本指令集

### 控制流指令

| 指令          | 参数                                    | 备注                  |
|-------------|---------------------------------------|---------------------|
| JUMP        | <scope>                               | 无条件跳转到指定作用域         |
| COND_JUMP   | <cond_var> <true_scope> [false_scope] | 条件跳转到作用域（提供双目标）     |
| FUNCTION    | <func>                                | 函数定义                |
| RETURN      | [value]                               | 从函数返回（可选返回值）        |
| CALL        | <result> <func> [args...]             | 函数调用                |
| CALL_INLINE | <result> <func> [args...]             | 函数内联调用提示（建议编译器优化）   |
| SCOPE_BEGIN | <name> <type>                         | 作用域开始标记（可标记为函数、循环等） |
| SCOPE_END   | -                                     | 作用域结束标记             |
| BREAK       | -                                     | 跳出指定循环              |
| CONTINUE    | -                                     | 终止当前循环迭代，继续下次迭代     |

### 变量操作

| 指令           | 参数                                   | 备注                    |
|--------------|--------------------------------------|-----------------------|
| DECLARE      | `<variable>`                         | 声明变量                  |
| DECLARE_TEMP | `<variable>`                         | 声明临时变量（自动生命周期管理）      |
| VAR_RELEASE  | `<name>`                             | 显式释放变量资源              |
| ASSIGN       | `<target>` `<source>`                | 赋值操作                  |
| UNARY_OP     | `<result>` `<op>` `<operand>`        | 一元运算（如 `-a`, `!b`）    |
| OP           | `<result>` `<op>` `<left>` `<right>` | 二元运算（如 `a+b`, `c*d`）  |
| COMPARE      | `<result>` `<op>` `<left>` `<right>` | 比较运算（如 `a>b`, `c==d`） |

### 面向对象指令

| 指令          | 参数                                        | 备注      |
|-------------|-------------------------------------------|---------|
| CLASS       | `<class>`                                 | 声明类结构   |
| NEW_OBJ     | `<result>` `<class>` `[args...]`          | 创建对象实例  |
| GET_FIELD   | `<result>` `<obj>` `<field>`              | 获取对象字段值 |
| SET_FIELD   | `<obj>` `<field>` `<value>`               | 设置对象字段值 |
| CALL_METHOD | `<result>` `<obj>` `<method>` `[args...]` | 调用对象方法  |

### 命令生成指令

| 指令      | 参数                     | 备注                   |
|---------|------------------------|----------------------|
| RAW_CMD | `<command_string>`     | 输出原生Minecraft命令      |
| FSTRING | `<result>` `<fstring>` | 插值字符串处理（编译时自动拆分为多指令） |

## 关键实现细节

### 1. 变量管理

- 所有临时变量显式声明
- 变量作用域通过SCOPE_BEGIN和SCOPE_END指令显式声明

### 2. 控制流实现

#### if-else 示例

```
if (cond_var) {
    # if块代码
} else {
    # else块代码
}
# 转换成ir层:
SCOPE_BEGIN IF_TRUE conditional
# if块代码
SCOPE_END IF_TRUE

SCOPE_BEGIN IF_FALSE conditional
# else块代码
SCOPE_END IF_FALSE

COND_JUMP cond_var IF_TRUE IF_FALSE


```

#### 传统for循环示例

```
for (int i=0;i<3;i++) {
    # 循环体
}
# 转换成ir层:
SCOPE_BEGIN LOOP loop
   DECLARE i int 0
   SCOPE_BEGIN LOOP_CHECK loop_check
      SCOPE_BEGIN LOOP_BODY loop_body
         # 循环体
         OP i + i 1
      SCOPE_END FOR_LOOP_BODY
      COMPARE $temp < i 3
      COND_JUMP $temp FOR_LOOP_BODY
      COND_JUMP $temp FOR_LOOP
   SCOPE_END LOOP_CHECK
SCOPE_END LOOP
```

### 3. 方法调用优化

#### 方法调用转为

```
CALL_METHOD result_var player "getScore" args...
# 可优化为
GET_FIELD temp_var player "scores"
GET_FIELD result_var temp_var "value"
```

### 4. IR优化策略

1. **内存优化**：
    - 作用域退出时自动释放局部变量
    - 临时变量重用池
2. **性能优化**：
    - 常量折叠：`OP $t0 + 2 3` → `ASSIGN $t0 5`
    - 方法内联：`CALL_INLINE foo()` → 插入foo函数体
    - 命令预计算：`RAW_CMD "say ${1+2}"` → `RAW_CMD "say 3"`

## IR转换示例

### 原始代码

```
func add(a:int, b:int) -> int {
    return a + b
}

cmd f"say ${add(1, 2)}"
```

### 生成IR

```
FUNCTION add a:int b:int
SCOPE_BEGIN add function
OP $t0 + a b
RETURN $t0
SCOPE_END add

# 主程序
DECLARE arg0 int 1
DECLARE arg1 int 2
CALL temp1 add arg0 arg1
FSTRING cmd_str "say ${temp1}"
RAW_CMD cmd_str
```

### 优化后IR

```
# 常量折叠优化后
FSTRING cmd_str "say 3"
RAW_CMD cmd_str
```

## 优点

1. 保持指令简洁但表达能力完整
2. 便于进行各种优化(常量折叠、死代码消除等)
3. 支持高级语言特性到低级命令的转换

## 附录

### 参数类型定义表

```
Literal:
    dtype: DataType
    value: Any
 
Variable:
    name: str
    dtype:  DataType|'Class'
    value: Any (可选)

Constant:
    name: str
    dtype:  DataType|'Class'
    value: Any (可选)

Function:
    name: str
    params: list[Variable]
    return_type:  DataType|'Class'


Class:
    name: str
    methods: list[Function]）
    interfaces: Optional[Class]
    parent: Optional[Class]
    constants: set[Reference[Constant]]
    variables: list[Reference[Variable]]

T = 'Variable','Constant','Literal','Function', 'Class'
Reference:
    value_type: ValueType
    value: T

```