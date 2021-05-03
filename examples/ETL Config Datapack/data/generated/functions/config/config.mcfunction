# Generated with ericthelemur's Datapack Settings Generator

# Header
tellraw @s {"text":"\n                                                                                ","color":"#808080","strikethrough":true}
tellraw @s [{"text":"           ETL Config Example v0.0 - Config Menu","color":"#101010","bold":true}]
tellraw @s {"text":"                                                                                ","color":"#808080","strikethrough":true}
tellraw @s {"text":"Text", "color":"#FF0000"}
tellraw @s [{"text":"\nSubtitle","bold":true,"color":"white"}]
# Fold
execute unless score fold enabled > zero constants run tellraw @s ["",{"text":"▷ ","color":"red","clickEvent":{"action":"run_command","value":"/function generated:config/enable/fold"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to enable ","color":"green"},"Fold"]}},"Fold"]
execute if score fold enabled > zero constants run tellraw @s ["",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function generated:config/disable/fold"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"Fold"]}},"Fold"]
execute if score fold enabled > zero constants run function generated:config/fold_config


tellraw @s {"text":"                                                                                ","color":"#808080","strikethrough":true}
tellraw @s ["",{"text":"◎","color":"dark_red","clickEvent":{"action":"run_command","value":"/function generated:config/uninstall_verif"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to Uninstall ETL Config Example","color":"red"}]}}," Uninstall ETL Config Example"]
tellraw @s {"text":"                                                                                \n","color":"#808080","strikethrough":true}

