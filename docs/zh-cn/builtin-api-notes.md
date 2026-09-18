# 内置功能及 API 杂项
> 本页为松散记录，内容未经系统整理，完整性与时效性不被保证。
> 部分内容可能会被选入调试指南
> 本页主要为一些内置的功能，使用可能存在风险

### 将类实例转换为结构体的实例

当类本身存在`__struct__`属性时无效，且转换后对结构体实例的修改不会影响到类实例。
> 仅建议在优化中使用

```dovetail
let struct_obj = obj.__struct__; 
```

### 代码中取命名空间名及游戏版本

内置提供 `__namespace__` 和 `__minecraft_version__`。

```dovetail
print(__namespace__)
print(__minecraft_version__)
```

### 对常量字符串进行命名修饰

内置函数 `__builtin_name_decorate__` 和 `__builtin_name_undecorate__` 两函数允许在编译期修饰及反修饰一个字面量字符串

### 手动跳转作用域

内置函数 `_call` 函数允许通过写作用域名手动跳转到其他作用域。
> 无法被优化pass识别，有很大概率出现问题

### 中国地区的 github 镜像分流

为编译器设置环境变量 `USED_MIRROR_GITHUB_CN=1` 即可，仅影响后端。
