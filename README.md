# Dovetail

> Minecraft数据包编译语言 | 面向对象的Minecraft DSL  
> 该项目部分参考了[MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP)
> 该项目的实现不够成熟，若需要生产环境使用，请考虑其他相对成熟的项目    
> 关于自举: 绝对不会考虑
<!-- 把史放github上我真是个天才 -->

## 目标

- [ ] 一次编写，处处编译(
- [ ] 面对对象支持
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
Q: wtf?编译器为什么提示未知的错误?如何解决?  
A: 你可以在github上开启一个issue提交这个问题  
Q: 明明我的代码没有错误，生成出的指令却无法正确执行  
A: 请先尝试添加参数 `-O0` ，若是再次生成的指令正确执行，请以`ir优化错误`为issue标题前缀,否则以`未知错误`作为标题前缀    
Q: 生成出来的指令执行到一半就中止  
A: 请尝试使用gamerule指令适当提高maxCommandChainLength规则的数量
Q: 如果我必须要用堆栈呢
A: 可以采用其他项目，如[MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP)

## 许可证

本项目采用 Apache 2.0 授权
