from config_fields.config_base import ConfigField
from config import *
from utils import SB

class Toggle(ConfigField):
    """Tick/Cross toggle, toggles (scoreboard player) sb_player, and calls "config/enable/function" and "config/disable/function" when swapped to, which have basic switch command and extra from extra_en/disable_comm"""
    def __init__(self, label: str, sb: SB, function: str, enable_commands: str = "", disable_commands: str = ""):
        self.args = {"label": label, "sb": sb, "function": function, "namespace": namespace, "enable_commands": enable_commands, "disable_commands": disable_commands, "directory": ""}

    def render(self, indent=0):
        # Line for each enabled and disabled
        self.args["indent"] = " " * indent_size * indent
        return ("""\n# %(label)s"""
                + """\nexecute unless score %(sb)s > zero constants run tellraw @s ["%(indent)s",{"text":"☒","color":"red","bold":true,"clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)senable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to enable ","color":"green"},"%(label)s"]}},"%(label)s"]"""
                + """\nexecute if score %(sb)s > zero constants run tellraw @s ["%(indent)s",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)sdisable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"%(label)s"]}},"%(label)s"]"""
                + "\n") % self.args

    def create_files(self, indent=0):
        # Enable function
        with open("enable/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["enable_commands"]: print(self.args["enable_commands"] % self.args, file=f)
            print("scoreboard players set %(sb)s 1\nfunction %(namespace)s:config" % self.args, file=f)
        
        # Disable function
        with open("disable/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["disable_commands"]: print(self.args["disable_commands"] % self.args, file=f)
            print("scoreboard players set %(sb)s -1\nfunction %(namespace)s:config" % self.args, file=f)


class Adjustable(ConfigField):
    """Add/subtract from value. Changes player adjust_pl in adjust_sb by inc_pl in inc_sb amount on +/-. Limited to max_sb/min_sb scoreboard values. On inc/dec, extra gets added too. Currently no case for min=max"""

    def __init__(self, label, adjust_sb: SB, function, inc_sb: SB, min_sb: SB = None, max_sb: SB = None, inc_commands="", dec_commands=""):
        self.args = {"label": label, "function": function, "adjust_sb": adjust_sb.scoreboard, "adjust_pl": adjust_sb.player, "inc_sb": inc_sb.scoreboard, "inc_pl": inc_sb.player, "min_sb": min_sb, "max_sb": max_sb, "namespace": namespace, "inc_commands": inc_commands, "dec_commands": dec_commands, "directory": ""}

    def render(self, indent=0):
        self.args["indent"] = " " * indent_size * indent
        
        self.args["filters"] = " "
        end = ""
        # If min_sb set, add check to basic call and add line for at min
        if self.args["min_sb"]:
            self.args["filters"] += "if score %(adjust_pl)s %(adjust_sb)s > %(min_sb)s " % self.args
            end += """\nexecute unless score %(adjust_pl)s %(adjust_sb)s > %(min_sb)s """ + ("if score %(adjust_pl)s %(adjust_sb)s < %(max_sb)s " if self.args["max_sb"] else "") + """run tellraw @s ["%(indent)s",{"text":"☐","color":"gray","bold":true},"%(label)s ", {"text":"-","color":"gray","hoverEvent":{"action":"show_text","contents":["",{"text":"Cannot decrease further"}]}}, " ", {"score":{"name":"%(adjust_pl)s","objective":"%(adjust_sb)s"}}, " ", {"text":"+","color":"green","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)sinc/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to increase %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}]"""

        # If max_sb set, add check to basic call and add line for at max
        if self.args["max_sb"]:
            self.args["filters"] += "if score %(adjust_pl)s %(adjust_sb)s < %(max_sb)s " % self.args
            end += """\nexecute unless score %(adjust_pl)s %(adjust_sb)s < %(max_sb)s """ + ("if score %(adjust_pl)s %(adjust_sb)s > %(min_sb)s " if self.args["min_sb"] else "") + """run tellraw @s ["%(indent)s",{"text":"☐","color":"gray","bold":true},"%(label)s ", {"text":"-","color":"red","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)sdec/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to decrease %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}, " ", {"score":{"name":"%(adjust_pl)s","objective":"%(adjust_sb)s"}}, " ", {"text":"+","color":"gray","hoverEvent":{"action":"show_text","contents":["",{"text":"Cannot increase further"}]}}]"""

        # Basic call with toggle, inserts min and max filter if appropriate
        return ("""# %(label)s"""
                + """\nexecute%(filters)srun tellraw @s ["%(indent)s",{"text":"☐","color":"gray","bold":true},"%(label)s ", {"text":"-","color":"red","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)sdec/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to decrease %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}, " ", {"score":{"name":"%(adjust_pl)s","objective":"%(adjust_sb)s"}}, " ", {"text":"+","color":"green","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)sinc/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to increase %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}]"""
                + end + "\n") % self.args
    
    def create_files(self, indent=0):
        with open("inc/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["inc_commands"]: print(self.args["inc_commands"] % self.args, file=f)
            print("scoreboard players operation %(adjust_pl)s %(adjust_sb)s += %(inc_pl)s %(inc_sb)s\nfunction %(namespace)s:config" % self.args, file=f)
            
        with open("dec/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["dec_commands"]: print(self.args["dec_commands"] % self.args, file=f)
            print("scoreboard players operation %(adjust_pl)s %(adjust_sb)s -= %(inc_pl)s %(inc_sb)s\nfunction %(namespace)s:config" % self.args, file=f)


class AdjustToggle(ConfigField):
    """Toggle with adjustment. Changes player adjust_pl in adjust_sb by inc_pl in inc_sb amount on +/-. Limited to max_sb/min_sb scoreboard values. On inc/dec, extra gets added too. Currently no case for min=max"""

    def __init__(self, label, toggle_sb: SB, function, adjust_sb: SB, inc_val_sb: SB, min_sb: SB = None, max_sb: SB = None, enable_commands="", disable_commands="", inc_commands="", dec_commands=""):
        self.args = {"label": label, "sb": toggle_sb, "function": function, "adjust": adjust_sb, "adjust_sb": adjust_sb.scoreboard, "adjust_pl": adjust_sb.player, "inc": inc_val_sb, "inc_sb": inc_val_sb.scoreboard, "inc_pl": inc_val_sb.player, "min_sb": min_sb, "max_sb": max_sb, "namespace": namespace, "enable_commands": enable_commands, "disable_commands": disable_commands, "inc_commands": inc_commands, "dec_commands": dec_commands, "directory": ""}

    def render(self, indent=0):
        self.args["indent"] = " " * indent_size * indent
        
        self.args["filters"] = " "
        end = ""
        # If min_sb set, add check to basic call and add line for at min
        if self.args["min_sb"]:
            self.args["filters"] += "if score %(adjust)s > %(min_sb)s " % self.args
            end += """\nexecute if score %(sb)s > zero constants unless score %(adjust)s > %(min_sb)s """ + ("if score %(adjust)s < %(max_sb)s " if self.args["max_sb"] else "") + """run tellraw @s ["%(indent)s",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)sdisable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"%(label)s"]}},"%(label)s ", {"text":"-","color":"gray","hoverEvent":{"action":"show_text","contents":["",{"text":"Cannot decrease further"}]}}, " ", {"score":{"name":"%(adjust_pl)s","objective":"%(adjust_sb)s"}}, " ", {"text":"+","color":"green","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)sinc/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to increase %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}]"""

        # If max_sb set, add check to basic call and add line for at max
        if self.args["max_sb"]:
            self.args["filters"] += "if score %(adjust)s < %(max_sb)s " % self.args
            end += """\nexecute if score %(sb)s > zero constants unless score %(adjust)s < %(max_sb)s """ + ("if score %(adjust)s > %(min_sb)s " if self.args["min_sb"] else "") + """run tellraw @s ["%(indent)s",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)sdisable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"%(label)s"]}},"%(label)s ", {"text":"-","color":"red","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)sdec/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to decrease %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}, " ", {"score":{"name":"%(adjust_pl)s","objective":"%(adjust_sb)s"}}, " ", {"text":"+","color":"gray","hoverEvent":{"action":"show_text","contents":["",{"text":"Cannot increase further"}]}}]"""

        # Basic call with toggle, inserts min and max filter if appropriate
        return ("""# %(label)s"""
                + """\nexecute unless score %(sb)s > zero constants run tellraw @s ["%(indent)s",{"text":"☒","color":"red","bold":true,"clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)senable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to enable ","color":"green"},"%(label)s"]}},"%(label)s"]"""
                + """\nexecute if score %(sb)s > zero constants%(filters)srun tellraw @s ["%(indent)s",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)sdisable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"%(label)s"]}},"%(label)s ", {"text":"-","color":"red","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)sdec/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to decrease %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}, " ", {"score":{"name":"%(adjust_pl)s","objective":"%(adjust_sb)s"}}, " ", {"text":"+","color":"green","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)sinc/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to increase %(label)s by "},{"score":{"name":"%(inc_pl)s","objective":"%(inc_sb)s"}}]}}]"""
                + end + "\n") % self.args
    
    def create_files(self, indent=0):
        # Toggle files
        with open("enable/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["enable_commands"]: print(self.args["enable_commands"] % self.args, file=f)
            print("scoreboard players set %(sb)s 1\nfunction %(namespace)s:config" % self.args, file=f)
            
        with open("disable/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["disable_commands"]: print(self.args["disable_commands"] % self.args, file=f)
            print("scoreboard players set %(sb)s -1\nfunction %(namespace)s:config" % self.args, file=f)

        # Adjust files
        with open("inc/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["inc_commands"]: print(self.args["inc_commands"] % self.args, file=f)
            print("scoreboard players operation %(adjust)s += %(inc)s\nfunction %(namespace)s:config" % self.args, file=f)
            
        with open("dec/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            if self.args["dec_commands"]: print(self.args["dec_commands"] % self.args, file=f)
            print("scoreboard players operation %(adjust)s -= %(inc)s\nfunction %(namespace)s:config" % self.args, file=f)




class Choice:
    def __init__(self, label, func_name, value: int, extra_commands=""):
        self.args = {"ch_label": label, "ch_func_name": func_name, "ch_value": value, "ch_extra_commands": extra_commands}
        

class Select(ConfigField):
    def __init__(self, label, sb: SB, choices: list[Choice], on_change=""):
        self.args = {"label": label, "sb": sb, "on_change": on_change, "namespace": namespace, "directory": ""}
        self.choices = choices

    def render(self, indent=0):
        self.args["indent"] = " " * indent_size * indent
        for c in self.choices:
            c.args |= self.args

        commands = """\n# %(label)s""" % self.args
        
        # exceptions = ["unless score %(sb)s matches %(value)s " % (self.args | c.args) for c in self.choices]
        selects = [""", " ", {"text":"[ %(ch_label)s ]","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)ssel/%(ch_func_name)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to set %(label)s to %(ch_label)s "}]}}""" % c.args for c in self.choices]


        for i, choice in enumerate(self.choices):
            # c_exp = "".join(e for j, e in enumerate(exceptions) if i != j)
            # %(exp)s ; | {"exp": c_exp}
            commands += ("""\nexecute if score %(sb)s matches %(ch_value)s run tellraw @s ["%(indent)s", {"text":"☐","color":"gray","bold":true}, "%(label)s" """ +
                            ("".join(selects[:i])) + 
                            """, " ", {"text":"[ %(ch_label)s ]","color":"green","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)ssel/%(ch_func_name)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to set %(label)s to %(ch_label)s "}]}}""" + 
                            ("".join(selects[(i+1):])) + "]") % choice.args
            
        commands += "\n"
        return commands

    def create_files(self):
        for choice in self.choices:
            with open("sel/%(ch_func_name)s.mcfunction" % choice.args, "w", encoding="utf-8") as f:
                print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
                if self.args["on_change"]: print(self.args["on_change"] % choice.args, file=f)
                if choice.args["ch_extra_commands"]: print(choice.args["ch_extra_commands"]% choice.args, file=f)
                print("scoreboard players set %(sb)s %(ch_value)s\nfunction %(namespace)s:config" % choice.args, file=f)
