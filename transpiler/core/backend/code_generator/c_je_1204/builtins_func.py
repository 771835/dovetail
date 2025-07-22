# coding=utf-8
builtins_func = {
    "builtins/exec": "$$(command)",
    "builtins/strcat": "$data modify storage $(target) $(target_path) set value '$(dest)$(src)'",
    "builtins/int2str": "$data modify storage $(target) $(target_path) set value '$(value)'",
    "builtins/str2int": "$scoreboard players set $(target) $(objective) $(value)'",
}
