# Dovetail

[English Version](README_EN.md) | [中文版本](README.md)

> Minecraft数据包编译语言 | 面向对象的Minecraft DSL  
> 该项目部分参考了[MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP)
> 该项目的实现不够成熟，若需要生产环境使用，请考虑其他相对成熟的项目    
> 关于自举: 暂时不会考虑
<!-- 把史放github上我真是个天才 -->

## 目标

- [ ] 一次编写，处处编译(
- [x] 面对对象支持
- [ ] 完善的依赖库，不用手写指令
- [ ] 更低学习曲线

## 部署

### 环境要求

- Python 3.10+

### 快速开始

```bash
git clone https://github.com/771835/dovetail.git
cd dovetail
pip install -r requirements.txt
python main.py -O2 xxx.mcdl
```

## FAQ

Q: 为什么不支持递归?  
A: 递归需要运行时维护栈帧，在Mc中实现非常繁琐复杂，因此你应当将递归改写成迭代实现  
Q: 有很多技术可以处理递归，如CPS+TRO，为什么不使用  
A: 因为技术所限，以及作者本身精力有限  
Q: 编译器为什么提示未知的错误并给出了堆栈信息?如何解决?  
A: 你可以在github上开启一个issue提交这个问题  
Q: 明明我的代码没有错误，生成出的指令却无法正确执行  
A: 请先尝试添加参数 `-O0` ，若是再次生成的指令正确执行，请以`ir优化错误`为issue标题前缀,否则以`未知错误`作为标题前缀    
Q: 生成出来的指令执行到一半就中止  
A: 请尝试使用gamerule指令适当提高maxCommandChainLength规则的数量

## 许可证

本项目采用 Apache 2.0 授权

## 鸣谢

### 参与测试

- 4424 在项目前期发现了诸多bug并提出了大量具有建设性的意见

### 代码使用

- 项目[fast_integer_sqrt](https://github.com/Triton365/fast_integer_sqrt) 快速整数开方

### 思路来源/大佬鸣谢

- 大佬[zmr-233](https://github.com/zmr-233/) 提出了cps变换的解决递归的思路
- 项目[MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP) 处理堆栈一条不同技术路线

