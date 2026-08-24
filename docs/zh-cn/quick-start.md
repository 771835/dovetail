# 快速开始指南

## 第零步：确认环境

### 操作系统兼容性

| 操作系统 | 最低版本             | 说明                                                                     |
|----------|----------------------|--------------------------------------------------------------------------|
| Windows  | **10 / Server 2016** | Python 3.9+ 已放弃 Windows 7/8/8.1 支持；Python 3.12+ 仅支持 Windows 10+ |
| macOS    | **10.9+**            | Python 3.11 官方支持 macOS 10.9+，但 Apple Silicon (M1+) 建议 macOS 12+  |
| Linux    | 无硬性底线           | 需 glibc 2.17+（CentOS 7+、Ubuntu 14.04+ 等）                            |

> **Windows 7 / 8 / 8.1 用户注意：** Python 3.9 起已移除对这几个系统的支持。Dovetail 要求 Python 3.11+，因此
> **这些系统无法运行**。这不是 Dovetail 的限制，而是 Python 本身的决定。

> **二进制构建（见下文）额外要求：** Nuitka 打包的 `.exe` 仅面向 64 位 Windows，且依赖目标系统的
> Runtime。如果你在老旧系统上运行二进制报错，优先改用 Git 源码方式。

### 运行时依赖

| 依赖                   | 要求                  | 如何确认               |
|------------------------|-----------------------|------------------------|
| Python                 | 3.11 或更高           | `python --version`     |
| Minecraft Java Edition | 1.21.5                | 游戏主菜单右下角版本号 |
| pip 依赖               | 见 `requirements.txt` | 安装时自动处理         |

`requirements.txt` 中包含的关键依赖：

- `lark` — 解析器引擎（Lark）
- `fastjsonschema` — 配置文件校验
- `attrs` — 数据类
- `requests` — 网络请求（下载工具等）
- `tomli` — TOML 解析（仅 Python < 3.11 需要；3.11+ 使用标准库 `tomllib`）

### Python 版本问题

**Python 版本过低**

```
SyntaxError: invalid syntax  （在合法的导入语句或其他语法处报错）
```

Dovetail 使用了 Python 3.11 引入的语法特性（如 `match` 语句、`Self` 类型、`tomllib` 标准库等），低版本解释器会在导入阶段崩溃。

**解决：** 安装 Python 3.11+。如果你系统上有多个版本共存，用 `python3.11` 或 `python3.12` 显式调用。

**Python 版本确认方式：**

```bash
python --version
# 或
python3 --version
```

---

## 第一步：获取 Dovetail

你有两种方式获取 Dovetail： **Git 源码方式**和 **二进制构建方式**。选哪种取决于你的需求。

### 方式 A：Git 源码（推荐）

适合想阅读源码、二次开发或需要跨平台运行的用户。

```bash
git clone https://github.com/771835/dovetail.git
cd dovetail
pip install -r requirements.txt
```

**验证安装：**

```bash
python main.py --version
```

正常输出类似：

```
The version of Dovetail is dev

License: Apache 2.0
Repository: https://github.com/771835/dovetail
OptimizationPass:
    [1] Constant Folding Pass (constant_folding)
    ...
Backends:
    je1215
```

如果你看到了优化pass列表和后端列表，说明安装成功。
> 直接 git 的版本号显示为`dev`是正常现象，可通过 `python ./scripts/gen_version.py` 生成具体的版本信息

### 方式 B：二进制构建（Windows 64 位）

适合不想配置 Python 环境、只需要编译功能的 Windows 用户。

