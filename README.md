# MCFDSL

> Minecraft数据包编译语言 | 面向对象的Minecraft DSL
> 该项目大部分参考了[MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP)，同时引入了部分新的语法和设计。但是，该项目最初并非由MCFPP启发而产生，仅为作者的想法而产生。


## ✨ 特性亮点
- 🧬 面向对象编程支持（类/接口/继承）(待实现)[NOTICE](NOTICE)
- 🧩 现代语法糖（注解系统、泛型、lambda表达式）
- ⚡ 实时命令编译（支持f-string插值）
- 🔄 流程控制（for/while循环、条件分支）
- 📦 模块化设计（支持import导入）

## 🛠️ 安装
### 环境要求
- Python 3.10+
- ANTLR4运行时

### 快速开始
```bash
git clone https://github.com/771835/mcfdsl.git
cd mcfdsl
pip install -r requirements.txt
python main.py xxx.mcdl
```

## 许可证
本项目采用 Apache 2.0 授权
