# Dovetail

[English Version](README_EN.md) | [中文版本](README.md)

> _**Translated by AI, please check for accuracy**_

> Minecraft Datapack Compilation Language | Object-Oriented Minecraft DSL  
> The implementation of this project is not yet mature. For production use, please consider other more mature projects.

## Goals

- [ ] Write once, compile everywhere
- [ ] Basic object-oriented support
- [ ] Comprehensive library support, no need to write commands manually
- [ ] Lower learning curve

## Long-term Plans (To Be Completed)

- Optimize error display
- Standardize debug information output
- Improve plugin API
- Keep up with Mojang version updates through iterative releases
- Enhance optimization effectiveness
- Find stack implementation methods that minimize performance overhead
- Support internationalization in the transpiler
- Optimize the transpiler for multithreading
- Streamline compilation for large projects
- Enable simple syntax for declaring and invoking other datapacks
- Support for predicates, custom data, and other features
- First-class function support
- Automated build script support

## Deployment

### Environment Requirements

- Python 3.10+

### Quick Start

    git clone https://github.com/771835/dovetail.git
    cd dovetail
    pip install -r requirements.txt
    python main.py -O2 xxx.mcdl

## FAQ

Q: Why is recursion not supported?  
A: Recursion requires maintaining stack frames at runtime, which is complex and cumbersome to implement in Minecraft.
Therefore, you should rewrite recursion into iterative implementations.  
Q: Many techniques can solve recursion, such as CPS + TRO + closures. Why not use them?  
A: Due to technical limitations and the author's limited bandwidth.  
Q: Why does the compiler report unknown errors and provide stack traces? How to resolve this?  
A: You can open an issue on GitHub to report this problem.  
Q: My code has no errors, but the generated commands do not execute correctly.  
A: First try using the `-O0` parameter. If the generated commands execute correctly, please prefix the issue title with
`IR optimization error`. Otherwise, prefix it with `Unknown error`.  
Q: The generated commands stop executing halfway.  
A: Try using the gamerule command to appropriately increase the `maxCommandChainLength` value.  
Q: What should I do if no available backend is found?  
A: Install the corresponding backend plugin.

## License

This project is licensed under Apache 2.0.

This means you **may** freely use it for personal or commercial purposes without direct permission from me.

At the same time, if you use this work unmodified in your project/product and derive commercial value from it, I would
greatly appreciate your acknowledgment through the following:

- **Attribute the source**: Mention this project in your product documentation or about page.
- **Share improvements**: Contribute improvements you make based on this project back to the community.
- **Contribute**: Welcome code submissions, bug reports, documentation improvements, or suggestions to help make the
  project better.

Thank you for your support!

## Acknowledgments

### Testing Contributors

- 4424 discovered many bugs in the early stages of the project and provided numerous constructive suggestions.

### Code Usage

- The project [fast_integer_sqrt](https://github.com/Triton365/fast_integer_sqrt) for fast integer square root.

### Inspiration/Credits

- Expert [zmr-233](https://github.com/zmr-233/) proposed the idea of using CPS transformation to solve recursion.
- The project [MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP) for exploring a different technical approach
  to stack handling.
