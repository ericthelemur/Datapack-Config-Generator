from pathlib import Path
from os.path import exists


# Stores scoreboards and players needed for the config
scoreboards = []
players = {}

class SB:
    """Represents scoreboard and player pair. If given default value, this is assigned in installation"""
    def __init__(self, player, scoreboard, default_val = None):
        self.scoreboard = scoreboard
        self.player = player
        self.default_val = default_val

        # Add to scoreboard and players
        if self.scoreboard not in scoreboards: scoreboards.append(self.scoreboard)
        t = (player, scoreboard)
        if t not in players and default_val is not None: players[t] = default_val

    def __repr__(self) -> str:
        return self.player + " " + self.scoreboard


# Makes empty dir recursively, ignores if existing
def make_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


# Creates file with content, if overwrites is false, will not overwrite if existing
def make_file(file: str, content: str = "", overwrite=False):
    if not overwrite and exists(file):
        with open(file, encoding="utf-8") as f:
            current_contents = f.read()
        if content != current_contents: 
            print(f"File {file} already exists, should read:\n{content}")

    with open(file, "w", encoding="utf-8") as f:
        f.write(content)

# Makes directories for config functions
def make_func_dirs():
    Path("dec").mkdir(parents=True, exist_ok=True)
    Path("inc").mkdir(parents=True, exist_ok=True)
    Path("disable").mkdir(parents=True, exist_ok=True)
    Path("enable").mkdir(parents=True, exist_ok=True)

