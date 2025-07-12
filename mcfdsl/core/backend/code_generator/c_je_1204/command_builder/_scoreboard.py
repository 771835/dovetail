# coding=utf-8
import uuid
import warnings


class ScoreboardBuilder:
    @staticmethod
    def add_objective(objective: str, criteria: str, display_name: str = ""):
        return f"scoreboard objectives add {objective} {criteria} \"{display_name}\""

    @staticmethod
    def del_objective(objective: str):
        return f"scoreboard objectives remove {objective}"

    @staticmethod
    def set_score(targets: str, objective: str, score: int):
        return f"scoreboard players set {targets} {objective} {score}"

    @staticmethod
    def add_score(targets: str, objective: str, score: int):
        return f"scoreboard players add {targets} {objective} {score}"

    @staticmethod
    def sub_score(targets: str, objective: str, score: int):
        return f"scoreboard players remove {targets} {objective} {score}"

    @staticmethod
    def reset_score(targets: str, objective: str = ""):
        return f"scoreboard players reset {targets} {objective}"

    @staticmethod
    def mul_score(targets: str, objective: str, score: int) -> list[str]:
        temp = '#' + uuid.uuid4().hex
        return [ScoreboardBuilder.set_score(temp, objective, score),
                ScoreboardBuilder.mul_op(targets, objective, temp, objective),
                ScoreboardBuilder.reset_score(temp, objective)]

    @staticmethod
    def div_score(targets: str, objective: str, score: int) -> list[str]:
        temp = '#' + uuid.uuid4().hex
        return [ScoreboardBuilder.set_score(temp, objective, score),
                ScoreboardBuilder.div_op(targets, objective, temp, objective),
                ScoreboardBuilder.reset_score(temp, objective)]

    @staticmethod
    def mod_score(targets: str, objective: str, score: int) -> list[str]:
        temp = '#' + uuid.uuid4().hex
        return [ScoreboardBuilder.set_score(temp, objective, score),
                ScoreboardBuilder.mod_op(targets, objective, temp, objective),
                ScoreboardBuilder.reset_score(temp, objective)]

    @staticmethod
    def min_score(targets: str, objective: str, score: int) -> list[str]:
        temp = '#' + uuid.uuid4().hex
        return [ScoreboardBuilder.set_score(temp, objective, score),
                ScoreboardBuilder.min_op(targets, objective, temp, objective),
                ScoreboardBuilder.reset_score(temp, objective)]

    @staticmethod
    def max_score(targets: str, objective: str, score: int) -> list[str]:
        temp = '#' + uuid.uuid4().hex
        return [ScoreboardBuilder.set_score(temp, objective, score),
                ScoreboardBuilder.max_op(targets, objective, temp, objective),
                ScoreboardBuilder.reset_score(temp, objective)]

    @staticmethod
    def swap_score(targets: str, objective: str, score: int) -> list[str]:
        """
            [Deprecated] 交换目标与指定分数（已弃用，请直接使用 set_score()）
        """
        warnings.warn(
            "swap_score() is deprecated since v1.0.0. Use set_score() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        temp = '#' + uuid.uuid4().hex
        return [ScoreboardBuilder.set_score(temp, objective, score),
                ScoreboardBuilder.swap_op(targets, objective, temp, objective),
                ScoreboardBuilder.reset_score(temp, objective)]

    @staticmethod
    def operation(targets: str, target_obj: str,
                  op: str, source: str, source_obj: str):
        return f"scoreboard players operation {targets} {target_obj} {op} {source} {source_obj}"

    @staticmethod
    def set_op(targets: str, target_obj: str, source: str, source_obj: str):
        """ 将 source_obj 的分数赋给 target_obj """
        return ScoreboardBuilder.operation(
            targets, target_obj, "=", source, source_obj)

    @staticmethod
    def add_op(targets: str, target_obj: str, source: str, source_obj: str):
        """ 将 source_obj 的分数加到 target_obj """
        return ScoreboardBuilder.operation(
            targets, target_obj, "+=", source, source_obj)

    @staticmethod
    def sub_op(targets: str, target_obj: str, source: str, source_obj: str):
        """ 从 target_obj 中减去 source_obj 的分数 """
        return ScoreboardBuilder.operation(
            targets, target_obj, "-=", source, source_obj)

    @staticmethod
    def mul_op(targets: str, target_obj: str, source: str, source_obj: str):
        """ 将 target_obj 乘以 source_obj 的分数 """
        return ScoreboardBuilder.operation(
            targets, target_obj, "*=", source, source_obj)

    @staticmethod
    def div_op(targets: str, target_obj: str, source: str, source_obj: str):
        """ 将 target_obj 除以 source_obj 的分数（注意取整规则） """
        return ScoreboardBuilder.operation(
            targets, target_obj, "/=", source, source_obj)

    @staticmethod
    def mod_op(targets: str, target_obj: str, source: str, source_obj: str):
        """ 计算 target_obj 对 source_obj 的取模结果 """
        return ScoreboardBuilder.operation(
            targets, target_obj, "%=", source, source_obj)

    @staticmethod
    def min_op(targets: str, target_obj: str, source: str, source_obj: str):
        """ 将 target_obj 设为两者中的较小值 """
        return ScoreboardBuilder.operation(
            targets, target_obj, "<", source, source_obj)

    @staticmethod
    def max_op(targets: str, target_obj: str, source: str, source_obj: str):
        """ 将 target_obj 设为两者中的较大值 """
        return ScoreboardBuilder.operation(
            targets, target_obj, ">", source, source_obj)

    @staticmethod
    def swap_op(targets: str, target_obj: str, source: str, source_obj: str):
        """ 交换 target_obj 和 source_obj 的分数 """
        return ScoreboardBuilder.operation(
            targets, target_obj, "><", source, source_obj)
