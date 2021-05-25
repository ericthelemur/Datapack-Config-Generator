from pathlib import Path
from sys import argv
from os import chdir

from config import *
from utils import make_func_dirs
from create_blank import create_blank


# First cmd line argument is location for dp, if -c first, will create a datapack template instead
if len(argv) >= 2:
    p = argv[1]
    if argv[1] == "-c": p = argv[2]
    Path(p).mkdir(parents=True, exist_ok=True)
    chdir(p)
    if argv[1] == "-c":
        create_blank()
        raise SystemExit
    
Path("data/%s/functions/config" % namespace).mkdir(parents=True, exist_ok=True)
chdir("data/%s/functions/config" % namespace)

make_func_dirs()

config.create_files()
