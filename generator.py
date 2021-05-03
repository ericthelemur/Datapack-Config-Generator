from pathlib import Path

Path("dec").mkdir(parents=True, exist_ok=True)
Path("inc").mkdir(parents=True, exist_ok=True)
Path("disable").mkdir(parents=True, exist_ok=True)
Path("enable").mkdir(parents=True, exist_ok=True)

# Name of your datapack (bit before :)
namespace = "generated"
line_colour = "#808080"
indent_size = 1

# See bottom of file for config layout

class ConfigField:
    """Template class"""
    def render(self, indent=0):
        return ""

    def create_files(self, indent=0):
        pass


class Config(ConfigField):
    """Root class"""
    def __init__(self, *contents):
        self.contents = contents

    def render(self, indent=0):
        for c in self.contents:
            print(c.render(indent=0))

    def create_files(self, indent=0):
        with open("config.mcfunction", "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            for c in self.contents:
                print(c.render(indent=0), file=f)

        for c in self.contents:
            c.create_files()


class Title(ConfigField):
    """Title banner at top"""
    def __init__(self, title, version, title_colour):
        self.args = {"title": f"{title} {version} - Config Menu".center(60).rstrip(), "version": version, "title_colour": title_colour, "line_colour": line_colour}

    def render(self, indent=0):
        return ("""# Header"""
              + """\ntellraw @s {"text":"\\n                                                                                ","color":"%(line_colour)s","strikethrough":true}"""
              + """\ntellraw @s [{"text":"%(title)s","color":"%(title_colour)s","bold":true}]"""
              + """\ntellraw @s {"text":"                                                                                ","color":"%(line_colour)s","strikethrough":true}"""
                ) % self.args


class SubTitle(ConfigField):
    """Bold text section"""
    def __init__(self, title, colour="white"):
        self.args = {"title": title, "colour": colour}

    def render(self, indent=0):
        self.args["indent"] = " " * indent_size * indent
        return """tellraw @s [{"text":"\\n%(indent)s%(title)s","bold":true,"color":"%(colour)s"}]""" % self.args


class Uninstall(ConfigField):
    """Uninstall banner at bottom"""
    def __init__(self, title):
        self.args = {"title": title, "line_colour": line_colour, "namespace": namespace}

    def render(self, indent=0):
        return ("""tellraw @s {"text":"                                                                                ","color":"%(line_colour)s","strikethrough":true}"""
              + """\ntellraw @s ["",{"text":"◎","color":"dark_red","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/uninstall_verif"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to Uninstall %(title)s","color":"red"}]}}," Uninstall %(title)s"]"""
              + """\ntellraw @s {"text":"                                                                                \\n","color":"%(line_colour)s","strikethrough":true}\n"""
        ) % self.args

    def create_files(self, indent=0):
        with open("uninstall_verif.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            print("""tellraw @s {"text":"\\n                                                                                ","color":"%(line_colour)s","strikethrough":true}""" % self.args, file=f)
            print("""tellraw @s ["", {"text":"Confirm uninstall of %(title)s?\\n    "},{"text":"Confirm Uninstall","color":"dark_red","underlined":true,"clickEvent":{"action":"run_command","value":"/function %(namespace)s:uninstall"},"hoverEvent":{"action":"show_text","contents":["",{"text":"This will remove all settings.","color":"red"}]}}]""" % self.args, file=f)
            print("""tellraw @s {"text":"                                                                                ","color":"%(line_colour)s","strikethrough":true}""" % self.args, file=f)
            

class Text(ConfigField):
    """Basic Text Field, text is passed into tellraw"""
    def __init__(self, text):
        self.args = {"text": text}

    def render(self, indent=0):
        return """tellraw @s %(text)s""" % self.args


class Toggle(ConfigField):
    """Tick/Cross toggle, toggles (scoreboard player) sb_player, and calls "config/enable/function" and "config/disable/function" when swapped to, which have basic switch command and extra from extra_en/disable_comm"""
    def __init__(self, label, sb_player, function, extra_enable_comm="", extra_disable_comm=""):
        self.args = {"label": label, "sb_player": sb_player, "function": function, "namespace": namespace, "extra_enable_comm": extra_enable_comm, "extra_disable_comm": extra_disable_comm}

    def render(self, indent=0):
        self.args["indent"] = " " * indent_size * indent
        return ("""\n# %(label)s"""
                + """\nexecute unless score %(sb_player)s > zero constants run tellraw @s ["%(indent)s",{"text":"☒","color":"red","bold":true,"clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/enable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to enable ","color":"green"},"%(label)s"]}},"%(label)s"]"""
                + """\nexecute if score %(sb_player)s > zero constants run tellraw @s ["%(indent)s",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/disable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"%(label)s"]}},"%(label)s"]"""
                + "\n") % self.args

    def create_files(self, indent=0):
        with open("enable/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["extra_enable_comm"]: print(self.args["extra_enable_comm"] % self.args, file=f)
            print("scoreboard players set %(sb_player)s 1\nfunction %(namespace)s:config" % self.args, file=f)
            
        with open("disable/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["extra_disable_comm"]: print(self.args["extra_disable_comm"] % self.args, file=f)
            print("scoreboard players set %(sb_player)s -1\nfunction %(namespace)s:config" % self.args, file=f)


class AdjustToggle(ConfigField):
    """Toggle with adjustment. Changes player adjust_pl in adjust_sb by inc_pl in inc_sb amount on +/-. Limited to max_sb/min_sb scoreboard values. On inc/dec, extra gets added too. Currently no case for min=max"""

    def __init__(self, label, sb_player, function, adjust_sb, adjust_pl, inc_sb, inc_pl, min_sb=None, max_sb=None, extra_enable_comm="", extra_disable_comm="", extra_inc_comm="", extra_dec_comm=""):
        self.args = {"label": label, "sb_player": sb_player, "function": function, "adjust_sb": adjust_sb, "adjust_pl": adjust_pl, "inc_sb": inc_sb, "inc_pl": inc_pl, "min_sb": min_sb, "max_sb": max_sb, "namespace": namespace, "extra_enable_comm": extra_enable_comm, "extra_disable_comm": extra_disable_comm, "extra_inc_comm": extra_inc_comm, "extra_dec_comm": extra_dec_comm}

    def render(self, indent=0):
        self.args["indent"] = " " * indent_size * indent
        
        self.args["filters"] = " "
        end = ""
        if self.args["min_sb"]:
            self.args["filters"] += "if score %(adjust_pl)s %(adjust_sb)s > %(min_sb)s " % self.args
            end += """\nexecute if score %(sb_player)s > zero constants unless score %(adjust_pl)s %(adjust_sb)s > %(min_sb)s """ + ("if score %(adjust_pl)s %(adjust_sb)s < %(max_sb)s " if self.args["max_sb"] else "") + """run tellraw @s ["%(indent)s",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/disable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"%(label)s"]}},"%(label)s ", {"text":"-","color":"gray","hoverEvent":{"action":"show_text","contents":["",{"text":"Cannot decrease further"}]}}, " ", {"score":{"name":"%(adjust_pl)s","objective":"%(adjust_sb)s"}}, " ", {"text":"+","color":"green","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/inc/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to increase %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}]"""

        if self.args["max_sb"]:
            self.args["filters"] += "if score %(adjust_pl)s %(adjust_sb)s < %(max_sb)s " % self.args
            end += """\nexecute if score %(sb_player)s > zero constants unless score %(adjust_pl)s %(adjust_sb)s < %(max_sb)s """ + ("if score %(adjust_pl)s %(adjust_sb)s > %(min_sb)s " if self.args["min_sb"] else "") + """run tellraw @s ["%(indent)s",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/disable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"%(label)s"]}},"%(label)s ", {"text":"-","color":"red","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/dec/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to decrease %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}, " ", {"score":{"name":"%(adjust_pl)s","objective":"%(adjust_sb)s"}}, " ", {"text":"+","color":"gray","hoverEvent":{"action":"show_text","contents":["",{"text":"Cannot increase further"}]}}]"""

        return ("""# %(label)s"""
                + """\nexecute unless score %(sb_player)s > zero constants run tellraw @s ["%(indent)s",{"text":"☒","color":"red","bold":true,"clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/enable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to enable ","color":"green"},"%(label)s"]}},"%(label)s"]"""
                + """\nexecute if score %(sb_player)s > zero constants%(filters)srun tellraw @s ["%(indent)s",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/disable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"%(label)s"]}},"%(label)s ", {"text":"-","color":"red","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/dec/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to decrease %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}, " ", {"score":{"name":"%(adjust_pl)s","objective":"%(adjust_sb)s"}}, " ", {"text":"+","color":"green","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/inc/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to increase %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}]"""
                + end + "\n") % self.args
    
    def create_files(self, indent=0):
        with open("enable/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["extra_enable_comm"]: print(self.args["extra_enable_comm"] % self.args, file=f)
            print("scoreboard players set %(sb_player)s 1\nfunction %(namespace)s:config" % self.args, file=f)
            
        with open("disable/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["extra_disable_comm"]: print(self.args["extra_disable_comm"] % self.args, file=f)
            print("scoreboard players set %(sb_player)s -1\nfunction %(namespace)s:config" % self.args, file=f)

        with open("inc/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["extra_inc_comm"]: print(self.args["extra_inc_comm"] % self.args, file=f)
            print("scoreboard players operation %(adjust_pl)s %(adjust_sb)s += %(inc_pl)s %(inc_sb)s\nfunction %(namespace)s:config" % self.args, file=f)
            
        with open("dec/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["extra_dec_comm"]: print(self.args["extra_dec_comm"] % self.args, file=f)
            print("scoreboard players operation %(adjust_pl)s %(adjust_sb)s -= %(inc_pl)s %(inc_sb)s\nfunction %(namespace)s:config" % self.args, file=f)



class Adjustable(ConfigField):
    """Add/subtract from value. Changes player adjust_pl in adjust_sb by inc_pl in inc_sb amount on +/-. Limited to max_sb/min_sb scoreboard values. On inc/dec, extra gets added too. Currently no case for min=max"""

    def __init__(self, label, function, adjust_sb, adjust_pl, inc_sb, inc_pl, min_sb=None, max_sb=None, extra_inc_comm="", extra_dec_comm=""):
        self.args = {"label": label, "function": function, "adjust_sb": adjust_sb, "adjust_pl": adjust_pl, "inc_sb": inc_sb, "inc_pl": inc_pl, "min_sb": min_sb, "max_sb": max_sb, "namespace": namespace, "extra_inc_comm": extra_inc_comm, "extra_dec_comm": extra_dec_comm}

    def render(self, indent=0):
        self.args["indent"] = " " * indent_size * indent
        
        self.args["filters"] = " "
        end = ""
        if self.args["min_sb"]:
            self.args["filters"] += "if score %(adjust_pl)s %(adjust_sb)s > %(min_sb)s " % self.args
            end += """\nexecute unless score %(adjust_pl)s %(adjust_sb)s > %(min_sb)s """ + ("if score %(adjust_pl)s %(adjust_sb)s < %(max_sb)s " if self.args["max_sb"] else "") + """run tellraw @s ["%(indent)s",{"text":"☐","color":"gray","bold":true},"%(label)s ", {"text":"-","color":"gray","hoverEvent":{"action":"show_text","contents":["",{"text":"Cannot decrease further"}]}}, " ", {"score":{"name":"%(adjust_pl)s","objective":"%(adjust_sb)s"}}, " ", {"text":"+","color":"green","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/inc/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to increase %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}]"""

        if self.args["max_sb"]:
            self.args["filters"] += "if score %(adjust_pl)s %(adjust_sb)s < %(max_sb)s " % self.args
            end += """\nexecute unless score %(adjust_pl)s %(adjust_sb)s < %(max_sb)s """ + ("if score %(adjust_pl)s %(adjust_sb)s > %(min_sb)s " if self.args["min_sb"] else "") + """run tellraw @s ["%(indent)s",{"text":"☐","color":"gray","bold":true},"%(label)s ", {"text":"-","color":"red","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/dec/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to decrease %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}, " ", {"score":{"name":"%(adjust_pl)s","objective":"%(adjust_sb)s"}}, " ", {"text":"+","color":"gray","hoverEvent":{"action":"show_text","contents":["",{"text":"Cannot increase further"}]}}]"""

        return ("""# %(label)s"""
                + """\nexecute%(filters)srun tellraw @s ["%(indent)s",{"text":"☐","color":"gray","bold":true},"%(label)s ", {"text":"-","color":"red","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/dec/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to decrease %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}, " ", {"score":{"name":"%(adjust_pl)s","objective":"%(adjust_sb)s"}}, " ", {"text":"+","color":"green","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/inc/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to increase %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}]"""
                + end + "\n") % self.args
    
    def create_files(self, indent=0):
        with open("inc/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["extra_inc_comm"]: print(self.args["extra_inc_comm"] % self.args, file=f)
            print("scoreboard players operation %(adjust_pl)s %(adjust_sb)s += %(inc_pl)s %(inc_sb)s\nfunction %(namespace)s:config" % self.args, file=f)
            
        with open("dec/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["extra_dec_comm"]: print(self.args["extra_dec_comm"] % self.args, file=f)
            print("scoreboard players operation %(adjust_pl)s %(adjust_sb)s -= %(inc_pl)s %(inc_sb)s\nfunction %(namespace)s:config" % self.args, file=f)



class Foldable(ConfigField):
    """Toggle with dependent options contents, which get placed in function"""
    def __init__(self, label, sb_player, function, fold_function, *contents, colour="white", extra_enable_comm="", extra_disable_comm=""):
        self.args = {"label": label, "sb_player": sb_player, "fold_function": fold_function, "function": function, "colour": colour, "namespace": namespace, "extra_enable_comm": extra_enable_comm, "extra_disable_comm": extra_disable_comm}
        self.function = function
        self.contents = contents


    def render(self, indent=0):
        self.args["indent"] = " " * indent_size * indent
        return ("""# %(label)s"""
                + """\nexecute unless score %(sb_player)s > zero constants run tellraw @s ["%(indent)s",{"text":"▷ ","color":"red","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/enable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to enable ","color":"green"},"%(label)s"]}},"%(label)s"]"""
                + """\nexecute if score %(sb_player)s > zero constants run tellraw @s ["%(indent)s",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/disable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"%(label)s"]}},"%(label)s"]"""
                + """\nexecute if score %(sb_player)s > zero constants run function %(namespace)s:config/%(fold_function)s"""
                + "\n\n") % self.args


    def create_files(self, indent=0):
        with open("enable/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            print("scoreboard players set %(sb_player)s 1\nfunction %(namespace)s:config" % self.args, file=f)
            if self.args["extra_enable_comm"]: print(self.args["extra_enable_comm"] % self.args, file=f)
            
        with open("disable/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            print("scoreboard players set %(sb_player)s -1\nfunction %(namespace)s:config" % self.args, file=f)
            if self.args["extra_disable_comm"]: print(self.args["extra_disable_comm"] % self.args, file=f)
            
        with open("%(fold_function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            for c in self.contents:
                print(c.render(indent=indent+1), file=f)
                c.create_files()



# Example
Config(
    Title("ETL Config Example", "v0.0", "#101010"),
    Text("{\"text\":\"Text\", \"color\":\"#FF0000\"}"),
    SubTitle("Subtitle"),

    Foldable("Fold", "fold enabled", "fold", "fold_config",

        Toggle("Toggle", "toggle enabled", "toggle", 
                extra_enable_comm="tellraw @s \"toggle enabled\"", 
                extra_disable_comm="tellraw @s \"toggle disabled\""),
        
        Adjustable("Adjust", "adjust", "values", "val1", "constants", "one", 
                                min_sb="zero constants", max_sb="five constants"),
        
        AdjustToggle("Adjust Toggle", "ad_tog enabled", "ad_toggle", "values", "val2", "constants", "five", 
                            min_sb="one constants", max_sb="twenty constants",
                            extra_enable_comm="tellraw @s \"adj toggle enabled\"",
                            extra_inc_comm="tellraw @s \"adj toggle increased\""),
    ),
    Uninstall("ETL Config Example")
).create_files()

# Still need to: 
# Create enabled scoreboard and initialize values. 0 = uninitialized, -1 = off, 1 = on. Can add zero to a value to create it if unsure
# Create uninstall function in namespace:uninstall
# This generator makes use of a zero constants in scoreboard constants
# Use if name scoreboard > zero constants instead of checking = 0 so can have -1