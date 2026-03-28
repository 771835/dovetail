# coding=utf-8
"""
字符串相似度匹配工具
用于编译器错误提示中的智能建议
"""

from difflib import SequenceMatcher
from typing import Optional


class StringSimilarity:
    """字符串相似度计算工具类

    提供多种字符串相似度计算方法，用于编译器中的智能错误提示。
    """

    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """计算两个字符串的莱文斯坦距离（编辑距离）

        莱文斯坦距离表示将一个字符串转换为另一个字符串所需的最少单字符编辑操作次数。
        允许的操作包括：插入、删除、替换。

        Args:
            s1 (str): 第一个字符串
            s2 (str): 第二个字符串

        Returns:
            int: 编辑距离，即需要的最少操作次数。值越小表示两个字符串越相似。

        Example:
            >>> StringSimilarity.levenshtein_distance("kitten", "sitting")
            3
            >>> StringSimilarity.levenshtein_distance("hello", "hello")
            0

        Note:
            时间复杂度 O(m*n)，空间复杂度 O(n)，其中 m 和 n 是两个字符串的长度。
        """
        if len(s1) < len(s2):
            return StringSimilarity.levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # 插入、删除、替换的成本
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    @staticmethod
    def similarity_ratio(s1: str, s2: str, method: str = "sequence") -> float:
        """计算两个字符串的相似度分数

        Args:
            s1 (str): 第一个字符串
            s2 (str): 第二个字符串
            method (str, optional): 计算方法。可选值：
                - "sequence": 使用 SequenceMatcher 算法（快速，推荐）
                - "levenshtein": 使用编辑距离算法（精确）
                默认为 "sequence"。

        Returns:
            float: 相似度分数，范围 [0.0, 1.0]。
                - 1.0 表示完全相同
                - 0.0 表示完全不同

        Raises:
            ValueError: 如果 method 参数不是有效值

        Example:
            >>> StringSimilarity.similarity_ratio("hello", "hallo")
            0.8
            >>> StringSimilarity.similarity_ratio("abc", "xyz")
            0.0
            >>> StringSimilarity.similarity_ratio("test", "test", method="levenshtein")
            1.0

        Note:
            - "sequence" 方法基于最长公共子序列，适合大多数场景
            - "levenshtein" 方法基于编辑距离，对单字符差异更敏感
        """
        if not s1 or not s2:
            return 0.0

        if s1 == s2:
            return 1.0

        if method == "levenshtein":
            max_len = max(len(s1), len(s2))
            distance = StringSimilarity.levenshtein_distance(s1, s2)
            return 1.0 - (distance / max_len)
        elif method == "sequence":
            return SequenceMatcher(None, s1, s2).ratio()
        else:
            raise ValueError(f"Invalid method '{method}'. Must be 'sequence' or 'levenshtein'.")

    @staticmethod
    def find_best_match(
            target: str,
            candidates: list[str],
            threshold: float = 0.6,
            case_sensitive: bool = False,
            method: str = "sequence"
    ) -> Optional[str]:
        """在候选列表中找到与目标字符串最相似的一个

        Args:
            target (str): 目标字符串（通常是用户输入的可能有误的字符串）
            candidates (list[str]): 候选字符串列表（有效的名称列表）
            threshold (float, optional): 相似度阈值，范围 [0.0, 1.0]。
                只返回相似度超过此阈值的匹配。默认为 0.6。
            case_sensitive (bool, optional): 是否区分大小写。默认为 False。
            method (str, optional): 相似度计算方法。可选 "sequence" 或 "levenshtein"。
                默认为 "sequence"。

        Returns:
            Optional[str]: 最相似的候选字符串（原始大小写）。
                如果没有候选项超过阈值，返回 None。

        Example:
            >>> candidates = ["username", "password", "email"]
            >>> StringSimilarity.find_best_match("usrname", candidates)
            'username'
            >>> StringSimilarity.find_best_match("xyz", candidates, threshold=0.8)
            None
            >>> StringSimilarity.find_best_match("USERNAME", candidates, case_sensitive=False)
            'username'

        Note:
            推荐的阈值设置：
            - 0.5-0.6: 宽松，适合容错性高的场景
            - 0.6-0.7: 平衡，适合一般错误提示（推荐）
            - 0.7-0.8: 严格，只匹配非常相似的字符串
        """
        if not target or not candidates:
            return None

        # 预处理：大小写
        search_target = target if case_sensitive else target.lower()
        search_candidates = candidates if case_sensitive else [c.lower() for c in candidates]

        best_match = None
        best_score = threshold  # 初始设为阈值，只保存超过阈值的

        for i, candidate in enumerate(search_candidates):
            score = StringSimilarity.similarity_ratio(search_target, candidate, method)
            if score > best_score:
                best_score = score
                best_match = candidates[i]  # 返回原始大小写的候选项

        return best_match

    @staticmethod
    def find_top_matches(
            target: str,
            candidates: list[str],
            threshold: float = 0.6,
            top_n: int = 3,
            case_sensitive: bool = False,
            method: str = "sequence"
    ) -> list[tuple[str, float]]:
        """在候选列表中找到与目标字符串最相似的前 N 个

        Args:
            target (str): 目标字符串
            candidates (list[str]): 候选字符串列表
            threshold (float, optional): 相似度阈值，范围 [0.0, 1.0]。默认为 0.6。
            top_n (int, optional): 返回前 N 个结果。默认为 3。
            case_sensitive (bool, optional): 是否区分大小写。默认为 False。
            method (str, optional): 相似度计算方法。默认为 "sequence"。

        Returns:
            list[tuple[str, float]]: 匹配结果列表，每个元素为 (候选字符串, 相似度分数)。
                按相似度分数降序排列。如果匹配数量少于 top_n，返回所有匹配项。

        Example:
            >>> candidates = ["username", "user_name", "password", "user_id"]
            >>> StringSimilarity.find_top_matches("usrname", candidates, top_n=2)
            [('username', 0.857), ('user_name', 0.75)]
            >>> StringSimilarity.find_top_matches("xyz", candidates, threshold=0.8)
            []

        Note:
            返回的分数已四舍五入到小数点后三位，用于显示。
            如果需要精确分数用于进一步计算，请直接使用 similarity_ratio()。
        """
        if not target or not candidates:
            return []

        search_target = target if case_sensitive else target.lower()
        search_candidates = candidates if case_sensitive else [c.lower() for c in candidates]

        # 计算所有相似度
        matches = []
        for i, candidate in enumerate(search_candidates):
            score = StringSimilarity.similarity_ratio(search_target, candidate, method)
            if score >= threshold:
                matches.append((candidates[i], score))

        # 按分数降序排序，取前 N 个
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:top_n]


