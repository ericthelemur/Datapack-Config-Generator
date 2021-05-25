from utils import SB

# Name of your datapack (bit before :)
namespace = "blank"
# Your name
author = "ericthelemur"
# Horizontal bar colour
line_colour = "#808080"
# Number of spaces per indent
indent_size = 1

# Scoreboard value signifiying pack enabled/install
# In general 0 = uninitialized, -1 = off, 1 = on
datapack_scoreboard = SB(namespace, "enabled", 1)

# List of scoreboards to not delete on uninstall
SBs_no_remove = ("enabled", "constants")
# List of scoreboards to not reset players on uninstall
SBs_no_reset = ("constants")

from config_fields.config_base import *
from config_fields.config_interactable import *
from config_fields.config_pages import *
from config_fields.config_text import *


config = Config(
    Title("ETL Pages Example", "v0.0", "#BBBBBB"),
    Book([
        Page("First page", "1", [
            Foldable("Fold", SB("fold", "enabled", 1), "fold", "fold_config",
                Toggle("Toggle", SB("toggle", "enabled", 1), "toggle", 
                       enable_commands="tellraw @s \"toggle enabled\"", 
                       disable_commands="tellraw @s \"toggle disabled\""),
                
                Adjustable("Adjust", SB("val1", "values", 5), "adjust", SB("one", "constants", 1), 
                           min_sb=SB("zero", "constants", 0), max_sb=SB("five", "constants", 5)),
                
                AdjustToggle("Adjust Toggle", SB("ad_tog", "enabled", 1), "ad_toggle", SB("val2", "values", 5), SB("five", "constants"), 
                             min_sb=SB("zero", "constants", 0),
                             enable_commands="tellraw @s \"adj toggle enabled\"",
                             inc_commands="tellraw @s \"adj toggle increased\""),
            )
        ]),
        Page("Second page", "2", [
            Text("{\"text\":\"More Text\", \"color\":\"#FF0000\"}"),
            Toggle("Toggle 2", SB("toggle2", "enabled", 1), "toggle2"),
        ]),
        Page("Third page", "3", [
            Text("{\"text\":\"Yet More Text\", \"color\":\"#FF0000\"}"),
            Adjustable("Adjust", SB("val3", "values", 5), "adjust2", SB("one", "constants", 1), 
                       min_sb=SB("zero", "constants", 0), max_sb=SB("five", "constants", 5)),
        ])
    ], SB("menu", "pages", 0)),
    Uninstall("ETL Config Example")
)


# Example without pages
"""
config = Config(
    Title("ETL Config Example", "v0.0", "#101010"),
    Text("{\"text\":\"Text\", \"color\":\"#FF0000\"}"),
    SubTitle("Subtitle"),

    Foldable("Fold", SB("fold", "enabled", 1), "fold", "fold_config",

        Toggle("Toggle", SB("toggle", "enabled", 1), "toggle", 
                enable_commands="tellraw @s \"toggle enabled\"", 
                disable_commands="tellraw @s \"toggle disabled\""),
    
        Adjustable("Adjust", SB("val1", "values", 5), "adjust", SB("one", "constants", 1), 
                                min_sb=SB("zero", "constants", 0), max_sb=SB("five", "constants", 5)),
    
        AdjustToggle("Adjust Toggle", SB("ad_tog", "enabled", 1), "ad_toggle", SB("val2", "values", 5), SB("five", "constants"), 
                            min_sb=SB("zero", "constants", 0), max_sb=SB("twenty", "constants", 20),
                            enable_commands="tellraw @s \"adj toggle enabled\"",
                            inc_commands="tellraw @s \"adj toggle increased\""),
    ),
    Uninstall("ETL Config Example")
)
"""