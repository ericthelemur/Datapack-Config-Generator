# Datapack Config Generator
This python script generates a datapack config menu with options for toggles, adjustable values (integers), folding sections and uninstall section.  
Version 1.1: Added config pages, as displayed at the bottom of this document.

## Example
![image](https://user-images.githubusercontent.com/8903016/116833210-d10f4f00-abaf-11eb-8c81-2f7241a65e1e.png)


## Usage
The generator is run with `python generator.py` pointed to the root directory of your datapack (where `pack.mcmeta` is). The path can be passed in as the only argument to the program, e.g. `python generator.py "../datapack"`.  
Options can be changed in the file `config.py`, in which you specify the options available and formatting of them.

If the program is run with the `-c` option, it will generate a template datapack (without any config settings), e.g. `python generator.py -c "../datapack"`, optionally given with the path as well. This includes the necessary advancements to display the pack's installation, and a `load` and `uninstall` function ready for the configs. No existing files will be deleted in this process. 

If you run the generator from inside the datapacks, as given in the examples, they are run with path `..`, and if you have the generator directory outside the datapack, it needs the path `<datapack>`.

3 examples are included:  
- **Blank:** this is the base generator, with no datapack generated
- **Template:** this is the result after `python generator.py -c ..` is run from the blank example.
- **Full:** this is the result after `python generator.py ..` is run on the template example. This includes the full settings menu, including a `init_config` function to initialize the config's values.


In this example, settings `config.py` to:
```py
namespace = "generated"
author = "ericthelemur"
line_colour = "#808080"
indent_size = 1

# Scoreboard value signifiying pack enabled/install
# In general 0 = uninitialized, -1 = off, 1 = on
datapack_scoreboard = SB(namespace, "enabled", 1)

# List of scoreboards to not delete on uninstall
SBs_no_remove = ("enabled", "constants")
# List of scoreboards to not reset players on uninstall
SBs_no_reset = ("constants")

...

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
```
Generates  
![image](https://user-images.githubusercontent.com/8903016/119574171-31f40680-bdad-11eb-9230-6c13f9e1d448.png)
![image](https://user-images.githubusercontent.com/8903016/119574186-391b1480-bdad-11eb-9132-248f0fd5c364.png)


All scoreboard values are given in the `SB` class, which pairs the values together, and registers the value for initialisation (if a default value is given) and deletion (on uninstallation).

Because I am hilarious, the `Book` class is used as the outer class for a set of `Page`s. A menu page is also generated along with the listed ones, which will list all available pages. Books can be nested in theory, however this has not been properly tested, and will give you two layers of navigation bars.

`xxx_commands` are extra commands to run on enable, disable, increase or decrease as required. My ETL Utils Datapack shows this all in use.

*For more information on settings available, read the Blank example readme; for more on the template read the Template example; and for more on files generated read the Full example.

## Version History
### v1
Initial version, basic support and examples

### v1.1
Added pages, along with refactoring into multiple folders and adding the `SB` class to represent scoreboards for consistent representation. Settings now changed in `config.py` and still ran with `generator.py`.  
Also added option to generate basic blank datapack with required advancements and uninstall function based of initial settings in `config.py`.

### V1.2
Added support for a multiple-choice selector. Example in config:
```
Select("Selector", SB("select", "enabled", 1), [
    Choice("One", "one", 1),
    Choice("Two", "two", 2),
    Choice("Three", "three", 3),
    Choice("Four", "four", 4),
])
```

## Future Plans
Future
- [ ] Better support for nested layers of pages
- [ ] Better interplay when used with existing datapacks (only `config` directory overwritten ever. Template creation does not overwrite.).

**v1.2**
- [x] Multiple choice/selector setting

**v1.1**
- [x] Pages
- [x] Refactoring including splitting and scoreboard class
- [x] Template creation mode
