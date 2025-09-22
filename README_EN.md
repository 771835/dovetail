# Dovetail

> _**Translated by AI, please check for accuracy**_

[English Version](README_EN.md) | [中文版本](README.md)

> Minecraft Data Pack Compilation Language | Object-oriented Minecraft DSL  
> This project references [MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP) in part  
> The implementation of this project is not yet mature. For production use, please consider other more mature projects

## Goals

- [ ] Write once, compile anywhere
- [x] Object-oriented support
- [ ] Complete dependency libraries, no need to write commands manually
- [ ] Lower learning curve

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

## FAQ

Q: Why is recursion not supported?  
A: Recursion requires runtime stack frame management, which is very cumbersome and complex to implement in Minecraft.
Therefore, you should rewrite recursion as iteration.

Q: There are many techniques that can handle recursion, such as CPS+TRO. Why not use them?  
A: Due to technical limitations and the author's limited energy.

Q: Why does the compiler show unknown errors and provide stack traces? How to solve this?  
A: You can open an issue on GitHub to report this problem.

Q: My code is clearly correct, but the generated commands fail to execute properly.  
A: First, try adding the `-O0` parameter. If the newly generated commands execute correctly, use `ir optimization error`
as the issue title prefix. Otherwise, use `unknown error` as the prefix.

Q: The generated commands stop executing halfway through.  
A: Try using the gamerule command to appropriately increase the value of the `maxCommandChainLength` rule.

## License

This project is licensed under the Apache 2.0 License.

## Acknowledgements

### Testing

- 4424 discovered many bugs in the early stages of the project and provided numerous constructive suggestions

### Code Usage

- Project [fast_integer_sqrt](https://github.com/Triton365/fast_integer_sqrt) for fast integer square root

### Inspiration/Thanks to Experts

- Expert [zmr-233](https://github.com/zmr-233/) proposed the CPS transformation approach to solve recursion
- Project [MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP) for a different technical approach to stack
  handling
