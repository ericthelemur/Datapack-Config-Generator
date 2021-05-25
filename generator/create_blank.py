from config import namespace, author, datapack_scoreboard, line_colour
from utils import make_file, make_dir

# Creates a blank datapack, with template advancements
def create_blank():
    make_file("pack.mcmeta", '{ \n\t"pack": {\n\t\t"pack_format": 6,\n\t\t"description": "Datapack generated with ericthelemur''s config generator"\n\t}\n}')
    
    make_dir("data/minecraft/tags/functions")
    make_file("data/minecraft/tags/functions/load.json", '{\n\t"values": [\n\t\t"%s:load"\n\t]\n}' % namespace)
    make_file("data/minecraft/tags/functions/tick.json", '{\n\t"values": [\n\t\t"%s:tick"\n\t]\n}' % namespace)
    
    make_dir("data/global/advancements")
    make_file("data/global/advancements/root.json", '{\n\t"display": {\n\t\t"title": "Installed Datapacks",\n\t\t"description": "",\n\t\t"icon": {\n\t\t\t"item": "minecraft:knowledge_book"\n\t\t},\n\t\t"background": "minecraft:textures/block/gray_concrete.png",\n\t\t"show_toast": false,\n\t\t"announce_to_chat": false\n\t},\n\t"criteria": {\n\t\t"trigger": {\n\t\t\t"trigger": "minecraft:tick"\n\t\t}\n\t}\n}')
    make_file("data/global/advancements/%s.json" % author, '{\n\t"display": {\n\t\t"title": "%(author)s",\n\t\t"description": "",\n\t\t"icon": {\n\t\t\t"item": "minecraft:player_head",\n\t\t\t"nbt": "{SkullOwner: ''%(author)s''}"\n\t\t},\n\t\t"show_toast": false,\n\t\t"announce_to_chat": false\n\t},\n\n\t"parent": "global:root",\n\t"criteria": {\n\t\t"trigger": {\n\t\t\t"trigger": "minecraft:tick"\n\t\t}\n\t}\n}' % {"author": author})
    
    make_dir("data/%s/advancements" % namespace)
    make_file("data/%s/advancements/%s.json" % (namespace, namespace), '{\n\t"display": {\n\t\t"title": "Generated Datapack",\n\t\t"description": "Datapack generated by ericthelemur''s datapack config generator.",\n\t\t"icon": {\n\t\t\t"item": "minecraft:white_dye"\n\t\t},\n\t\t"announce_to_chat": false,\n\t\t"show_toast": false\n\t},\n\t"parent": "global:%s",\n\t"criteria": {\n\t\t"trigger": {\n\t\t\t"trigger": "minecraft:tick"\n\t\t}\n\t}\n}' % author)

    make_dir("data/%s/functions" % namespace)
    make_file("data/%s/functions/load.mcfunction" % namespace, "execute if score %s = zero constants run function %s:config/load_config" % (datapack_scoreboard, namespace))
    make_file("data/%s/functions/tick.mcfunction" % namespace, "")
    make_file("data/%s/functions/uninstall.mcfunction" % namespace, """function %(namespace)s:config/uninstall_config\nscoreboard players reset %(dp_sb)s\n\ntellraw @s {"text":"\\n                                                                                ","color":"%(line_colour)s","strikethrough":true}\ntellraw @s "Datapack uninstalled. Remove from datapacks folder before next restart or reload."\ntellraw @s {"text":"                                                                                ","color":"%(line_colour)s","strikethrough":true}""" % {"namespace": namespace, "line_colour": line_colour, "dp_sb": datapack_scoreboard})


    print("""
Template datapack created.
You now need to replace the placeholders in these files:
\tpack.mcmeta
\tdata/%s/advancements/%s.json
\t
""" % (namespace, namespace))