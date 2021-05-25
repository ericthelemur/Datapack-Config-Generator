# Generated with ericthelemur's Datapack Settings Generator

tellraw @s ["\n", {"text":"Menu ", "bold":true, "clickEvent":{"action":"run_command","value":"/function full:config/pages/setpage_menu"},"hoverEvent":{"action":"show_text","contents":"Go to Menu"}}, {"text":" < ", "bold":true, "color": "gray"}, {"text":"First page", "hoverEvent":{"action":"show_text","contents":"Currently on page First page"}}, {"text":" > ", "bold":true, "clickEvent":{"action":"run_command","value":"/function full:config/pages/setpage_2"},"hoverEvent":{"action":"show_text","contents":"Go to next page"}}, "\n"]
# Fold
execute unless score fold enabled > zero constants run tellraw @s ["",{"text":"▷ ","color":"red","clickEvent":{"action":"run_command","value":"/function full:config/pages/enable/fold"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to enable ","color":"green"},"Fold"]}},"Fold"]
execute if score fold enabled > zero constants run tellraw @s ["",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function full:config/pages/disable/fold"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"Fold"]}},"Fold"]
execute if score fold enabled > zero constants run function full:config/pages/fold_config


