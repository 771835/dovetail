# coding=utf-8
"""
通过 Minecraft 版本获得数据包版本号
"""
import re
from functools import lru_cache
from typing import Optional

import requests

from transpiler.core.enums import MinecraftVersion

DEFAULT_MINECRAFT_VERSION_TO_DATAPACK_FORMAT_MAP = {
    '1.13': 4,
    '1.15': 5,
    '1.16.2': 6,
    '1.17': 7,
    '1.18': 8,
    '1.18.2': 9,
    '1.19': 10,
    '1.19.4': 12,
    '1.20': 15,
    '1.20.2': 18,
    '1.20.3': 26,
    '1.20.5': 41,
    '1.21': 48,
    '1.21.2': 57,
    '1.21.4': 61,
    '1.21.5': 71,
    '1.21.6': 80,
    '1.21.7': 81,
    '1.21.9': 88.0,
    '1.21.11': 94.1,
}

wiki_table_pattern = re.compile(r'<tab.*?标志.*?/table>', re.DOTALL)
wiki_row_pattern = re.compile(r'<tr[^>]*?>\s*<td>([\d.]+)</td>\s*<td>.*?>([\d.]+)<', re.DOTALL)


@lru_cache(maxsize=None)
def _get_wiki_new_map() -> dict[str, int | float]:
    try:
        response = requests.get(
            "https://zh.minecraft.wiki/w/Template:Data_pack_format",
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException:
        return {}

    # 找到表格
    table_match = wiki_table_pattern.search(response.text)
    if not table_match:
        return {}

    new_map = {}
    # 一次正则匹配提取所有需要的数据
    for match in wiki_row_pattern.finditer(table_match.group()):
        try:
            datapack_format_str = match.group(1)
            minecraft_version = match.group(2)

            # 处理整数和浮点数（如 88.0, 94.1）
            datapack_format = float(datapack_format_str) if '.' in datapack_format_str else int(datapack_format_str)

            new_map[minecraft_version] = datapack_format
        except (ValueError, IndexError):
            continue

    return new_map


def get_datapack_format(
        version: MinecraftVersion | str,
        ref_map: Optional[dict[str, int | float]] = None
) -> float | int:
    if isinstance(version, str):
        version = MinecraftVersion.instance(version)
    if ref_map is None:
        used_map = DEFAULT_MINECRAFT_VERSION_TO_DATAPACK_FORMAT_MAP
    else:
        used_map = ref_map
    # 尝试从给定表中查找数据包编号
    last: float | int | None = None
    for minecraft_version in reversed(used_map.keys()):
        v = MinecraftVersion.instance(minecraft_version)
        if version < v:
            break
        last = used_map[minecraft_version]
    # 当找到合适的数据包编号且不为最后一个时
    if last is not None:
        return last
    else:
        if ref_map is None:
            # 爬取wiki获得新对应表
            new_map = _get_wiki_new_map()
            return get_datapack_format(version, new_map)
        else:
            return next(reversed(ref_map.values()))
