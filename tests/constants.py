from os.path import join, dirname

STATIC_DIR: str = join(dirname(__file__), "static")


with open(join(STATIC_DIR, "four_divs.html"), "r") as file:
    FOUR_DIVS_HTML = file.read()


with open(join(STATIC_DIR, "with_links.html"), "r") as file:
    WITH_LINKS_HTML = file.read()


with open(join(STATIC_DIR, "high_nesting_level.html"), "r") as file:
    HIGH_NESTING_LEVEL_HTML = file.read()
