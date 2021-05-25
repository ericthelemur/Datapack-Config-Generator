# Generated with ericthelemur's Datapack Settings Generator

tellraw @s ["\n", {"text":"Menu ", "bold":true, "clickEvent":{"action":"run_command","value":"/function full:config/pages/setpage_menu"},"hoverEvent":{"action":"show_text","contents":"Go to Menu"}}, {"text":" < ", "bold":true, "clickEvent":{"action":"run_command","value":"/function full:config/pages/setpage_1"},"hoverEvent":{"action":"show_text","contents":"Go to previous page"}}, {"text":"Second page", "hoverEvent":{"action":"show_text","contents":"Currently on page Second page"}}, {"text":" > ", "bold":true, "clickEvent":{"action":"run_command","value":"/function full:config/pages/setpage_3"},"hoverEvent":{"action":"show_text","contents":"Go to next page"}}, "\n"]
tellraw @s {"text":"More Text", "color":"#FF0000"}

# Toggle 2
execute unless score toggle2 enabled > zero constants run tellraw @s ["",{"text":"☒","color":"red","bold":true,"clickEvent":{"action":"run_command","value":"/function full:config/pages/enable/toggle2"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to enable ","color":"green"},"Toggle 2"]}},"Toggle 2"]
execute if score toggle2 enabled > zero constants run tellraw @s ["",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function full:config/pages/disable/toggle2"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"Toggle 2"]}},"Toggle 2"]

