# coding=utf-8
"""
递归调用分析

基于调用图的强连通分量（SCC）检测，识别所有可能递归的函数/方法调用，
并在对应调用指令上标记 needs_stack_save。

支持两种调用指令：
  - IRCall:         operands[1] 是 Function
  - IRCallMethod:   operands[2] 是 Function

调用图从 IR 指令中提取，SCC 使用 Tarjan 算法分解。
所有包含自环的平凡 SCC 和大小 >= 2 的非平凡 SCC 均视为递归。
"""
from __future__ import annotations

from collections import defaultdict
from typing import NamedTuple

from dovetail.core.ir_code import IROpCode, IROpDescriptor
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.instructions import IRInstruction
from dovetail.core.symbols import Function
from dovetail.utils.logger import get_logger

logger = get_logger(__name__)

# ─── 元数据键 ────────────────────────────────────────────────────────────────

META_KEY_NEEDS_STACK_SAVE: str = "needs_stack_save"
"""IRInstruction.metadata 中的键名，值为 bool"""


# ─── 数据结构 ────────────────────────────────────────────────────────────────

class CallGraph(NamedTuple):
    """调用图，邻接表表示"""

    edges: dict[str, set[str]]
    """caller -> set of callees"""

    all_functions: set[str]
    """图中出现过的所有函数名（含限定方法名）"""


class RecursiveSCC(NamedTuple):
    """递归强连通分量"""

    members: frozenset[str]
    """SCC 内所有函数/方法名"""

    is_direct: bool
    """是否为直接递归（单节点自环）"""


# ─── 调用图构建 ──────────────────────────────────────────────────────────────

# 调用指令中 callee Function 的 operands 索引
_CALLEE_INDICES: dict[IROpDescriptor, int] = {
    IROpCode.CALL: 1,
    IROpCode.CALL_METHOD: 2,
}


def _get_callee_from_call(instr: IRInstruction) -> str | None:
    """
    从调用指令中提取 callee 的函数名。

    支持三种调用指令，通过预定义的 operands 索引取 Function 对象。
    未来统一方法调用指令后，只需修改此映射。

    Args:
        instr: 调用指令

    Returns:
        callee 函数名，非调用指令返回 None
    """
    index = _CALLEE_INDICES.get(instr.opcode)
    if index is None:
        return None
    if index >= len(instr.operands):
        return None
    callee: Function = instr.operands[index]
    return callee.get_name()


def build_call_graph(builder: IRBuilder) -> CallGraph:
    """
    从 IR 指令中提取函数/方法调用关系，构建调用图。

    遍历所有 IRFunction 和调用指令（CALL / CALL_METHOD / STRUCT_CALL），
    记录 caller -> callee 的边。
    方法定义挂在类/结构体内部，但其 IRFunction 的 name 应为限定名
    （如 MyClass.method），与调用侧的 Function.get_name() 对齐。

    Args:
        builder: IR 构建器

    Returns:
        调用图
    """
    edges: dict[str, set[str]] = defaultdict(set)
    all_functions: set[str] = set()
    current_func: str | None = None

    for instr in builder:
        if instr.opcode is IROpCode.FUNCTION:
            func: Function = instr.operands[0]
            current_func = func.name
            all_functions.add(func.name)
        else:
            callee_name = _get_callee_from_call(instr)
            if callee_name is not None and current_func is not None:
                edges[current_func].add(callee_name)
                all_functions.add(callee_name)

    return CallGraph(edges=dict(edges), all_functions=all_functions)


# ─── Tarjan SCC ──────────────────────────────────────────────────────────────

def _tarjan_scc(graph: dict[str, set[str]]) -> list[frozenset[str]]:
    """
    Tarjan 算法求强连通分量。

    时间复杂度 O(V + E)，空间复杂度 O(V)。

    Args:
        graph: 邻接表，键为节点，值为后继集合

    Returns:
        所有强连通分量列表，每个分量为函数名的 frozenset
    """
    index_counter: list[int] = [0]
    stack: list[str] = []
    on_stack: set[str] = set()

    index: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    sccs: list[frozenset[str]] = []

    def strongconnect(v: str) -> None:
        index[v] = index_counter[0]
        lowlink[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack.add(v)

        for w in graph.get(v, set()):
            if w not in index:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], index[w])

        if lowlink[v] == index[v]:
            component: set[str] = set()
            while True:
                w = stack.pop()
                on_stack.discard(w)
                component.add(w)
                if w == v:
                    break
            sccs.append(frozenset(component))

    for v in graph:
        if v not in index:
            strongconnect(v)

    return sccs


# ─── 递归 SCC 检测 ──────────────────────────────────────────────────────────

def find_recursive_sccs(call_graph: CallGraph) -> list[RecursiveSCC]:
    """
    从调用图中找出所有递归的强连通分量。

    判定规则：
      - SCC 大小 >= 2：间接递归，所有成员参与递归
      - SCC 大小 == 1 且有自环：直接递归
      - SCC 大小 == 1 且无自环：非递归，忽略

    Args:
        call_graph: 调用图

    Returns:
        所有递归 SCC 列表
    """
    all_sccs = _tarjan_scc(call_graph.edges)
    recursive: list[RecursiveSCC] = []

    for component in all_sccs:
        if len(component) > 1:
            recursive.append(RecursiveSCC(
                members=component,
                is_direct=False,
            ))
        elif len(component) == 1:
            func_name = next(iter(component))
            if func_name in call_graph.edges.get(func_name, set()):
                recursive.append(RecursiveSCC(
                    members=component,
                    is_direct=True,
                ))

    return recursive


# ─── 调用指令标记 ───────────────────────────────────────────────────────────

def tag_recursive_calls(builder: IRBuilder) -> None:
    """
    识别所有递归调用点，在对应调用指令的 metadata 上
    打上 needs_stack_save = True 标记。

    标记规则：caller 和 callee 属于同一个递归 SCC 内的调用
    一律标记。这保证了正确性优先于性能——即使运行时
    某条路径不构成递归，也执行 save/restore。

    Args:
        builder: IR 构建器（将被就地修改 metadata）
    """
    call_graph = build_call_graph(builder)
    recursive_sccs = find_recursive_sccs(call_graph)

    if not recursive_sccs:
        logger.debug("未检测到递归函数调用")
        return

    # 构建 函数名 -> 所属递归 SCC 的映射
    func_to_scc: dict[str, frozenset[str]] = {}
    for scc in recursive_sccs:
        for func_name in scc.members:
            func_to_scc[func_name] = scc.members

    # 遍历 IR，标记递归调用
    current_func: str | None = None
    tagged_count: int = 0

    for instr in builder:
        if instr.opcode is IROpCode.FUNCTION:
            current_func = instr.operands[0].get_name()
            continue

        callee_name = _get_callee_from_call(instr)
        if callee_name is not None and current_func is not None:
            if (current_func in func_to_scc
                    and callee_name in func_to_scc[current_func]):
                instr.metadata[META_KEY_NEEDS_STACK_SAVE] = True
                tagged_count += 1

    scc_summary = ", ".join(
        f"{'直接' if s.is_direct else '间接'}递归 {{{', '.join(sorted(s.members))}}}"
        for s in recursive_sccs
    )
    logger.info(
        f"递归分析完成: {len(recursive_sccs)} 个递归 SCC ({scc_summary}), "
        f"标记了 {tagged_count} 个调用点"
    )