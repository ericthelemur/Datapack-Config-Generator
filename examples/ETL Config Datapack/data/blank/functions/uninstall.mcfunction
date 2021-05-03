# Remove scoreboards and residual entities etc.

scoreboard players reset blank enabled

tellraw @s {"text":"\n                                                                                ","color":"#808080","strikethrough":true}
tellraw @s ["", {"text":"Blank Example has been Uninstalled","hoverEvent":{"action":"show_text","contents":["",{"text":"Remove this folder from world/datapacks to complete.","color":"red"}]}}]
tellraw @s {"text":"                                                                                \n","color":"#808080","strikethrough":true}