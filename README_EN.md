# Dovetail

> This article was translated by AI and may contain errors.

[English Version](README_EN.md) | [中文版本](README.md)

> Minecraft Datapack Compilation Language - A Solution with Partial Object-Oriented Features
>
> **Current Status:**
> - **Advantages:** Basic syntax is functional and capable of compiling simple programs.
> - **Known Limitations:** Lacks extensive standard library, unfriendly error messages, optimizer may introduce bugs,
    complete OOP features not yet implemented.
> - **Production Environment Recommendation:** If you need it for production use, please consider
    using [MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP)
    or other more mature projects.
> - Due to technical limitations, no new feature implementations will be committed in the short term.
> - **Nature:** Compared to stability-focused projects like **clang-mc**, this project leans toward using more
    aggressive features and optimizations, as well as experimental handling of certain content. These changes may not be
    specially marked and lack long-term stable maintenance.
> - **Syntax:** Syntax updates iterate rapidly, therefore backward compatibility is not guaranteed. Correct syntax is
    only guaranteed with accompanying examples when releases are published.

**Dovetail** is an object-oriented language that compiles into `Minecraft Datapacks` (hereinafter referred to as
`datapacks`). It aims to transform the procedural orientation of traditional commands into goal-oriented design.

## Goals

- [ ] Write once, ~~crash~~ compile everywhere
- [ ] Basic object-oriented support
- [ ] Comprehensive dependency libraries to prevent developers from programming directly with commands
- [ ] Low-overhead datapacks
- [ ] Version iterations keeping pace with Minecraft major version updates

## Long-term Plans

- [ ] Improve safety and performance through prerequisite datapacks
- [ ] Optimize error display
- [x] Unified logging output
- [ ] Improve plugin API
- [ ] Enhance optimization effectiveness
- [ ] Find performance-efficient stack implementation methods
- [ ] Compiler internationalization support
- [ ] Allow declaration and invocation of other datapacks through simple syntax
- [ ] Predicates, custom data, and other features
- [ ] First-class functions
- [ ] Simple event system and annotation functionality
- [ ] Comprehensive built-in library

## Quick Start

### Requirements

- Python 3.11+ (PyPy is supported and recommended)
- Minecraft Java Edition 1.21.4-1.21.5

### Installation

```bash
git clone https://github.com/771835/dovetail.git
cd dovetail
pip install -r requirements.txt
python main.py -O2 xxx.mcdl
```

### Code Example

```mcdl
// Define function
fn greet(name: string) {
    print(f"Hello, {name}");
}

// Main function (using @init annotation)
@init
fn main() {
    greet("World")
    greet("Bob")
}
```

## How to Contribute

- Bug Reports and Suggestions
    - Submit an issue and wait for project authors or other contributors to make fixes
- Bug Fixes or Submissions
    1. Submit an issue or pull request and wait for fixes or implementation
- Complex Feature Implementation
    1. Create or modify DFP document proposals based on the corresponding feature
    2. After community discussion reaches consensus, clone a new branch for modifications
    3. Test for errors
    4. Merge into main branch

## FAQ

Q: Why doesn't it support recursion?  
A: Recursion requires maintaining stack frames at runtime, which has significant performance overhead in Minecraft. It's
recommended to rewrite recursive algorithms as iterative implementations.

Q: There are techniques to solve recursion, but the project chooses to ignore them?  
A: Due to technical limitations and the author's limited time and energy.

Q: Why does the compiler show unknown errors with stack information? How to resolve it?  
A: You can open an issue on the `GitHub` platform to report this problem.

Q: My code is clearly correct, but the generated datapack doesn't execute properly.  
A: Please try disabling code optimization. If the generated datapack executes correctly, use `Code Optimization Error`
as the issue title prefix; otherwise, use `Unknown Error` as the title prefix.

Q: Why does the generated datapack halt during execution?  
A: Try using the `gamerule` command to appropriately increase the `maxCommandChainLength` rule value.

Q: What if no available backend is found?  
A: Install the corresponding backend plugin.

## Known Issues (Won't be fixed in the long term)

- No recursion support
- Advanced leaky memory management

## License

This project is licensed under Apache 2.0

This means you **can** freely use it for personal or commercial purposes without my direct permission.

Meanwhile, if you use this work in your project/product and derive commercial value from it, I would greatly appreciate
your acknowledgment through the following ways:

- **Attribution**: Mention this project in your product documentation or About page.
- **Share Improvements**: Contribute back improvements you've made based on this project to the community.
- **Contribute**: Welcome code submissions, bug reports, documentation improvements, or suggestions to make the project
  better together.

Thank you for your support!
<!-- Where's the community? Who knows -->

## Acknowledgments

### Testing Participants

- 4424 discovered numerous bugs in the early stages of the project and provided many constructive suggestions

### Code Usage

> Due to `Minecraft` version compatibility reasons, necessary modifications may be made to the following projects during
> actual use. If you are an author or contributor to any of the following projects and wish your project not to be used or
> modified, please feel free to contact the project author to discuss removal.

- Project [fast_integer_sqrt](https://github.com/Triton365/fast_integer_sqrt) Fast integer square root  
  _See the isqrt function in [mathlib](lib/mathlib.mcdl) for specific usage_

<!--- Project [DNT-Dahesor-NBT-Transformer](https://github.com/Dahesor/DNT-Dahesor-NBT-Transformer) Safe string concatenation, NBT to JSON and other SNBT and string operations-->
<!-- Not displayed or used because DNT doesn't support 1.21.4 -->

- Project [StringLib](https://github.com/CMDred/StringLib) Provides numerous unsafe but reasonably fast string
  manipulation methods

<!-- It seems I can write the stuff from this library myself, and that way I can inline it too ( -->

### Data Usage

- [Chinese Wiki Datapack Version](https://zh.minecraft.wiki/w/Template:Data_pack_format) Dynamically updates the
  correspondence between `Minecraft` and `datapack versions`

### Other Recommendations

- [《Feature》](https://vanillalibrary.mcfpp.top/datapack-index/feature/_index.html)
  《Feature》is a platform hosted by the Vanilla Library team for collecting and showcasing short articles on vanilla
  mod (datapack + resource pack) development, aimed at communication between developers, updated monthly.

### Inspiration Sources / Expert Acknowledgments

- Expert [zmr-233](https://github.com/zmr-233/) proposed ideas for solving recursion problems (although I haven't read
  the books they recommended, nor implemented them)
- Project [MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP) An excellent project with a different technical
  approach to handling stacks
- Project [clang-mc](https://github.com/xia-mc/clang-mc) Very innovative idea, implementing partial support for assembly
  in Minecraft with great potential