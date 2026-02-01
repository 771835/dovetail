# coding=utf-8
from .template import CommandTemplate, TemplateRegistry


def register_builtin_templates():
    """注册所有内置模板"""

    templates = [
        # ============ 基础命令 ============
        CommandTemplate(
            name="exec",
            template="$(command)",
            function_path="builtins/exec",
            param_names=["command"],
            description="执行原始 Minecraft 命令",
            tags=["basic", "core"]
        ),

        CommandTemplate(
            name="strcat",
            template="data modify storage $(target) $(target_path) set value '$(dest)$(src)'",
            function_path="builtins/strcat",
            param_names=["target", "target_path", "dest", "src"],
            description="字符串拼接",
            tags=["data", "string"]
        ),

        # ============ Tellraw 系列 ============
        CommandTemplate(
            name="tellraw_nbt",
            template='tellraw $(target) {"storage":"$(objective)","nbt":"$(path)"}',
            function_path="builtins/tellraw/tellraw_nbt",
            param_names=["target", "objective", "path"],
            description="向指定目标发送指定nbt路径中的文本消息",
            tags=["ui", "tellraw"]
        ),

        CommandTemplate(
            name="tellraw",
            template="tellraw $(target) $(json)",
            function_path="builtins/tellraw/tellraw",
            param_names=["target", "json"],
            description="向指定目标发送文本组件(1.21.5及以上)/json(1.21.5以下)",
            tags=["ui", "tellraw"]
        ),

        CommandTemplate(
            name="tellraw_json_all",
            template="tellraw @a $(json)",
            function_path="builtins/tellraw/tellraw_json_all",
            param_names=["json"],
            description="向所有玩家发送 JSON 消息",
            tags=["ui", "tellraw", "shortcut"]
        ),

        CommandTemplate(
            name="tellraw_json_self",
            template="tellraw @s $(json)",
            function_path="builtins/tellraw/tellraw_json_self",
            param_names=["json"],
            description="向目标执行者发送 JSON 消息",
            tags=["ui", "tellraw", "shortcut"]
        ),

        CommandTemplate(
            name="tellraw_json_entities",
            template="tellraw @e $(json)",
            function_path="builtins/tellraw/tellraw_json_entities",
            param_names=["json"],
            description="向所有实体发送 JSON 消息",
            tags=["ui", "tellraw", "shortcut"]
        ),

        CommandTemplate(
            name="tellraw_json_nearest",
            template="tellraw @n $(json)",
            function_path="builtins/tellraw/tellraw_json_nearest",
            param_names=["json"],
            description="向最近的实体发送 JSON 消息",
            tags=["ui", "tellraw", "shortcut"]
        ),

        CommandTemplate(
            name="tellraw_json_nearest_player",
            template="tellraw @p $(json)",
            function_path="builtins/tellraw/tellraw_json_nearest_player",
            param_names=["json"],
            description="向最近的玩家发送 JSON 消息",
            tags=["ui", "tellraw", "shortcut"]
        ),

        CommandTemplate(
            name="tellraw_json_random",
            template="tellraw @r $(json)",
            function_path="builtins/tellraw/tellraw_json_random",
            param_names=["json"],
            description="向随机玩家发送 JSON 消息",
            tags=["ui", "tellraw", "shortcut"]
        ),

        # ============ Random 系列 ============
        CommandTemplate(
            name="random_score",
            template="execute store result score $(target) $(objective) run random value $(min)..$(max)",
            function_path="builtins/random/random_value_score",
            param_names=["target", "objective", "min", "max"],
            description="生成随机数到记分板",
            tags=["random", "scoreboard"],
            validator=lambda p: (
                int(p['min']) <= int(p['max']),
                "min must be less than or equal to max"
            )
        ),

        CommandTemplate(
            name="random_storage",
            template="execute store result storage $(target) $(target_path) int 1.0 run random value $(min)..$(max)",
            function_path="builtins/random/random_value_storage",
            param_names=["target", "target_path", "min", "max"],
            description="生成随机数到存储",
            tags=["random", "storage"]
        ),

        # ============ Setblock 系列 ============
        CommandTemplate(
            name="setblock",
            template="setblock $(x) $(y) $(z) $(block) $(mode)",
            function_path="builtins/setblock/setblock_a",
            param_names=["x", "y", "z", "block"],
            optional_params={"mode": "replace"},
            description="放置方块",
            tags=["world", "block"]
        ),

        CommandTemplate(
            name="setblock_destroy",
            template="setblock $(x) $(y) $(z) $(block) destroy",
            function_path="builtins/setblock/setblock_d",
            param_names=["x", "y", "z", "block"],
            description="破坏性放置方块",
            tags=["world", "block"]
        ),

        # ============ List 操作 ============
        CommandTemplate(
            name="list_setitem",
            template="data modify storage $(target) object.$(id).value[$(index)] set value $(value)",
            function_path="builtins/data/list_setitem_value",
            param_names=["target", "id", "index", "value"],
            description="设置列表元素",
            tags=["data", "list"]
        ),

        CommandTemplate(
            name="list_getitem",
            template="data modify storage $(target) $(target_path) set from storage $(source) object.$(id).value[$(index)]",
            function_path="builtins/data/list_getitem_storage",
            param_names=["target", "target_path", "source", "id", "index"],
            description="获取列表元素",
            tags=["data", "list"]
        ),

        # ============ OOP 系列 ============
        CommandTemplate(
            name="oop_get_property_score",
            template="execute store result score $(target) $(objective) run data get storage $(source) object.$(id).$(property) 1",
            function_path="builtins/oop/get_property_score",
            param_names=["target", "objective", "source", "id", "property"],
            description="获取对象属性到记分板",
            tags=["oop", "property"]
        ),

        CommandTemplate(
            name="oop_set_property_value",
            template='data modify storage $(target) object.$(id).$(property) set value "$(value)"',
            function_path="builtins/oop/set_property_storage_value",
            param_names=["target", "id", "property", "value"],
            description="设置对象属性值",
            tags=["oop", "property"]
        ),

        # ============ 实体操作 ============
        CommandTemplate(
            name="tp",
            template="tp $(target) $(x) $(y) $(z)",
            function_path="builtins/tp",
            param_names=["target", "x", "y", "z"],
            optional_params={"rotation": None},
            description="传送实体",
            tags=["entity", "world"]
        ),

        CommandTemplate(
            name="summon",
            template="summon $(entity_type) $(x) $(y) $(z) $(nbt)",
            function_path="builtins/summon",
            param_names=["entity_type", "x", "y", "z"],
            optional_params={"nbt": "{}"},
            description="生成实体",
            tags=["entity", "world"]
        ),

        CommandTemplate(
            name="kill",
            template="kill $(target)",
            function_path="builtins/kill",
            param_names=["target"],
            description="杀死实体",
            tags=["entity"]
        ),

        # ============ 世界操作 ============
        CommandTemplate(
            name="time_set",
            template="time set $(value)",
            function_path="builtins/time_set",
            param_names=["value"],
            description="设置世界时间",
            tags=["world", "time"]
        ),

        CommandTemplate(
            name="weather",
            template="weather $(type) $(duration)",
            function_path="builtins/weather",
            param_names=["type"],
            optional_params={"duration": ""},
            description="设置天气",
            tags=["world", "weather"]
        ),
    ]

    # 批量注册
    for template in templates:
        TemplateRegistry.register(template)
