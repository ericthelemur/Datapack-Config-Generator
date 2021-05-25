from config_fields.config_base import ConfigField
from config import *

class Title(ConfigField):
    """Title banner at top"""
    def __init__(self, title, version, title_colour):
        self.args = {"title": f"{title} {version} - Config Menu".center(60).rstrip(), "version": version, "title_colour": title_colour, "line_colour": line_colour}

    def render(self, indent=0):
        # Title with lines above and below
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
    """Uninstall banner at bottom, ultimately calls namespace:uninstall"""
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
