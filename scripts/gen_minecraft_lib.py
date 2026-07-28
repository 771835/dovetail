#!/usr/bin/env python3
# coding=utf-8
"""
gen_minecraft_lib.py
根据 Minecraft 生成的命令报告，生成 minecraft.mcdl 库
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# ── 开关 ──────────────────────────────────────────────────────────
EMIT_REAL_ALIAS = True  # True：别名生成真实函数体；False：仅生成注释索引
SKIP_GETTING_COMMANDS = True  # True：跳过data get等指令并导入"__minecraft_getting__"；False：完整生成
# ── parser → MCDL 类型（全部用 string，避免 int 在部分命令无法判断是否可用的问题）──────────
PARSER_TO_TYPE: dict[str, str] = {
    "brigadier:bool": "string",
    "brigadier:integer": "string",
    "brigadier:float": "string",
    "brigadier:double": "string",
    "brigadier:long": "string",
    "brigadier:string": "string",
    "minecraft:entity": "string",
    "minecraft:game_profile": "string",
    "minecraft:block_pos": "string",
    "minecraft:column_pos": "string",
    "minecraft:vec3": "string",
    "minecraft:vec2": "string",
    "minecraft:block_state": "string",
    "minecraft:block_predicate": "string",
    "minecraft:item_stack": "string",
    "minecraft:item_predicate": "string",
    "minecraft:color": "string",
    "minecraft:component": "string",
    "minecraft:style": "string",
    "minecraft:message": "string",
    "minecraft:nbt_compound_tag": "string",
    "minecraft:nbt_tag": "string",
    "minecraft:nbt_path": "string",
    "minecraft:objective": "string",
    "minecraft:objective_criteria": "string",
    "minecraft:operation": "string",
    "minecraft:particle": "string",
    "minecraft:angle": "string",
    "minecraft:rotation": "string",
    "minecraft:scoreboard_slot": "string",
    "minecraft:swizzle": "string",
    "minecraft:team": "string",
    "minecraft:item_slot": "string",
    "minecraft:item_slots": "string",
    "minecraft:resource_location": "string",
    "minecraft:function": "string",
    "minecraft:entity_anchor": "string",
    "minecraft:int_range": "string",
    "minecraft:float_range": "string",
    "minecraft:dimension": "string",
    "minecraft:gamemode": "string",
    "minecraft:time": "string",
    "minecraft:template_mirror": "string",
    "minecraft:template_rotation": "string",
    "minecraft:heightmap": "string",
    "minecraft:loot_table": "string",
    "minecraft:loot_predicate": "string",
    "minecraft:loot_modifier": "string",
    "minecraft:uuid": "string",
    "minecraft:resource": "string",
    "minecraft:resource_key": "string",
    "minecraft:resource_or_tag": "string",
    "minecraft:resource_or_tag_key": "string",
}

# ── 别名表 ────────────────────────────────────────────────────────
# key: 别名命令名，value: 对应的完整命令名
COMMAND_ALIASES: dict[str, str] = {
    # 别名有点问题，所以不用了
    # "tp": "teleport",
    # "tell": "msg",
    "xp": "experience",
}

# ── 跳过表 ────────────────────────────────────────────────────────
# 不生成 MCDL 代码的表
SKIP_COMMANDS: set[str] = {
    "help",
    "debug",
    "jfr",
    "list",  # 由其他 api 获取玩家数量，故不提供
    "deop",
    "op",
    "publish",  # 不可能被使用
    "save-all",
    "save-off",
    "save-on",
    "seed",
    "unpublish",
    "version",
    "reload",  # 需要的话手动通过exec实现
    "test"
}


# ── 工具 ──────────────────────────────────────────────────────────

def sanitize(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", name)


def ptype(node: dict) -> str:
    return PARSER_TO_TYPE.get(node.get("parser", ""), "string")


def default_val(typ: str) -> str:
    match typ:
        case "string":
            return '""'
        case "int":
            return '0'
        case "boolean":
            return 'false'
        case _:  # 同 string
            return '""'


# ── 路径收集 ──────────────────────────────────────────────────────

# 一条"可执行路径"的表示：
# ExecutablePath = list of (seg_name, seg_type, node_dict)
ExecutablePath = list[tuple[str, str, dict]]


def collect_paths(
        node: dict,
        current: ExecutablePath,
        results: list[ExecutablePath],
        depth: int = 0,
) -> None:
    """DFS 收集命令树中所有可执行路径"""
    if depth > 32:
        return
    if node.get("executable", False) and depth > 0:
        results.append(list(current))
    for child_name, child_node in node.get("children", {}).items():
        ctype = child_node.get("type", "literal")
        collect_paths(child_node, current + [(child_name, ctype, child_node)],
                      results, depth + 1)


# ── 合并逻辑 ──────────────────────────────────────────────────────

def literal_key(path: ExecutablePath) -> str:
    """提取路径中所有 literal 段，作为函数名 key"""
    return "_".join(sanitize(seg) for seg, stype, _ in path if stype == "literal")


def merge_paths(
        root_cmd: str,
        paths: list[ExecutablePath],
) -> list[dict]:
    """
    将同一 literal_key 的路径合并为一个函数描述：
    {
      "fn_name": str,
      "params": [(name, type, is_optional)],   # 按出现顺序，必选在前
      "cmd_template": [(seg, type)],            # 用于构建 if-chain
    }
    """
    # 按 literal_key 分组
    groups: dict[str, list[ExecutablePath]] = defaultdict(list)
    for path in paths:
        groups[literal_key(path)].append(path)

    results = []
    for key, group_paths in groups.items():
        fn_name = sanitize(root_cmd) + ("_" + key if key else "")

        # 收集所有参数（argument 段），按在路径中首次出现顺序排列
        # 先找最长路径（参数最多），再标记哪些是"可选"（不是所有路径都有）
        all_arg_names: list[tuple[str, dict]] = []
        seen_arg_names: set[str] = set()

        # 按路径长度降序，确保最长的先处理
        for path in sorted(group_paths, key=len, reverse=True):
            for seg, stype, node in path:
                if stype == "argument":
                    safe = sanitize(seg)
                    if safe not in seen_arg_names:
                        seen_arg_names.add(safe)
                        all_arg_names.append((safe, node))

        # 判断哪些参数是可选的：不存在于所有路径中的参数为可选
        required_args: set[str] = set()
        for path in group_paths:
            arg_set = {sanitize(s) for s, t, _ in path if t == "argument"}
            if not required_args:
                required_args = arg_set
            else:
                required_args &= arg_set  # 所有路径都有的才是必选

        params = []
        for safe_name, node in all_arg_names:
            is_optional = safe_name not in required_args
            params.append((safe_name, ptype(node), is_optional))

        # 确保必选参数在前，可选参数在后
        params.sort(key=lambda x: x[2])  # False(必选) < True(可选)

        # 构建命令模板：每个段是 (原始名, literal|argument)
        # 取最长路径作为模板（包含所有可能的段）
        longest = max(group_paths, key=len)
        cmd_template = [(seg, stype) for seg, stype, _ in longest]

        results.append({
            "fn_name": fn_name,
            "params": params,
            "cmd_template": cmd_template,
            "root_cmd": root_cmd,
            "all_paths": group_paths,
        })

    return results


# ── 代码生成 ──────────────────────────────────────────────────────

def fmt_params(params: list[tuple[str, str, bool]]) -> str:
    parts = []
    for name, typ, optional in params:
        if optional:
            parts.append(f'{name}: {typ} = {default_val(typ)}')
        else:
            parts.append(f'{name}: {typ}')
    return ", ".join(parts)


def build_exec(root_cmd: str, template: list[tuple[str, str]]) -> str:
    """根据完整模板构建 exec(f"...") 字符串"""
    parts = [root_cmd]
    for seg, stype in template:
        parts.append("{" + sanitize(seg) + "}" if stype == "argument" else seg)
    cmd = " ".join(parts)
    return f'exec(f"{cmd}")'


def emit_fn(desc: dict) -> list[str]:
    """
    生成单个合并函数。
    对于有可选参数的情况，生成 if-chain 按参数是否为空决定命令长度。

    策略：
      - 找出所有可执行路径按参数数量排序
      - 每个路径对应一个 if 分支（判断该路径的最后一个可选参数是否为空）
      - 最长路径为 else 分支（或最后一个 if）
    """
    fn_name = desc["fn_name"]
    params = desc["params"]
    root_cmd = desc["root_cmd"]
    all_paths: list[ExecutablePath] = desc["all_paths"]

    lines = [f"fn {fn_name}({fmt_params(params)}) {{"]

    optional_params: list[tuple[str, str]] = [(n, t) for n, t, opt in params if opt]

    if not optional_params:
        # 无可选参数，直接生成单条 exec
        template = desc["cmd_template"]
        lines.append(f"    {build_exec(root_cmd, template)}")
    else:
        # 按路径中 argument 数量升序排列，构建 if-elif-else 链
        sorted_paths = sorted(all_paths, key=lambda p: sum(1 for _, t, _ in p if t == "argument"))

        for i, path in enumerate(sorted_paths):
            arg_names_in_path = [sanitize(s) for s, t, _ in path if t == "argument"]
            template = [(seg, stype) for seg, stype, _ in path]

            # 条件：当前路径比上一条多出的那个参数为空
            # → 即该路径是"刚好到这里停下"的情况
            # 找出本路径相比上一条多出的最后一个可选参数
            if i == len(sorted_paths) - 1:
                # 最后一条：else 分支
                lines.append(f"    }} else {{")
                lines.append(f"        {build_exec(root_cmd, template)}")
            elif i == 0:
                # 第一条：找第一个可选参数作为判断条件
                missing_param = next(
                    (p for p in optional_params if p[0] not in arg_names_in_path),
                    optional_params[0][0]
                )

                lines.append(f'    if ({missing_param[0]} == {default_val(missing_param[1])}) {{')

                lines.append(f"        {build_exec(root_cmd, template)}")
            else:
                # 中间条：找本路径有但下一条还不够的参数
                next_args = [sanitize(s) for s, t, _ in sorted_paths[i + 1] if t == "argument"]
                extra = next(
                    (n for n in next_args if n not in arg_names_in_path),
                    None
                )
                extra_param = next(
                    (p for p in params if p[0] == extra),
                )

                cond = f'{extra} == {default_val(extra_param[1])}' if extra else f'{optional_params[-1][0]} != {default_val(optional_params[-1][1])}'
                lines.append(f'    }} else if ({cond}) {{')
                lines.append(f"        {build_exec(root_cmd, template)}")

        lines.append(f"    }}")  # 关闭最后的 else

    lines.append(f"}}")
    lines.append("")
    return lines


# ── 别名生成 ──────────────────────────────────────────────────────

def emit_aliases(
        all_descs: list[dict],
) -> list[str]:
    lines = []
    lines.append("// ────────────────────────────────────────────────────────────")
    lines.append("// 命令别名")
    lines.append("// ────────────────────────────────────────────────────────────")
    lines.append("")

    for alias, canonical in COMMAND_ALIASES.items():
        alias_safe = sanitize(alias)
        canonical_safe = sanitize(canonical)

        matched = [d for d in all_descs if d["fn_name"].startswith(canonical_safe)]
        if not matched:
            lines.append(f"// [跳过] 未找到 {canonical} 的函数定义")
            lines.append("")
            continue

        for desc in matched:
            orig_fn = desc["fn_name"]
            alias_fn = alias_safe + orig_fn[len(canonical_safe):]
            params = desc["params"]

            if EMIT_REAL_ALIAS:
                # 生成真实函数体，exec 直接用 alias 命令名
                lines.append(f"fn {alias_fn}({fmt_params(params)}) {{")

                optional_params = [n for n, t, opt in params if opt]
                all_paths: list[ExecutablePath] = desc["all_paths"]

                if not optional_params:
                    template = desc["cmd_template"]
                    # 替换 root_cmd 为 alias
                    lines.append(f"    {build_exec(alias, template)}")
                else:
                    sorted_paths = sorted(
                        all_paths,
                        key=lambda p: sum(1 for _, t, _ in p if t == "argument")
                    )
                    for i, path in enumerate(sorted_paths):
                        arg_names_in_path = [sanitize(s) for s, t, _ in path if t == "argument"]
                        template = [(seg, stype) for seg, stype, _ in path]
                        if i == len(sorted_paths) - 1:
                            lines.append(f"    }} else {{")
                            lines.append(f"        {build_exec(alias, template)}")
                        elif i == 0:
                            missing = next(
                                (n for n in optional_params if n not in arg_names_in_path),
                                optional_params[0]
                            )
                            lines.append(f'    if ({missing} == "") {{')
                            lines.append(f"        {build_exec(alias, template)}")
                        else:
                            next_args = [sanitize(s) for s, t, _ in sorted_paths[i + 1] if t == "argument"]
                            extra = next(
                                (n for n in next_args if n not in arg_names_in_path), None
                            )
                            cond = f'{extra} == ""' if extra else f'{optional_params[-1]} != ""'
                            lines.append(f"    }} else if ({cond}) {{")
                            lines.append(f"        {build_exec(alias, template)}")
                    lines.append(f"    }}")

                lines.append(f"}}")
                lines.append("")
            else:
                lines.append(f"// {alias_fn} → {orig_fn}")

    return lines


# ── 主流程 ────────────────────────────────────────────────────────

def generate(commands_json: dict) -> str:
    header = [
        "// ================================================================",
        "// lib/minecraft.mcdl",
        "// Minecraft Java Edition 原版指令标准库",
        "// 由 gen_minecraft_lib.py 自动生成，请勿手动修改",
        "// ================================================================",
        "",
        'include \"__minecraft_getting__\"' if SKIP_GETTING_COMMANDS else "",
        ""
    ]

    all_lines: list[str] = list(header)
    all_descs: list[dict] = []

    for cmd_name, cmd_node in commands_json.get("children", {}).items():
        # 跳过无意义的指令
        if cmd_name in SKIP_COMMANDS:
            continue

        all_lines.append(f"// {'─' * 60}")
        all_lines.append(f"// {cmd_name}")
        all_lines.append(f"// {'─' * 60}")
        all_lines.append("")

        # 收集该命令下所有可执行路径
        paths: list[ExecutablePath] = []
        collect_paths(cmd_node, [], paths)

        if not paths:
            all_lines.append(f"// (无可执行子命令)")
            all_lines.append("")
            continue

        # 合并同名函数
        descs = merge_paths(cmd_name, paths)
        all_descs.extend(descs)

        for desc in descs:
            fn_name: str = desc["fn_name"]
            if SKIP_GETTING_COMMANDS and fn_name.startswith(("data_get", "scoreboard_players_get")):
                continue
            all_lines.extend(emit_fn(desc))

    # 别名区块
    all_lines.extend(emit_aliases(all_descs))

    return "\n".join(all_lines)


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("commands.json")
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("../lib/minecraft.mcdl")

    if not input_path.exists():
        print(f"[错误] 找不到输入文件: {input_path}")
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    mcdl = generate(data)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(mcdl)

    fn_count = mcdl.count("\nfn ")
    print(f"[✓] 共生成 {fn_count} 个函数 → {output_path}")


if __name__ == "__main__":
    main()
