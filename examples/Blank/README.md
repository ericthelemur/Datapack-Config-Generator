# Blank Example for v1.1
This only includes the base generator program, with the config appropriately set up for example.

## Setting Types Available
- **Config:** This is the root class of your config, and should only be used once, as the top level class. It also generates the base files for the config to function.
- **Foldable:** Folding section, allowing for hiding sub-options when an option is disabled.

**Pages**
- **Book:** Base class for a set of pages. Generates and displays the pages, as well as a menu page for the book.
- **Page:** A single page, displays it's contents when selected.
- **MenuPage:** the main menu page, linking to all other pages. Also generates the `setpage_<page>` functions.

**Interactable**
- **Toggle:** A simple toggle switch, can run extra commands on enabling or disabling
- **Adjustable:** A single value that can be increased and decreased at a set increment. Can optionally give a minimum and maximum value, as well as extra commands to run on in/decreasing.
  - The increment scoreboard can be edited to create varying increments, though it will only update the display when `config` is called.
- **AdjustToggle:** Combines a toggle and adjustable: an adjustable that is only accessed when the toggle is off. Just like the previous, can have min/max and extra commands on en/disable and in/decrease.
- **Selector (v1.2):** Multiple choice, setting value of scoreboard when selected.

**Text**
- **Title:** The main heading, has bars above and below.
- **SubTitle:** Bold text in config list
- **Text:** Plain text entry. Can be given the arguments to a tellraw command for more functionality.
- **Uninstall:** The uninstall option. Asks the user to confirm uninstallation to protect against accidental removal.
  - Should always be on the top level