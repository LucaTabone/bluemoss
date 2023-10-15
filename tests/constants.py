from os.path import join, dirname

STATIC_DIR: str = join(dirname(__file__), "static")


with open(join(STATIC_DIR, "four_divs.html"), "r") as file:
    FOUR_DIVS_HTML = file.read()