项目提供了 `build.bat` 脚本，使用 [Nuitka](https://nuitka.net/) 将 Python 代码编译为独立的 `.exe`。

```bash
# 前置：安装 Nuitka
pip install nuitka

# 执行构建
build.bat
```

构建完成后，`build/main.dist/` 目录中会生成独立的 `dovetail.exe` 和 `dovetail-build.exe` 及其依赖。脚本还会自动复制
`plugins/`、`lark/`、
`examples/`、`LICENSE`、`NOTICE` 等必要文件。

**使用方式：**

```bash
dovetail.exe examples/example1.mcdl -o target
dovetail.exe --version
```

### 两种方式的对比

|            | Git 源码                  | 二进制构建                      |
|------------|---------------------------|---------------------------------|
| 平台       | Windows / macOS / Linux   | 仅 Windows 64 位                |
| 前置要求   | Python 3.11+ + pip 依赖   | 无（exe 自包含）                |
| 启动速度   | 较慢（Python 解释器）     | 较快（编译为原生代码）          |
| 可修改性   | ✅ 可阅读和修改源码       | ❌ 需要从源码重新构建           |
| 构建复杂度 | 低（clone + pip install） | 高（需安装 Nuitka 和 C 编译器） |
| 适合场景   | 开发、调试、跨平台        | 分发、纯使用                    |

### 安装阶段常见问题

**`pip install` 报错 `lark` 或其他包找不到**

可能原因：pip 源问题或网络问题。

**解决：** 尝试切换 pip 镜像源（中国大陆）：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**`--version` 输出中 Backends 列表为空**

后端是作为插件加载的，如果插件加载失败，编译器将无法生成数据包。

**解决：** 确认 `/plugins/` 目录存在且其他存在后端插件（如：`je1215`）。如果被误删或损坏，重新安装（第三方插件）或`git clone`
（项目自带的插件）即可。

**`--version` 报 `ModuleNotFoundError`**

某个依赖包未安装成功。

**解决：** 重新运行 `pip install -r requirements.txt`，确认所有包安装成功无跳过。

**`--version` 报 `ImportError: 请在 Python < 3.11 环境下安装 tomli 库`**

插件加载器需要 TOML 解析能力。Python 3.11+ 自带 `tomllib`；更低版本需要 `tomli` 包。

**解决：** 安装 `tomli`：

```bash
pip install tomli
```

或升级到 Python 3.11+。

**二进制构建：`build.bat` 报错 `nuitka 不是内部命令`**

Nuitka 未安装。

**解决：**

```bash
pip install nuitka
```

**二进制构建：Nuitka 报错找不到 C 编译器**

Nuitka 需要 C 编译器来生成原生代码。通常会自动下载 C 编译器，可能需要较长时间。

**二进制构建：`build.bat` 后 `dovetail.exe` 找不到标准库或插件**

`build.bat` 中 `--include-data-dir=lib=lib` 会将 `lib/` 目录打包进二进制。但如果 `lib/` 在构建时不存在或为空，编译时会报标准库路径错误。

**解决：** 确保在 **项目根目录**下运行 `build.bat`，且 `lib/` 目录存在。构建脚本会通过 `xcopy` 复制插件和示例，但如果目录结构有变动，需手动更新
`build.bat` 中的路径。

---

## 第二步：编译你的第一个数据包（单文件模式）

最简单的方式是直接编译单个 `.mcdl` 文件：

```bash
python main.py examples/example1.mcdl -o target
```

这会将 `example1.mcdl` 编译为 Minecraft 数据包，输出到 `target/` 目录。

### 一个最小的 Dovetail 程序

创建文件 `hello.mcdl`，写入：

```dovetail
include "minecraft.mcdl"

@init
fn main() {
    say("Hello, Minecraft!")
}
```

编译：

```bash
python main.py hello.mcdl -o target
```

### 你刚用到了什么

| 语法                       | 含义                                                                    |
|----------------------------|-------------------------------------------------------------------------|
| `include "minecraft.mcdl"` | 引入 Minecraft 标准库（提供 `say`、`kill` 等 Minecraft 原生指令的绑定） |
| `@init`                    | 标记此函数为数据包加载时自动执行的入口函数                              |
| `fn main()`                | 定义函数 `main`，无参数，无返回值                                       |
| `say("...")`               | 调用函数，等价于 Minecraft 的 `say` 命令                                |

### 更多语法速览

```mcdl
include "minecraft.mcdl"

// 带参数和返回值的函数
fn add(a: int, b: int) -> int {
    return a + b
}

// f-string 格式化输出
fn greet(name: string) {
    print(f"Hello, {name}!")
}

// 变量声明
@init
fn main() {
    let result = add(3, 7)
    print(f"3 + 7 = {result}")

    let counter = 0
    counter += 1

    // for 循环
    for (let i = 0; i < 5; i = i + 1) {
        print(f"i = {i}")
    }
}
```

### 单文件编译常见问题

**报错 `标准库路径 '...' 不存在或不是一个目录`**

编译器在寻找 `lib/` 目录（标准库），它默认在项目根目录下查找。

**解决：**

1. 确保你在 `dovetail/` 项目根目录下运行命令（`lib/` 应该在你当前目录或其子目录中）
2. 如果标准库在别处，用 `-l` 参数显式指定：
   ```bash
   python main.py hello.mcdl -l /path/to/lib -o target
   ```
3. 也可以设置环境变量 `DOVETAIL_LIB_PATH`：
   ```bash
   export DOVETAIL_LIB_PATH=/path/to/lib
   python main.py hello.mcdl -o target
   ```
4. **二进制构建用户注意：** 标准库已随 `lib/` 打包进 `build/main.dist/lib/`，需在 exe 同级目录下保留该文件夹

**报错 `0x9204: 文件 'xxx' 不存在`**

输入文件路径写错了。

**解决：** 检查路径拼写，确认文件存在。注意相对路径基于当前工作目录。

**报错 `0x100A: include 路径 'xxx' 格式错误或无效`**

`include` 的路径写错了或文件不存在。

**解决：** 检查 `include` 语句中的路径。注意：

- `"minecraft.mcdl"` 是标准库入口，无需写完整路径
- `"math"` 或 `"mathlib.mcdl"` 是标准库中的数学库
- 自定义文件使用相对路径，如 `"utils/helpers.mcdl"`

**报错 `0x100B: 检测到循环包含`**

两个或多个文件互相 `include` 形成了环。

**解决：** 拆分公共部分到独立文件，消除循环依赖。

**报错 `0x1005: 注解 '@xxx' 无效或不存在`**

使用了编译器不认识的注解。

**解决：** 目前支持的注解包括：

- `@init` — 入口函数
- `@target("java")` / `@target("be")` — 平台条件编译
- `#deprecated` — 标记弃用

其他注解拼写错误请更正。

**报错 `0x1011: 参数 'xxx' 缺少必要的类型注解`**

MCDL 要求函数参数必须标注类型。

**解决：** `fn foo(x)` → `fn foo(x: int)`

**报错 `0x1012: 带默认值的参数 'xxx' 必须在无默认值参数之后`**

默认参数位置错误。

**解决：** `fn foo(a: int = 0, b: int)` → `fn foo(b: int, a: int = 0)`

**报错 `0x1004: 标识符 'xxx' 重复定义`**

同一作用域内定义了同名符号。

**解决：** 重命名其中一个。

**报错 `没有找到适合该配置的合适后端` 或 `Backends` 列表为空**

后端插件未加载。后端（如 `je1215`）是插件，负责将 IR 翻译为 Minecraft 命令。

**解决：**

1. 确认没有使用 `--disable-plugins`（它会禁用所有插件， **包括后端**）
2. 确认 `dovetail/plugins/je1215/` 目录完整
3. 如果安装了第三方后端，用 `--backend <名称>` 指定：
   ```bash
   python main.py hello.mcdl --backend je1215 -o target
   ```
4. **二进制构建用户：** 确认 `plugins/` 目录被正确复制到了 exe 旁

---

## 第三步：理解命令行参数

```bash
python main.py <输入文件> [选项]
```

### 常用参数

| 参数                 | 默认值      | 含义                                             |
|----------------------|-------------|--------------------------------------------------|
| `-o <路径>`          | `target`    | 输出目录                                         |
| `-O <级别>`          | `2`         | 优化级别：`0`=关闭, `1`=基本, `2`=标准, `3`=激进 |
| `-mcv <版本>`        | `1.21.5`    | 目标 Minecraft 版本                              |
| `-n <命名空间>`      | `namespace` | 数据包命名空间                                   |
| `-b <后端名>`        | 自动选择    | 强制指定后端                                     |
| `-l <路径>`          | 自动查找    | 标准库路径                                       |
| `--debug`            | 关闭        | 调试模式，输出 IR 和详细日志                     |
| `--output-temp-file` | 关闭        | 输出 `.mcdo` 中间文件                            |
| `--recursion`        | 关闭        | 启用递归支持（需后端支持）                       |
| `--disable-plugins`  | 关闭        | 禁用所有插件（**包括后端！**）                   |

### 优化级别说明

| 级别   | 含义             | 风险                     |
|--------|------------------|--------------------------|
| `-O 0` | 无优化           | 无风险，用于排查优化 Bug |
| `-O 1` | 基本优化         | 低风险                   |
| `-O 2` | 标准优化（默认） | 一般安全                 |
| `-O 3` | 激进优化         | 可能引入错误，谨慎使用   |

> **重要：** 如果你的代码在 `-O 2` 或 `-O 3` 下行为异常，先用 `-O 0` 确认是否是优化器引入的 Bug。

### 参数相关常见问题

**`-O 3` 编译后数据包执行结果不对**

激进优化可能引入错误。

**解决：** 降级到 `-O 2` 或 `-O 0`。如果 `-O 0` 正确而 `-O 2`/`-O 3` 不正确，这是优化器 Bug，请提交 Issue
并以"代码优化错误"为标题前缀。

**`--disable-plugins` 后报"没有找到后端"**

`--disable-plugins` 禁用的是 **所有插件**，包括编译器内置的后端（`je1215`）和插件加载器（`plugin_loader`）。

**解决：** 除非你在排查第三方插件问题，否则不要使用 `--disable-plugins`。排查第三方插件时，改用 `--backend <名称>` 手动指定后端。

**`-mcv` 指定版本后报 `0x9001: 不支持的目标版本`**

编译器不支持你指定的 Minecraft 版本。

**解决：** 运行 `python main.py --version` 查看可用后端及其支持的版本范围。Dovetail 的版本支持策略是 **跟随最新版本**
，不会长期停留在旧版本。

---

## 第四步：项目构建模式（推荐）

单文件模式适合小型项目或实验，正式开发推荐如下项目结构组织代码。

### 项目结构

```
my_project/
├── dovetail.toml      # 项目配置清单
├── src/               # 源代码目录
│   └── main.mcdl      # 入口文件
├── hook/              # 构建钩子（可选）
│   ├── pre_build.py
│   └── post_build.py
├── lib/               # 本地库（可选）
└── build/             # 编译输出（自动生成）
    └── datapack/
```

### 如何创建项目

当使用二进制文件时， 直接执行 `dovetial-build init 项目名` 即可
通过 `git` 下载源码的，执行 `python .\build_main.py init`

### 构建钩子（可选）

钩子是在编译前后执行的 Python 脚本，用于自动化任务。

`hook/pre_build.py`（编译前清理输出目录）：

```python
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
output = root / "build" / "datapack"

if output.exists():
    shutil.rmtree(output)
print("[pre_build] Ready.")
```

`hook/post_build.py`（编译后列出输出文件）：

```python
from pathlib import Path

root = Path(__file__).resolve().parent.parent
output = root / "build" / "datapack"

print(f"[post_build] Output at {output}")
for f in sorted(output.rglob("*")):
    print(f"  {f.relative_to(output)}")
```

### 编译项目

```bash
python main.py build .
```

这会读取当前目录的 `dovetail.toml`，调用构建插件完成编译。

> **二进制构建用户：** 将 `python main.py` 替换为 `dovetail.exe`，其余参数不变。但注意二进制模式下 `build .` 命令的工作目录是
> exe 所在目录，需确保 `dovetail.toml` 在正确位置。

---

## 第五步：安装数据包到 Minecraft

编译完成后，你得到的是一个标准的 Minecraft 数据包目录。接下来要让它进入游戏。

### 安装步骤

1. 找到你的 Minecraft 存档目录：
    - Windows: `%APPDATA%\.minecraft\saves\<世界名>\`
    - Linux: `~/.minecraft/saves/<世界名>/`
    - macOS: `~/Library/Application Support/minecraft/saves/<世界名>/`
    - 或者你所使用的启动器设置的位置 

2. 将编译输出目录（如 `target/` 或 `build/datapack/`） **整体**复制到存档的 `datapacks/` 文件夹中：
   ```
   saves/<世界名>/datapacks/<你的数据包名>/
   ├── pack.mcmeta
   ├── data/
   │   └── <命名空间>/
   │       └── functions/
   │           └── *.mcfunction
   └── ...
   ```

3. 在游戏内执行：
   ```
   /reload
   ```
   或重新进入世界。

4. 数据包中 `@init` 标记的函数会自动在加载时执行。

> **提示：** 如果不想反复复制文件，可以在编译时用 `-o` 参数直接指向存档的 `datapacks/` 目录下：
> ```bash
> python main.py hello.mcdl -o "%APPDATA%\.minecraft\saves\MyWorld\datapacks\hello"
> ```

### 安装阶段常见问题

**`/reload` 后提示"数据包加载失败"**

可能原因：

- 数据包目录结构不正确
- `pack.mcmeta` 缺失或格式错误
- 数据包格式版本与 Minecraft 版本不匹配

**解决：**

1. 确认你复制的是数据包的 **根目录**（包含 `pack.mcmeta` 的那个），而不是它的父目录
2. 检查 `pack.mcmeta` 中的 `pack_format` 是否与你的 Minecraft 版本匹配（1.21.5 对应特定 pack_format 值）
3. 用 `/datapack list` 查看数据包是否被识别

**数据包加载成功但函数不执行**

`@init` 函数应该在加载时自动运行。如果没有：

**解决：**

1. 用 `/function <命名空间>:main` 手动调用，确认函数本身能执行
2. 检查 `data/<命名空间>/tags/functions/load.json` 是否包含入口函数（编译器应自动生成）
3. 如果标签文件缺失，可能是后端生成 Bug，尝试 `-O 0` 重新编译

**游戏内执行函数时报 `Unknown function`**

函数路径拼错或命名空间不对。

**解决：** 命令格式为 `/function <命名空间>:<函数路径>`。命名空间由 `-n` 参数或 `dovetail.toml` 的 `[package].name` 决定。

**命令执行中止（未完整运行）**

Minecraft 默认的 `maxCommandChainLength` 为 65536，复杂程序可能超限。

**解决：**

```
/gamerule maxCommandChainLength 2147483647
```

**数据包在游戏内执行结果与预期不符**

可能是编译器优化引入的错误。

**解决：** 用 `-O 0` 重新编译，对比行为。如果 `-O 0` 正确而高优化级别不正确，是优化器 Bug——请提交 Issue。
