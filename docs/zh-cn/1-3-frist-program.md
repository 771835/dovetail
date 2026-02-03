# 第一个程序

创建 hello.mcdl 文件：

```dovetail
@init
func main() {
    print("Hello, Minecraft!");
}
```

编译并生成数据包：

```bash
python main.py hello.mcdl -o output
```

这将在 output 目录生成完整的数据包结构。

# 编译选项

```bash
# 基本编译
python main.py input.mcdl
 
# 指定输出目录
python main.py input.mcdl -o my_datapack
 
# 设置优化级别（0-3）
python main.py input.mcdl -O2
 
# 指定 Minecraft 版本
python main.py input.mcdl --minecraft_version 1.20.4
 
# 指定命名空间
python main.py input.mcdl -n my_namespace
 
# 启用调试模式
python main.py input.mcdl --debug
```

# 示例程序

## Hello World 增强版

```dovetail
@init
func main() {
    string playerName = "Steve";
    print(f"欢迎 {playerName} 来到我的世界!");
    
    // 给玩家一些物品
    exec(f"give {playerName} minecraft:diamond 5");
}
 
@tick
func gameLoop() {
    // 每 tick 执行的逻辑
    exec("scoreboard players add timer global 1");
}
```

类与对象示例

```
class Player {
    string name;
    int health;
    
    method __init__(Player self, string playerName) {
        self.name = playerName;
        self.health = 20;
    }
    
    method heal(Player self, int amount) {
        self.health = self.health + amount;
        if (self.health > 20) {
            self.health = 20;
        }
        print(f"{self.name} 治疗了 {amount} 点生命值");
    }
}
 
@init
func main() {
    Player steve = Player("Steve");
    steve.heal(steve, 5);
}
```

# 常见问题

Q: 编译时提示语法错误怎么办？
A: 检查语法是否正确，参考 基础语言语法 文档。

Q: 生成的指令在游戏中不执行？
A: 尝试使用 -O0 关闭优化，如果能正常执行则可能是优化器问题。

Q: 如何调试我的代码？
A: 使用 --debug 参数启用调试模式，查看详细的编译信息。

# 下一步

- [编译器架构与流水线](./2-1-compiler-architecture-and-pipeline) - 编译器架构与流水线简单描述