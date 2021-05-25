# Generated with ericthelemur's Datapack Settings Generator

# Header
tellraw @s {"text":"\n                                                                                ","color":"#808080","strikethrough":true}
tellraw @s [{"text":"            ETL Pages Example v0.0 - Config Menu","color":"#BBBBBB","bold":true}]
tellraw @s {"text":"                                                                                ","color":"#808080","strikethrough":true}

# Book pages/
function full:config/pages/main
tellraw @s {"text":"                                                                                ","color":"#808080","strikethrough":true}
tellraw @s ["",{"text":"◎","color":"dark_red","clickEvent":{"action":"run_command","value":"/function full:config/uninstall_verif"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to Uninstall ETL Config Example","color":"red"}]}}," Uninstall ETL Config Example"]
tellraw @s {"text":"                                                                                \n","color":"#808080","strikethrough":true}

