# Datapack Config Generator
This python script generates a datapack config menu with options for toggles, adjustable values (integers), folding sections and uninstall section.

## Example
<IMG>


## Usage
The config is generated by running `generator.py` in `functions/config`. This script also requires you to make a `uninstall` function, which is run on uninstall being confirmed. 

A root `config` function calling `config/config` is also recommended, and to initialize config values and scoreboards on loading, an `initialize` function is recommended, to be called on the first run.

The `examples/ETL Config/data/blank` example demonstrates an example set up before running `generator.py`, and `examples/ETL Config/data/generated` shows the same example after running.

In this example, settings `generator.py` to load:
```py
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
```
Generates
<IMG>

`extra_xxx_comm` are extra commands to run on enable, disable, increase or decrease as required. My ETL Utils Datapack shows this all in use.
Some scoreboard values want both scoreboard and value in one string and some separate. Where possible I have combined them, though some commands make that impossible.