# ==================== 便捷函数 ====================

def suggest_similar(
        typo: str,
        valid_names: list[str],
        threshold: float = 0.6,
        case_sensitive: bool = False
) -> Optional[str]:
    """为拼写错误提供建议（便捷函数）

    这是 StringSimilarity.find_best_match() 的便捷封装，
    使用默认的 "sequence" 方法进行快速匹配。

    Args:
        typo (str): 可能拼错的字符串
        valid_names (list[str]): 有效的名称列表
        threshold (float, optional): 相似度阈值。默认为 0.6。
        case_sensitive (bool, optional): 是否区分大小写。默认为 False。

    Returns:
        Optional[str]: 建议的正确名称。如果没有合适建议则返回 None。

    Example:
        >>> suggest_similar("usrname", ["username", "password"])
        'username'
        >>> suggest_similar("calcualte", ["calculate", "calibrate"])
        'calculate'
        >>> suggest_similar("xyz", ["abc", "def"], threshold=0.8)
        None

    See Also:
        StringSimilarity.find_best_match(): 提供更多自定义选项的完整版本
        StringSimilarity.find_top_matches(): 返回多个候选建议
    """
    return StringSimilarity.find_best_match(
        typo,
        valid_names,
        threshold=threshold,
        case_sensitive=case_sensitive
    )
