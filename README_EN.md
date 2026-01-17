# Dovetail

[English Version](README_EN.md) | [中文版本](README.md)

> Minecraft Datapack Compilation Language  
> This project is not mature enough for production use. Please consider other more established projects if needed.

Dovetail is a language with object-oriented features that compiles to Minecraft datapacks. It aims to transform the procedural paradigm of traditional commands into a goal-oriented approach.

## Goals

- [ ] Write once, compile ~~crash~~ everywhere
- [ ] Basic object-oriented programming support
- [ ] Comprehensive dependency libraries to shield developers from direct command exposure
- [ ] Reduced datapack overhead

## Long-term Roadmap

- [ ] Enhanced error display
- [ ] Unified debug output
- [ ] Improved plugin API
- [ ] Version updates aligned with Minecraft releases
- [ ] Better optimization effectiveness
- [ ] Performance-efficient stack implementation methods
- [ ] Transpiler internationalization support
- [ ] Multi-threaded transpiler optimization
- [ ] Simple syntax for declaring and calling other datapacks
- [ ] Predicates, custom data, and other features
- [ ] First-class function support
- [ ] Simple event system and annotation features
- [ ] Enhanced built-in libraries

## Deployment

### Requirements

- Python 3.10+

### Quick Start

```bash
git clone https://github.com/771835/dovetail.git
cd dovetail
pip install -r requirements.txt
python main.py -O2 xxx.mcdl
```

## Example
 
```mcdl
func greet(name: string) {
    print(f"Hello, {name}");
}
@init
func main() {
    greet("World")
    greet("Bob")
}
```

## FAQ

**Q: Why doesn't it support recursion?**  
A: Recursion requires maintaining stack frames at runtime, which is extremely cumbersome and complex to implement in Minecraft. You should rewrite recursive algorithms as iterative ones.

**Q: There are many techniques to solve recursion, such as CPS+TRO+closures. Why not use them?**  
A: Due to technical limitations and the author's limited time and energy.

**Q: The compiler reports an unknown error with stack trace information. How to fix it?**  
A: You can open an issue on GitHub to report this problem.

**Q: My code has no errors, but the generated commands don't execute correctly.**  
A: First try using the `-O0` parameter to disable code optimization. If the regenerated commands execute correctly, prefix your issue title with "Code Optimization Error"; otherwise, use "Unknown Error" as the prefix.

**Q: The generated commands stop executing halfway.**  
A: Try using the gamerule command to appropriately increase the maxCommandChainLength value.

**Q: What if no available backend is found?**  
A: Install the corresponding backend plugin.

## License

This project is licensed under Apache 2.0.

This means you **can** freely use it for personal or commercial purposes without my direct permission.

At the same time, if you use this work in your project/product and derive commercial value from it, I warmly welcome you to acknowledge it in the following ways:

- **Credit the source**: Mention this project in your product documentation or about page.
- **Share improvements**: Contribute your improvements back to the community.
- **Make contributions**: Feel free to submit code, report issues, improve documentation, or provide suggestions to make the project better together.

Thank you for your support!

## Acknowledgments

### Testing Contributors

- 4424 discovered numerous bugs in the early stages and provided many constructive suggestions.

### Code Usage

- Project [fast_integer_sqrt](https://github.com/Triton365/fast_integer_sqrt) for fast integer square root

### Inspiration Sources / Special Thanks

- [zmr-233](https://github.com/zmr-233/) proposed the CPS transformation approach for solving recursion (though I haven't read the books they recommended)
- Project [MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP) for an alternative approach to stack handling
