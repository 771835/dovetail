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
```
JUMP <scope>                 # 无条件跳转
COND_JUMP <cond_var> <true_scope> [false_scope] # 条件跳转双目标
FUNCTION <name> [params...]  # 函数定义
RETURN [value]               # 返回值
CALL <func> [args...]        # 函数调用
CALL_INLINE <func> [args...] # 函数调用(内联提示)
SCOPE_BEGIN <name> <type>    # 作用域开始标记
SCOPE_END <name>             # 作用域结束标记
LOOP_BEGIN <loop_id> [init] [cond] # 循环开始标记
LOOP_END <loop_id>           # 结束标记
BREAK <loop_id>              # 跳出指定循环
CONTINUE <loop_id>           # 继续下次迭代
```

### 变量操作
```
DECLARE <name> <type> [value] # 声明变量(含初始化)
DECLARE_TEMP <name> <type> [value] # 声明临时变量
VAR_RELEASE <name>  # 显式释放变量资源
ASSIGN <target> <source>      # 赋值操作
UNARY_OP <result> <op> <operand> # 一元运算
OP <result> <op> <left> <right> # 二元运算
COMPARE <result> <op> <left> <right> # 比较运算
```
### 面向对象指令
``` 
CLASS <name> <annotation> [extends] [implements...] [method...] # 声明类
NEW_OBJ <result> <class> [args...] # 对象实例化
GET_FIELD <result> <obj> <field>   # 获取字段
SET_FIELD <obj> <field> <value>    # 设置字段
CALL_METHOD <result> <obj> <method> [args...] # 方法调用
```

### 命令生成指令
```
RAW_CMD <command_string>      # 原始命令输出
FSTRING <result> <fstring>    # 插值字符串处理
```
<!-- TODO:考虑将FSTRING拆分成多指令 -->

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
#### for循环示例
```
for (int i=0;i<3;i++) {
    # 循环体
}
# 转换成ir层:

LOOP_BEGIN FOR_LOOP i=0          # 初始化 i=0
LOOP_COND FOR_LOOP i<3           # 条件 i<3
  # 循环体
  OP i + i 1                     # i++
LOOP_END FOR_LOOP

```

### 3. 方法调用优化
#### 方法调用转为
```
CALL_METHOD result_var player "getScore" args...
# 可优化为
GET_FIELD temp_var player "scores"
GET_FIELD result_var temp_var "value"
```

### 4. ir优化:
1. 内存优化:
   1. 作用域结束自动释放局部变量
2. 性能优化:
   1. 常量折叠
   2. 方法调用内联
   3. 分支预测
   4. 分析RAW_CMD指令
   5. 预存储常用的常量

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
