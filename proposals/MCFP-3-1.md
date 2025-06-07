### McFuncDSL 到 Minecraft Commands 的编译思路 (基于 Visitor 模式和 Scoreboard/NBT Storage)
    警告:该文章可能过时或与实际代码实现不同
    警告:该文章可能使用ai编写
编译过程本质上是将抽象语法树 (AST) 遍历，根据不同的语言构造（变量声明、表达式、控制流、函数等）生成对应的 Minecraft 命令。为了在 MC 环境中模拟变量和数据类型，我们采用了 Scoreboard 和 NBT Storage 结合的方式。

**核心组成部分和它们的作用：**

1.  **ANTLR 解析器和 AST:**
    *   `McFuncDSLLexer` 和 `McFuncDSLParser` 负责词法分析和语法分析，将源代码转化为一棵抽象语法树 (AST)。
    *   每个语法规则对应 AST 中的一个节点类型 (`ParserRuleContext`)。

2.  **Visitor 模式 (`McFuncDSLVisitor` 和 `MCGenerator`)：**
    *   `MCGenerator` 继承自 ANTLR 生成的 `McFuncDSLVisitor`。
    *   Visitor 模式允许我们遍历 AST。每个 `visit<RuleName>` 方法对应处理 AST 中特定类型的节点。
    *   在 `visit` 方法中，我们根据 DSL 语法规则的语义，生成相应的 Minecraft 命令，并将其添加到当前作用域的命令列表中。

3.  **作用域管理 (`Scope` 类)：**
    *   Minecraft Function Pack 是基于文件的，每个文件就是一个函数。DSL 中的作用域（函数、代码块、类、循环、条件语句）需要映射到 MC 的函数文件结构。
    *   `Scope` 类构建了一个作用域的树形结构：每个作用域有一个父级 (`parent`) 和多个子级 (`children`)。
    *   `Scope` 负责维护一个 **符号表 (`symbols`)**，存储在该作用域内声明的变量、函数、类等信息。
    *   `Scope` 存储该作用域块需要生成的 Minecraft 命令列表 (`cmd`)。
    *   `Scope` 具有生成 **唯一名称 (`get_unique_name`)** 的能力，这个唯一名称是基于其在作用域树中的层级和其局部名称生成的（例如 `global_main_for_0_body_0`）。这个唯一名称用于生成对应的 `.mcfunction` 文件路径和 NBT Storage 路径，确保命名不冲突。
    *   `_enter_scope` 和 `_exit_scope` 辅助方法用于在 AST 遍历时管理当前所处的编译作用域。

4.  **符号表 (`Symbol` 类)：**
    *   `Symbol` 类代表 DSL 代码中的一个命名实体（变量、函数、类）。
    *   它存储了符号的名称 (`name`)、类型 (`symbol_type`) 和数据类型 (`data_type`)。
    *   **关键点：** 为了支持 Scoreboard 和 NBT，`Symbol` 被扩展以存储变量在 **运行时** 的信息：
        *   `storage_location`: 指示变量的值是存储在 `SCOREBOARD` 还是 `NBT` (或 `SELECTOR`)。
        *   `scoreboard_name`: 如果存储在 Scoreboard，这是对应的玩家名（其实是Scoreboard的key）。
        *   `nbt_path`: 如果存储在 NBT，这是在 `mcfdsl:storage` 中的具体路径。
    *   `resolve_symbol` 方法在当前作用域及其父级作用域链中查找指定名称的符号。

5.  **表达式结果表示 (`Result` 类)：**
    *   `Result` 类用于表示 **表达式求值** 的结果。它不是语法树节点，而是 AST 遍历时从子节点向上返回的信息载体。
    *   它包含：
        *   `type_`: 表达式结果的 **运行时数据类型** (例如 `Type.TYPE_INT`, `Type.TYPE_STRING`, `Type.TYPE_BOOLEAN`, `Type.TYPE_SELECTOR`)。
        *   `value`: 仅用于表示 **编译期字面量** 的值。
        *   `storage_location`: 表达式结果在 **运行时** 存储在哪里 (`LITERAL`, `SCOREBOARD`, `NBT`, `SELECTOR`, `VOID`, `SYMBOL_REF` 等)。
        *   `runtime_id`: 如何在 **运行时** 引用这个结果（ Scoreboard 玩家名，NBT 路径，或 Selector 字符串等）。
        *   `Error`: 标记是否有错误。
    *   例如，访问变量 `myVar` (`visitVarExpr`) 会返回一个 `Result`，其 `type_` 是 `myVar` 的数据类型，`storage_location` 是 `myVar` 的存储位置 (`SCOREBOARD` 或 `NBT`)，`runtime_id` 是 `myVar` 在 Scoreboard 或 NBT 中的具体标识符。访问数字字面量 `10` (`visitLiteral`) 会返回 `Result(Type.TYPE_INT, 10, StorageLocation.LITERAL, None, False)`。

6.  **变量存储和赋值 (`visitVarDeclaration`, `visitAssignment`)：**
    *   变量声明 (`varDecl`) 时，根据声明的类型和初始化值，决定变量是存储在 Scoreboard (INT, BOOLEAN) 还是 NBT (STRING)。在符号表中创建对应的 `Symbol`，并生成 Scoreboard `set` 或 NBT `data modify set value` 命令进行初始化。Scoreboard 变量使用作用域的唯一名前缀确保唯一性。NBT 变量使用作用域的唯一名作为路径前缀。
    *   变量赋值 (`assignment`) 是一个复杂的操作，它需要根据目标变量 (`Symbol`) 的存储位置和右侧表达式 (`Result`) 的存储位置生成不同的 Minecraft 命令：
        *   Scoreboard = Literal: `scoreboard players set ...`
        *   Scoreboard = Scoreboard: `scoreboard players operation ... = ...`
        *   Scoreboard = NBT (限 int/byte NBT): `execute store result score ... run data get storage ...`
        *   NBT = Literal: `data modify storage ... set value ...`
        *   NBT = Scoreboard (限 int/bool SB -> int/byte NBT): `execute store result storage ... int 1 run scoreboard players get ...`
        *   NBT = NBT: `data modify storage ... set from storage ...`
        *   Selector = Selector (限 Literal): 仅更新符号表的 `runtime_id`，不生成运行时命令。
    *   这个过程包含了类型兼容性检查和隐式转换处理 (int/bool)。

