# Template Example for v1.1
This includes the base generator program and generated base datapack after `python generator.py -c ..` is run in the `generator` directory..  

This is still applicable to all projects.  
Only need to update values in `pack.mcmeta` and `data/generated/advancements/generated.json`, assuming basic parameters in `config.py` are set correctly.

## Template Files Generated
- `pack.mcmeta` - registers datapack with minecraft. Edit to include description.
- `minecraft/tags/functions/load.json` and `tick.json` - registers `load` and `tick` functions with Minecraft

**Advancements**
- `global/root.json` - Root installed datapacks advancement page.
- `global/ericthelemur.json` - Advancement for datapacks creator, me in this case. Name and head is updated to match `config.py`.
- `template/advancements/template.json` - Advancement for this datapack specifically. Gets deleted if datapack is deleted, cannot be removed in uninstall.
  
**Functions**
- `template/functions/load` - main load function. Calls `config/load_config` with `execute if score template enabled = zero constants run function template:config/load_config`. If no config, just ignored.
- `template/functions/tick` - main function run every tick. Empty in template.
- `template/uninstall` - function to call on uninstall. Calls `template:config/uninstall_config`, if no config, just ignored.