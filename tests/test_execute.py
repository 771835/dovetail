# coding=utf-8
import unittest

from mcfdsl.core.command_builder import Execute

class TestExecuteBuilder(unittest.TestCase):
    """ExecuteBuilder 功能测试套件"""

    def test_example_1_simple_as_run(self):
        """测试基础 as 和 run 的组合"""
        cmd = Execute.execute().as_("@a").run("say Hello!")
        self.assertEqual(str(cmd), "execute as @a run say Hello!")

    def test_example_2_at_if_block_run(self):
        """测试位置条件判断"""
        cmd = (
            Execute.execute()
            .at("@s")
            .if_block("~ ~-1 ~", "minecraft:dirt")
            .run("setblock ~ ~ ~ minecraft:grass_block")
        )
        self.assertEqual(
            str(cmd),
            "execute at @s if block ~ ~-1 ~ minecraft:dirt run setblock ~ ~ ~ minecraft:grass_block"
        )

    def test_example_3_positioned_unless_entity_store_score(self):
        """测试位置条件+实体否定条件+记分板存储"""
        cmd = (
            Execute.execute()
            .positioned("100 64 200")
            .unless_entity("@e[type=minecraft:zombie]")
            .store_result_score("@s", "zombie_count")
            .run("say No zombies nearby!")
        )
        self.assertEqual(
            str(cmd),
            "execute positioned 100 64 200 unless entity @e[type=minecraft:zombie] store result score @s zombie_count run say No zombies nearby!"
        )

    def test_example_4_chained_modifiers(self):
        """测试多个上下文修饰器的链式调用"""
        cmd = (
            Execute.execute()
            .as_("@e[type=minecraft:arrow]")
            .at("@s")
            .rotated_as("@p")
            .run("summon minecraft:fireball")
        )
        self.assertEqual(
            str(cmd),
            "execute as @e[type=minecraft:arrow] at @s rotated as @p run summon minecraft:fireball"
        )

    def test_example_5_store_block_data(self):
        """测试NBT数据存储到方块"""
        cmd = (
            Execute.execute()
            .store_result_block("~ ~-1 ~", "Items[0].Count", "byte", 1)
            .run("data get block ~ ~-2 ~ Items[0].Count")
        )
        self.assertEqual(
            str(cmd),
            "execute store result block ~ ~-1 ~ Items[0].Count byte 1 run data get block ~ ~-2 ~ Items[0].Count"
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)  # 显示详细测试结果