7.  **表达式求值 (`visitAddSubExpr`, `visitCompareExpr`, 等)：**
    *   Minecraft 原生只支持 Scoreboard 上的算术和比较操作。
    *   表达式的 visitor 方法会递归调用子表达式的 visit 方法，获取子表达式的 `Result`。
    *   **关键辅助方法 (`_ensure_scoreboard`)：** 如果一个操作数不在 Scoreboard 中（例如是 NBT 变量或非整数字面量），`_ensure_scoreboard` 会生成临时的 Scoreboard 变量，并生成 `execute store result data get` (NBT -> SB) 或 `scoreboard players set` (Literal -> SB) 命令，将值加载到这个临时 Scoreboard 变量中。然后返回一个指向这个临时 Scoreboard 变量的新 `Result`。
    *   所有 Scoreboard 操作（`scoreboard players operation`）都使用经过 `_ensure_scoreboard` 处理后的 Scoreboard 玩家名。
    *   运算或比较的结果存储在另一个临时的 Scoreboard 变量中，并返回一个指向它的 `Result`。

8.  **控制流 (`visitIfStmt`, `visitWhileStmt`, `visitForStmt`)：**
    *   条件判断 (if, while, for 的条件部分) 必须在 Scoreboard 上进行 (`execute if score` / `execute unless score`)。
    *   条件表达式的结果会通过 `_ensure_scoreboard` 加载或确保在 Scoreboard 中。
    *   这些语句的代码块 (if body, else body, while body, for body/update/check) 被编译成独立的 `mcfunction` 文件。
    *   通过在父函数中生成 `execute if/unless score ... run function ...` 命令，或者在循环函数内部通过 `function` 命令互相调用，来实现控制流跳转。`return` 命令用于提前退出函数/循环。

9.  **函数定义与调用 (`visitFunctionDecl`, `visitDirectFuncCall`)：**
    *   函数定义 (`functionDecl`) 创建一个新的函数作用域 (`ScopeType.FUNCTION`)，这个作用域对应一个独立的 `.mcfunction` 文件。
    *   参数通过固定的 Scoreboard 玩家名 (`arg0`, `arg1`, ...) 传递。函数定义时，参数被视为局部变量，生成命令将其从 `argN` Scoreboard 复制到函数内部的局部 Scoreboard 变量。
    *   返回值（目前限 int/bool）通过固定的 `return` Scoreboard 玩家名返回。
    *   函数定义会在其父作用域中注册一个 `Symbol(SymbolType.FUNCTION)`，其中存储了函数的 MC 函数路径 (`get_minecraft_function_path`)。
    *   函数调用 (`directFuncCall`) 时，通过 `resolve_symbol` 查找函数符号获取其 MC 函数路径。生成命令将参数值（通过 `_ensure_scoreboard` 处理）赋值到 `argN` Scoreboard。然后生成 `function <func_path>` 命令调用函数。调用后，如果函数有返回值，则生成命令将 `return` Scoreboard 的值复制到调用方的临时 Scoreboard 变量中，并返回指向该临时变量的 `Result`。

10. **FString 处理 (`_process_fstring`)：**
    *   cmd 表达式或字符串字面量中的 FString (`f"..."`) 在 **编译期** 进行插值。
    *   它通过查找符号表，将 `${symbolName}` 替换为符号的 **编译期已知值** (如字面常量的值)。
    *   运行时变量 (Scoreboard 或 NBT) 的当前值在编译期是未知的，因此不能通过这种方式直接插值。需要在 Minecraft 命令中通过 `tellraw` 或 `execute` 的 NBT/score component 来引用。

11. **代码生成 (`_generate_commands`)：**
    *   遍历编译完成的 Scope 树。
    *   对于每个包含命令的 Scope，根据其唯一名称生成对应的 `.mcfunction` 文件路径，并写入收集到的命令。

**总结：**

整个思路是利用 ANTLR visitor 遍历 AST，并结合 Scoreboard 和 NBT Storage 作为 Minecraft 的运行时"内存"。通过 `Symbol` 和 `Result` 对象追踪变量的类型和存储位置，并在生成命令时，根据操作的需求（尤其是 Scoreboard 强制要求整数操作），利用临时的 Scoreboard 变量和 `execute store` 等命令在 Scoreboard 和 NBT 之间移动数据，从而模拟更丰富的数据类型支持。控制流则通过生成独立的函数文件和 `function` / `return` / `execute if/unless` 命令来实现。

这种方法的主要复杂性在于：
*   需要仔细管理 Scoreboard 和 NBT 变量的唯一命名（依赖作用域路径）。
*   Scoreboard 和 NBT 之间的类型转换和数据移动需要生成多条命令。
*   字符串操作、复杂类型（如类实例映射到 NBT）的实现需要更复杂的命令模式。
*   编译期插值 (`f""`) 和运行时引用 (`tellraw` NBT/score component) 的区分和正确使用。

虽然实现复杂，但这是一种将高级语言编译到 Minecraft 环境中相对可行的方法。希望这个思路解释能帮助你理解代码结构和其中的权衡。
