from config import *
from utils import SB, make_file, scoreboards, players

class ConfigField:
    """Template class"""
    def render(self, indent=0):
        """Returns commands to include field in parent's text"""
        return ""

    def create_files(self, indent=0):
        """Generates the files required for field"""
        pass

    def set_dir(self, dir: str):
        if hasattr(self, "args"):
            self.args["directory"] = dir
            

class Config(ConfigField):
    """Root class of config"""
    def __init__(self, *contents):
        self.contents = contents

    def render(self, indent=0):
        for c in self.contents:
            print(c.render(indent=0))

    def create_files(self, indent=0):
        # Make config/config.mcfunction - just calls config/config/config.mcfunction
        make_file("../config.mcfunction", "# Generated with ericthelemur's Datapack Settings Generator\n\nfunction %s:config/config" % namespace, overwrite=True)

        # Fill out config function from contents
        with open("config.mcfunction", "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            for c in self.contents:
                print(c.render(indent=0), file=f)

        
        with open("load_config.mcfunction", "w", encoding="utf-8") as f:
            print("""scoreboard objectives add constants dummy
scoreboard players set zero constants 0

scoreboard objectives add %(root_sb)s dummy
scoreboard players operation %(root)s += zero constants
execute if score %(root)s = zero constants run function generated:config/init_config""" % {"root": datapack_scoreboard, "root_sb": datapack_scoreboard.scoreboard}, file=f)

        # Generate scoreboard initialization commands
        with open("init_config.mcfunction", "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            for s in scoreboards:
                print("\nscoreboard objectives add %s dummy" % s, file=f)
                for p, s1 in players:
                    if s == s1:
                        print("scoreboard players set %s %s %s" % (p, s1, players[(p, s1)]), file=f)

        # Generate uninstall scoreboard commands
        with open("uninstall_config.mcfunction", "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            # Objectives remove, ignore SBs in SBs_no_remove
            for s in scoreboards:
                if s not in SBs_no_remove:
                    print("scoreboard objectives remove %s" % s, file=f)
            # Players reset, ignore SBs in SBs_no_reset
            for p, s in players:
                if s in SBs_no_remove and s not in SBs_no_reset:
                    print("scoreboard players reset %s %s" % (p, s), file=f)


        for c in self.contents:
            c.create_files()

        print("Finished generating config files.")
        print("\nIf you did not generate the base datapack with this generator, these changes should be made:")
        print("\tAdded to load: function %s:config/load_config" % namespace)
        print("\tAdded to uninstall: function %s:config/uninstall_config" % namespace)
        print("\tWhen comparing a toggle setting, it is recommended to check it is <= or > 0 instead of = 1 or = 0, to allow for uninitialized values.")
        print("\t\tFor toggles: 0 = uninitialized, -1 = off, 1 = on, including datapack flag.")



class Foldable(ConfigField):
    """Toggle with dependent options contents, which get placed in function"""
    def __init__(self, label, sb: SB, function, fold_function, *contents, colour="white", enable_commands="", disable_commands=""):
        self.args = {"label": label, "sb_player": sb, "fold_function": fold_function, "function": function, "colour": colour, "namespace": namespace, "enable_commands": enable_commands, "disable_commands": disable_commands, "directory": ""}
        self.function = function
        self.contents = contents


    def render(self, indent=0):
        self.args["indent"] = " " * indent_size * indent
        # Option for folded and open, if open call sub-function
        return ("""# %(label)s"""
                + """\nexecute unless score %(sb_player)s > zero constants run tellraw @s ["%(indent)s",{"text":"▷ ","color":"red","clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)senable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to enable ","color":"green"},"%(label)s"]}},"%(label)s"]"""
                + """\nexecute if score %(sb_player)s > zero constants run tellraw @s ["%(indent)s",{"text":"☑","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)sdisable/%(function)s"},"hoverEvent":{"action":"show_text","contents":["",{"text":"Click to disable ","color":"red"},"%(label)s"]}},"%(label)s"]"""
                + """\nexecute if score %(sb_player)s > zero constants run function %(namespace)s:config/%(directory)s%(fold_function)s"""
                + "\n\n") % self.args


    def create_files(self, indent=0):
        # Toggle functions
        with open("enable/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            print("scoreboard players set %(sb_player)s 1\nfunction %(namespace)s:config" % self.args, file=f)
            if self.args["enable_commands"]: print(self.args["enable_commands"] % self.args, file=f)
            
        with open("disable/%(function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            print("scoreboard players set %(sb_player)s -1\nfunction %(namespace)s:config" % self.args, file=f)
            if self.args["disable_commands"]: print(self.args["disable_commands"] % self.args, file=f)

        # Create sub-function
        with open("%(fold_function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            for c in self.contents:
                print(c.render(indent=indent+1), file=f)
                c.create_files()
        
        print("Finished generating for foldable", self.args["label"])

    def set_dir(self, dir: str):
        super().set_dir(dir)

        for c in self.contents:
            c.set_dir(dir)
