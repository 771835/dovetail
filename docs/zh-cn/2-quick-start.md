# 快速开始

## 环境要求

- **Python 3.11+**（支持且推荐使用 PyPy）
- **Minecraft Java Edition 1.21.5**（默认目标版本）
- Git

## 安装

### 方式一：从源码安装（推荐）

```bash
git clone https://github.com/771835/dovetail.git
cd dovetail
pip install -r requirements.txt

# 验证安装
python main.py --version
```

依赖项：`attrs`、`fastjsonschema`、`requests`、`lark`

### 方式二：下载预编译版本

访问 [Releases 页面](https://github.com/771835/dovetail/releases) 下载。目前存在 **1.0.0**
版本的历史发行版。注意旧版本与当前文档描述的语法及功能可能存在差异，建议优先使用源码安装以获取最新特性。

## 第一个程序

创建 `hello.mcdl`：

```mcdl
@init
fn main() {
    print("Hello, Minecraft!")
}
```

编译：

```bash
python main.py hello.mcdl -o output
```

这将在 `output/` 目录生成完整的数据包结构。

## 命令行参数完整参考

```
python main.py <input> [选项]
```

### 核心参数

| 参数                    | 简写     | 说明              | 默认值         |
|-----------------------|--------|-----------------|-------------|
| `input`               | —      | 输入文件或目录路径       | （必需）        |
| `--output`            | `-o`   | 输出目录路径          | `target`    |
| `--namespace`         | `-n`   | 输出数据包命名空间       | `namespace` |
| `--minecraft-version` | `-mcv` | 目标 Minecraft 版本 | `1.21.5`    |
| `-O`                  | —      | 优化级别（0/1/2/3）   | `2`         |

### 路径与后端

| 参数           | 简写   | 说明        | 默认值    |
|--------------|------|-----------|--------|
| `--lib-path` | `-l` | 强制指定标准库路径 | `lib/` |
| `--backend`  | `-b` | 强制指定后端名称  | 自动选择   |

### 功能开关

| 参数                              | 说明                             |
|---------------------------------|--------------------------------|
| `--recursion`                   | 启用递归函数调用（需后端支持）                |
| `--same-name-function-nesting`  | 启用同名函数嵌套                       |
| `--disable-deprecated-function` | 禁用已弃用函数的编译                     |
| `--experimental`                | 启用实验性功能（如 `@extern`/`@export`） |
| `--disable-names-normalize`     | 禁用命名规范化                        |
| `--disable-plugins`             | 禁用插件加载                         |

### 调试与输出

| 参数                                | 说明                    |
|-----------------------------------|-----------------------|
| `--debug`                         | 打印 AST 结构、最终 IR 及详细日志 |
| `--no-generate-commands` / `-ngc` | 仅编译，不生成最终指令文件         |
| `--output-temp-file`              | 输出中间文件（`.mcdc`）       |
| `--version`                       | 显示版本、许可证及已注册后端        |

### 环境变量

| 变量                  | 说明                         |
|---------------------|----------------------------|
| `DOVETAIL_LIB_PATH` | 标准库路径（`--lib-path` 未指定时生效） |

## 目录编译

当输入路径为目录时，需在目录下提供 `pack.config` 文件：

```json
{
  "main": "main.mcdl",
  "description": "我的数据包"
}
```

`main` 字段为必需，指定入口文件相对路径。

## 常用编译示例

```bash
# 基本编译，输出到 target/
python main.py hello.mcdl

# 指定输出目录和命名空间
python main.py hello.mcdl -o my_datapack -n my_namespace

# 关闭优化（调试用）
python main.py hello.mcdl -O 0

# 指定 Minecraft 版本
python main.py hello.mcdl -mcv 1.21.5

# 启用调试模式（输出 AST 和 IR）
python main.py hello.mcdl --debug

# 仅语法检查，不生成文件
python main.py hello.mcdl -ngc
```

## 下一步

- [语言语法与 MCDL 基础](3-language-syntax-and-mcdl-basics) — 学习完整语法
- [编译配置参考](22-compile-configuration-reference) — 详细配置说明
