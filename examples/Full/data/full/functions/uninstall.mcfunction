function full:config/uninstall_config
scoreboard players reset full enabled

tellraw @s {"text":"\n                                                                                ","color":"#808080","strikethrough":true}
tellraw @s "Datapack uninstalled. Remove from datapacks folder before next restart or reload."
tellraw @s {"text":"                                                                                ","color":"#808080","strikethrough":true}