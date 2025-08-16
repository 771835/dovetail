# coding=utf-8
import uuid
import warnings


class ScoreboardBuilder:
    @staticmethod
    def add_objective(objective: str, criteria: str, display_name: str = ""):
        """
        增加记分板

        :param objective: 记分板名称
        :param criteria: 记分板准则
        :param display_name: 记分板演示名
        :return: 生成的指令
        """
        return f"scoreboard objectives add {objective} {criteria} \"{display_name}\""

    @staticmethod
    def del_objective(objective: str):
        """
        删除一个记分板

        :param objective: 将要删除的记分板名称
        :return: 生成的指令
        """
        return f"scoreboard objectives remove {objective}"

    @staticmethod
    def get_score(target: str, objective: str):
        """
        读取目标的分数

        :param target: 目标
        :param objective: 目标的记分板名称
        :return: 生成的指令
        """
        return f"scoreboard players get {target} {objective}"

    @staticmethod
    def set_score(targets: str, objective: str, score: int):
        """
        设置目标的分数

        :param targets: 目标
        :param objective: 目标的记分板名称
        :param score: 需要设置的分数
        :return: 生成的指令
        """
        return f"scoreboard players set {targets} {objective} {score}"

    @staticmethod
    def add_score(targets: str, objective: str, score: int) -> list[str]:
        """
        设置目标的分数

        :param targets: 目标
        :param objective: 目标的记分板名称
        :param score: 需要增加的分数
        :return: 生成的指令
        """
        return [f"scoreboard players add {targets} {objective} {score}"]

    @staticmethod
    def sub_score(targets: str, objective: str, score: int) -> list[str]:
        """
        设置目标的分数

        :param targets: 目标
        :param objective: 目标的记分板名称
        :param score: 需要减少的分数
        :return: 生成的指令
        """
        return [f"scoreboard players remove {targets} {objective} {score}"]

    @staticmethod
    def reset_score(targets: str, objective: str = ""):
        """
        重置目标的分数

        :param targets: 目标
        :param objective: 目标的记分板名称
        :return: 生成的指令
        """
        return f"scoreboard players reset {targets} {objective}"

    @staticmethod
    def mul_score(targets: str, objective: str, score: int) -> list[str]:
        """
        将目标的分数乘以指定值

        :param targets: 目标
        :param objective: 目标的记分板名称
        :param score: 指定值
        :return: 生成的指令
        """
        #  对于score为2的情况下进行优化(使用加法而非乘法)
        if score == 1:
            return []
        elif score <= 3:
            return [ScoreboardBuilder.add_op(targets, objective, targets, objective)]*int(score-1)
        temp = '#' + uuid.uuid4().hex
        return [ScoreboardBuilder.set_score(temp, objective, score),
                ScoreboardBuilder.mul_op(targets, objective, temp, objective),
                ScoreboardBuilder.reset_score(temp, objective)]

    @staticmethod
    def div_score(targets: str, objective: str, score: int) -> list[str]:
        """
        将目标的分数除以指定值

        :param targets: 目标
        :param objective: 目标的记分板名称
        :param score: 指定值
        :return: 生成的指令
        """
        temp = '#' + uuid.uuid4().hex
        return [ScoreboardBuilder.set_score(temp, objective, score),
                ScoreboardBuilder.div_op(targets, objective, temp, objective),
                ScoreboardBuilder.reset_score(temp, objective)]

    @staticmethod
    def mod_score(targets: str, objective: str, score: int) -> list[str]:
        """
        将目标的分数取模为指定值

        :param targets: 目标
        :param objective: 目标的记分板名称
        :param score: 指定值
        :return: 生成的指令
        """
        temp = '#' + uuid.uuid4().hex
        return [ScoreboardBuilder.set_score(temp, objective, score),
                ScoreboardBuilder.mod_op(targets, objective, temp, objective),
                ScoreboardBuilder.reset_score(temp, objective)]

    @staticmethod
    def min_score(targets: str, objective: str, score: int) -> list[str]:
        """
        目标的分数与指定值取较小值

        :param targets: 目标
        :param objective: 目标的记分板名称
        :param score: 指定值
        :return: 生成的指令
        """
        temp = '#' + uuid.uuid4().hex
        return [ScoreboardBuilder.set_score(temp, objective, score),
                ScoreboardBuilder.min_op(targets, objective, temp, objective),
                ScoreboardBuilder.reset_score(temp, objective)]

    @staticmethod
    def max_score(targets: str, objective: str, score: int) -> list[str]:
        """
        目标的分数与指定值取较大值

        :param targets: 目标
        :param objective: 目标的记分板名称
        :param score: 指定值
        :return: 生成的指令
        """
        temp = '#' + uuid.uuid4().hex
        return [ScoreboardBuilder.set_score(temp, objective, score),
                ScoreboardBuilder.max_op(targets, objective, temp, objective),
                ScoreboardBuilder.reset_score(temp, objective)]

    @staticmethod
    def swap_score(targets: str, objective: str, score: int) -> list[str]:
        """
            [Deprecated] 交换目标与指定分数（已弃用，推荐直接使用 set_score()）
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
