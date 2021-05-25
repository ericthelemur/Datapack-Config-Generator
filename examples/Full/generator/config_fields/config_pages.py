from config_fields.config_base import ConfigField
from config_fields.config_text import SubTitle

from config import *
from utils import *
from os import getcwd, chdir

class Book(ConfigField):
    """Set of pages with menu"""
    def __init__(self, pages, page_sb: SB, directory="pages", main_function="main", menu_title="Menu", menu_page="menu"):
        self.pages = pages
        self.directory = directory
        self.page_sb = page_sb
        
        self.args = {"directory": directory + ("" if directory[-1] == "/" else "/"), "page_sb": page_sb, "menu_page": menu_page, "menu_title": menu_title, "main_function": main_function, "namespace": namespace}
        self.menu = MenuPage(pages, menu_title, menu_page)
        self.menu.args |= self.args

        # Link pages to previous and next pages
        prev_page = None
        for page in self.pages:
            page.args |= self.args  # Add general args to each page
            page.directory = directory
            page.args["prev_page"] = None if prev_page is None else prev_page.page_name
            if prev_page is not None: prev_page.args["next_page"] = page.page_name
            prev_page = page

        # Set directory of child fields
        self.set_dir(self.args["directory"])

    def render(self, indent=0):
        return "\n# Book %(directory)s\nfunction %(namespace)s:config/%(directory)s%(main_function)s" % self.args

    def create_files(self, indent=0):
        # Create and move to directory
        make_dir(self.args["directory"])
        old_dir = getcwd()
        chdir(self.args["directory"])

        make_func_dirs()

        # Create book main function
        with open("%(main_function)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)

            print("execute if score %(page_sb)s matches 0 run function %(namespace)s:config/%(directory)spage_%(menu_page)s" % self.args, file=f)
            for i, p in enumerate(self.pages):
                print(("execute if score %(page_sb)s matches " + str(i+1) + " run function %(namespace)s:config/%(directory)spage_%(page_name)s") % p.args, file=f)

        # Create files for pages
        self.menu.create_files()
        for page in self.pages: 
            page.create_files()

        # Reset directory
        chdir(old_dir)
        
        print("Finished generating for book", self.directory)

    
    def set_dir(self, dir: str):
        for c in self.pages:
            c.set_dir(dir)


class Page(ConfigField):
    """Single page of fields"""
    def __init__(self, title, page_name, contents):
        self.page_name = page_name
        self.args = {"title": title, "page_name": page_name, "namespace": namespace, "prev_page": None, "next_page": None}
        self.contents = contents
        self.directory = ""

    def create_files(self, indent=0):
        # Make page function
        with open("page_%(page_name)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)

            back = """{"text":" < ", "bold":true, "clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)ssetpage_%(prev_page)s"},"hoverEvent":{"action":"show_text","contents":"Go to previous page"}}""" % self.args
            if self.args["prev_page"] is None: back = """{"text":" < ", "bold":true, "color": "gray"}"""
            next = """{"text":" > ", "bold":true, "clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)ssetpage_%(next_page)s"},"hoverEvent":{"action":"show_text","contents":"Go to next page"}}""" % self.args
            if self.args["next_page"] is None: next = """{"text":" > ", "bold":true, "color": "gray"}"""
            print("""tellraw @s ["\\n", {"text":"Menu ", "bold":true, "clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)ssetpage_%(menu_page)s"},"hoverEvent":{"action":"show_text","contents":"Go to %(menu_title)s"}}, %(back)s, {"text":"%(title)s", "hoverEvent":{"action":"show_text","contents":"Currently on page %(title)s"}}, %(next)s, "\\n"]""" % (self.args | {"back": back, "next": next}), file=f)
            
            # Put content in page
            for c in self.contents:
                print(c.render(indent=0), file=f)

        # Create content's files
        for c in self.contents:
            c.create_files()
        
        print("Finished generating for page", self.page_name)

    def set_dir(self, dir: str):
        super().set_dir(dir)

        for c in self.contents:
            c.set_dir(dir)


class MenuPage(Page):
    """Main menu page, linking to all others"""
    def __init__(self, pages, title="Menu", page_name="menu"):
        self.pages = pages
        self.title = title
        self.page_name = page_name
        self.args = {}

    def create_files(self, indent=0):
        with open("page_%(menu_page)s.mcfunction" % self.args, "w", encoding="utf-8") as f:
            print("# Generated with ericthelemur's Datapack Settings Generator\n", file=f)
            print(SubTitle(self.title).render(), file=f)

            # Add link to each page, and create setpage functions
            for i, p in enumerate(self.pages):
                print("""tellraw @s ["  ", {"text": "%(title)s", "clickEvent":{"action":"run_command","value":"/function %(namespace)s:config/%(directory)ssetpage_%(page_name)s"},"hoverEvent":{"action":"show_text","contents":"Go to %(title)s"}}]""" % p.args, file=f)
                make_file("setpage_%(page_name)s.mcfunction" % p.args, ("# Generated with ericthelemur's Datapack Settings Generator\n\nscoreboard players set %(page_sb)s " + str(i+1) + "\nfunction %(namespace)s:config") % self.args, overwrite=True)
            
            # Create setmenu
            make_file("setpage_%(menu_page)s.mcfunction" % self.args, ("# Generated with ericthelemur's Datapack Settings Generator\n\nscoreboard players set %(page_sb)s 0\nfunction %(namespace)s:config") % self.args, overwrite=True)

