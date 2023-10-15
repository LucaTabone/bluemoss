from os import walk, getcwd
from bs4 import BeautifulSoup
from bluemoss.utils import remove_tags


def setup():
    _prettify_html_files()


def _prettify_html_files():
    for res in walk(getcwd()):
        if "/tests/" in res[0]:
            continue
        for file_name in res[2]:
            if not file_name.endswith(".html"):
                continue
            file_path: str = f"{res[0]}/{file_name}"
            with open(file_path, "r+", encoding="utf-8") as file:
                soup: BeautifulSoup = BeautifulSoup(file.read(), "html.parser")
                remove_tags(soup=soup, tag_names=["script", "noscript", "style"])
                file.seek(0)
                file.write(soup.prettify())
                file.truncate()


if __name__ == '__main__':
    setup()
