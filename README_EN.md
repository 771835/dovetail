# Dovetail

[English Version](README_EN.md) | [中文版本](README.md)

> Minecraft Datapack Compilation Language - A Solution with Partial Object-Oriented Features
>
> **Current Status:**
> - **Advantages:** Basic syntax is functional and capable of compiling simple programs.
> - **Known Limitations:** Lacks extensive standard library, unfriendly error messages, optimizer may introduce bugs, full OOP features not yet implemented.
> - **Production Environment Recommendation:** If you need this for production use, please consider [MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP) or other more mature projects.
> Due to technical limitations, no new feature implementations will be committed in the short term.

Dovetail is an object-oriented language that compiles into `Minecraft Datapacks` (hereinafter referred to as `datapacks`). It aims to transform traditional command-based procedural orientation into goal-oriented development.

## Goals

- [ ] Write once, ~~crash~~ compile everywhere
- [ ] Basic object-oriented support
- [ ] Comprehensive dependency libraries to shield developers from direct command manipulation
- [ ] Reduced datapack overhead
- [ ] Iterative versions keeping pace with Minecraft updates

## Mid to Long-term Plans

- [ ] Improve security and performance through prerequisite datapacks
- [ ] Optimize error display
- [x] Unified logging output
- [ ] Improve plugin API
- [ ] Enhance optimization effectiveness
- [ ] Find performance-efficient stack implementation methods
- [ ] Transpiler internationalization support
- [ ] Transpiler multi-threading optimization
- [ ] Allow declaration and invocation of other datapacks through simple syntax
- [ ] Predicates, custom data, and other features
- [ ] First-class function citizens
- [ ] Simple event system and annotation functionality
- [ ] Improve built-in library

## Quick Start

### Requirements

- Python 3.10+
- Minecraft Java Edition 1.21.4

### Getting Started

```bash
git clone https://github.com/771835/dovetail.git
cd dovetail
pip install -r requirements.txt
python main.py -O2 xxx.mcdl
```

## Example

```mcdl
// Define function
func greet(name: string) {
    print(f"Hello, {name}");
}

// Main function (using @init annotation)
@init
func main() {
    greet("World")
    greet("Bob")
}
```

## FAQ

Q: Why doesn't it support recursion?
A: Recursion requires runtime stack frame maintenance, which is performance-intensive in Minecraft. It's recommended to rewrite recursive algorithms as iterative implementations.

Q: There are techniques to solve recursion, but the project chooses to ignore them?
A: Due to technical limitations and the author's limited energy.

Q: Why does the compiler report unknown errors with stack information? How to resolve?
A: You can open an issue on GitHub to report this problem.

Q: My code is clearly correct, but the generated datapack doesn't execute properly.
A: Please try disabling code optimization. If the generated datapack executes correctly, please prefix your issue title with `Code Optimization Error`; otherwise, use `Unknown Error` as the title prefix.

Q: Why does the generated datapack stop executing?
A: Please try using the gamerule command to appropriately increase the maxCommandChainLength rule value.

Q: Can't find an available backend?
A: Install the corresponding backend plugin.

## License

This project is licensed under Apache 2.0.

This means you **can** freely use it for personal or commercial purposes without direct permission from me.

At the same time, if you use this work in your project/product and derive commercial value from it, I warmly welcome you to acknowledge it in the following ways:

- **Attribute the source**: Mention this project in your product documentation or About page.
- **Share improvements**: Contribute your improvements based on this project back to the community.
- **Contribute**: Feel free to submit code, report issues, improve documentation, or propose suggestions to make the project better together.

Thank you for your support!
<!-- Where's the community? Who knows -->

## Acknowledgments

### Testing Participants

- 4424 discovered numerous bugs in the early stages of the project and provided many constructive suggestions.

### Code Usage

> Due to `Minecraft` version reasons, necessary modifications may be made to the following projects during actual use. If you wish your project not to be used or modified, please feel free to contact the project author to discuss removal.

- Project [fast_integer_sqrt](https://github.com/Triton365/fast_integer_sqrt) - Fast integer square root
<!--- Project [DNT-Dahesor-NBT-Transformer](https://github.com/Dahesor/DNT-Dahesor-NBT-Transformer) - Safe string concatenation, NBT to JSON conversion, and other SNBT and string operations-->
<!-- Not displayed as DNT doesn't support 1.21.4 -->
- Project [StringLib](https://github.com/CMDred/StringLib) - Provides numerous unsafe but fast string manipulation methods

### Data Usage

- [Wiki Datapack Format](https://zh.minecraft.wiki/w/Template:Data_pack_format) - Dynamically updates the correspondence between `Minecraft` and `datapack versions`

### Inspiration Sources / Expert Acknowledgments

- Expert [zmr-233](https://github.com/zmr-233/) - Proposed ideas for solving recursion problems (though I haven't read the books they recommended)
- Project [MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP) - A different technical approach to handling stacks (an excellent project)
- Project [clang-mc](https://github.com/xia-mc/clang-mc) - Very innovative idea, implementing partial assembly support in Minecraft
