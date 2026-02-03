# Dovetail

[English Version](README_EN.md) | [中文版本](README.md)

> Minecraft数据包编译语言 - 具有部分面向对象特性的解决方案
>
> **目前状态：**
> - **优点:** 语法基本可用，能够编译简单程序。
> - **已知局限:** 缺乏大量标准库、错误信息不友好、优化器可能引入Bug、尚未实现完整的OOP特性。
> - **生产环境建议:** 如果您需要用于生产环境，请考虑使用 [MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP)
    或其他更成熟的项目。

Dovetail 是一种具有面向对象特征的语言，可以编译成`Minecraft 数据包`(以下简称`数据包`)。它旨在将传统命令的过程导向改变为目标导向。

## 目标

- [ ] 一次编写，处处~~报错~~编译
- [ ] 基本面对对象支持
- [ ] 完善的依赖库，使开发者不直接面向指令
- [ ] 数据包开销降低
- [ ] 迭代版本跟上我的世界版本更新

## 中长期计划

- [ ] 通过使用前置数据包以提高安全性及性能
- [ ] 优化错误显示
- [x] 统一日志输出
- [ ] 完善插件api
- [ ] 提高优化效果
- [ ] 寻找尽量节省性能的堆栈实现方法
- [ ] 转译器国际化支持
- [ ] 转译器多线程优化
- [ ] 允许通过简单的语法声明和调用其他数据包
- [ ] 谓词，自定义数据等功能
- [ ] 函数一等公民化
- [ ] 简易事件系统及注解功能
- [ ] 完善内置库

## 快速开始

### 环境要求

- Python 3.10+
- Minecraft Java Edition 1.21.4+

### 快速开始

```bash
git clone https://github.com/771835/dovetail.git
cd dovetail
pip install -r requirements.txt
python main.py -O2 xxx.mcdl
```

## 示例

```mcdl
// 定义函数
func greet(name: string) {
    print(f"Hello, {name}");
}

// 主函数（使用@init注解）
@init
func main() {
    greet("World")
    greet("Bob")
}
```

## FAQ

Q: 为什么不支持递归?  
A: 递归需要运行时维护栈帧，在Minecraft中实现性能消耗较大。建议将递归算法改写成迭代实现。  
Q: 有技术可以解决递归，但是项目选择忽视?  
A: 因为技术所限，以及作者本身精力有限  
Q: 编译器为什么提示未知的错误并给出了堆栈信息?如何解决?  
A: 你可以在github上开启一个issue提交这个问题  
Q: 明明我的代码没有错误，生成出的数据包却无法正确执行  
A: 请尝试禁用代码优化，若生成的数据包正确执行，请以`代码优化错误`为issue标题前缀,否则以`未知错误`作为标题前缀      
Q: 为什么生成的数据包在执行时中止?  
A: 请尝试使用gamerule指令适当提高maxCommandChainLength规则的数量    
Q: 找不到可用后端怎么办?  
A: 安装对应后端插件

## 许可证

本项目采用 Apache 2.0 授权

这意味着您**可以**自由地将其用于个人或商业目的，无需我的直接许可。

同时，如果您在项目/产品中使用了本作品并从中获得了商业价值，我非常欢迎您通过以下方式予以认可：

- **注明来源**：在您的产品文档或在关于页面中提及本项目。
- **分享改进**：将您基于本项目所做的改进回馈给社区。
- **进行贡献**：欢迎提交代码、报告问题、改进文档或提出建议，共同让项目变得更好。

感谢您的支持！
<!-- 社区在哪？鬼知道 -->

## 鸣谢

### 参与测试

- 4424 在项目前期发现了诸多bug并提出了大量具有建设性的意见

### 代码使用

> 由于 `Minecraft` 版本的原因，实际使用时可能会对以下项目进行一定的必要修改。如果您希望您的项目不被使用或修改，请随时联系本项目作者讨论移除事宜。

- 项目[fast_integer_sqrt](https://github.com/Triton365/fast_integer_sqrt) 快速整数开方
<!--- 项目[DNT-Dahesor-NBT-Transformer](https://github.com/Dahesor/DNT-Dahesor-NBT-Transformer) 安全字符串拼接，NBT转JSON等SNBT与字符串操作-->
<!-- 由于dnt不支持1.21.4故不展示 -->
- 项目[StringLib](https://github.com/CMDred/StringLib) 提供了大量不安全但快速的字符串操作手段

### 数据使用

- [wiki数据包版本](https://zh.minecraft.wiki/w/Template:Data_pack_format) 动态更新`Minecraft`与`数据包版本`之间的对应关系

### 思路来源/大佬鸣谢

- 大佬[zmr-233](https://github.com/zmr-233/) 提出了解决递归问题的思路(虽然ta推荐的书我都没看)
- 项目[MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP) 处理堆栈一条不同技术路线(很优秀的一个项目)
- 项目[clang-mc](https://github.com/xia-mc/clang-mc) 十分创新的想法，实现汇编的在mc中的部分支持

