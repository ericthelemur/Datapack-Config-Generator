# Generated with ericthelemur's Datapack Settings Generator


# Toggle
execute unless score toggle enabled > zero constants run tellraw @s [" ",{"text":"☒","color":"red","bold":true,"clickEvent":{"action":"run_command","value":"/function generated:config/enable/toggle"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to enable ","color":"green"},"Toggle"]}},"Toggle"]
execute if score toggle enabled > zero constants run tellraw @s [" ",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function generated:config/disable/toggle"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"Toggle"]}},"Toggle"]

# Adjust
execute if score val1 values > zero constants if score val1 values < five constants run tellraw @s [" ",{"text":"☐","color":"gray","bold":true},"Adjust ", {"text":"-","color":"red","clickEvent":{"action":"run_command","value":"/function generated:config/dec/adjust"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to decrease Adjust by "},{"score":{"name":"one","objective":"constants"}}]}}, " ", {"score":{"name":"val1","objective":"values"}}, " ", {"text":"+","color":"green","clickEvent":{"action":"run_command","value":"/function generated:config/inc/adjust"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to increase Adjust by "},{"score":{"name":"one","objective":"constants"}}]}}]
execute unless score val1 values > zero constants if score val1 values < five constants run tellraw @s [" ",{"text":"☐","color":"gray","bold":true},"Adjust ", {"text":"-","color":"gray","hoverEvent":{"action":"show_text","contents":["",{"text":"Cannot decrease further"}]}}, " ", {"score":{"name":"val1","objective":"values"}}, " ", {"text":"+","color":"green","clickEvent":{"action":"run_command","value":"/function generated:config/inc/adjust"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to increase Adjust by "},{"score":{"name":"one","objective":"constants"}}]}}]
execute unless score val1 values < five constants if score val1 values > zero constants run tellraw @s [" ",{"text":"☐","color":"gray","bold":true},"Adjust ", {"text":"-","color":"red","clickEvent":{"action":"run_command","value":"/function generated:config/dec/adjust"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to decrease Adjust by "},{"score":{"name":"one","objective":"constants"}}]}}, " ", {"score":{"name":"val1","objective":"values"}}, " ", {"text":"+","color":"gray","hoverEvent":{"action":"show_text","contents":["",{"text":"Cannot increase further"}]}}]

# Adjust Toggle
execute unless score ad_tog enabled > zero constants run tellraw @s [" ",{"text":"☒","color":"red","bold":true,"clickEvent":{"action":"run_command","value":"/function generated:config/enable/ad_toggle"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to enable ","color":"green"},"Adjust Toggle"]}},"Adjust Toggle"]
execute if score ad_tog enabled > zero constants if score val2 values > one constants if score val2 values < twenty constants run tellraw @s [" ",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function generated:config/disable/ad_toggle"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"Adjust Toggle"]}},"Adjust Toggle ", {"text":"-","color":"red","clickEvent":{"action":"run_command","value":"/function generated:config/dec/ad_toggle"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to decrease Adjust Toggle by "},{"score":{"name":"five","objective":"constants"}}]}}, " ", {"score":{"name":"val2","objective":"values"}}, " ", {"text":"+","color":"green","clickEvent":{"action":"run_command","value":"/function generated:config/inc/ad_toggle"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to increase Adjust Toggle by "},{"score":{"name":"five","objective":"constants"}}]}}]
execute if score ad_tog enabled > zero constants unless score val2 values > one constants if score val2 values < twenty constants run tellraw @s [" ",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function generated:config/disable/ad_toggle"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"Adjust Toggle"]}},"Adjust Toggle ", {"text":"-","color":"gray","hoverEvent":{"action":"show_text","contents":["",{"text":"Cannot decrease further"}]}}, " ", {"score":{"name":"val2","objective":"values"}}, " ", {"text":"+","color":"green","clickEvent":{"action":"run_command","value":"/function generated:config/inc/ad_toggle"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to increase Adjust Toggle by "},{"score":{"name":"five","objective":"constants"}}]}}]
execute if score ad_tog enabled > zero constants unless score val2 values < twenty constants if score val2 values > one constants run tellraw @s [" ",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function generated:config/disable/ad_toggle"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"Adjust Toggle"]}},"Adjust Toggle ", {"text":"-","color":"red","clickEvent":{"action":"run_command","value":"/function generated:config/dec/ad_toggle"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to decrease Adjust Toggle by "},{"score":{"name":"five","objective":"constants"}}]}}, " ", {"score":{"name":"val2","objective":"values"}}, " ", {"text":"+","color":"gray","hoverEvent":{"action":"show_text","contents":["",{"text":"Cannot increase further"}]}}]
