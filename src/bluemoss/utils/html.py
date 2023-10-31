from lxml import etree
from bs4 import BeautifulSoup
from lxml.html import HtmlElement


def is_valid_xpath(xpath_query: str):
    root = etree.Element("root")
    doc = etree.ElementTree(root)
    try:
        doc.xpath(xpath_query)
        return True
    except etree.XPathEvalError:
        return False


def lxml_etree_to_bs4(tag: HtmlElement | str) -> BeautifulSoup | None:
    if isinstance(tag, HtmlElement):
        return BeautifulSoup(lxml_etree_to_string(tag), "html.parser")


def lxml_etree_to_string(tag: HtmlElement | str) -> str | None:
    if isinstance(tag, HtmlElement):
        return etree.tostring(tag, method="html").decode("utf-8")


def remove_tags_from_soup(soup: BeautifulSoup, tag_names: list[str]):
    """
    Removes specific HTML tags from a BeautifulSoup object.

    :param soup: BeautifulSoup object representing a block of HTML
    :param tag_names: Tag names to be removed HTML
    """
    for data in soup(tag_names):
        data.decompose()


__all__ = [
    "is_valid_xpath",
    "lxml_etree_to_bs4",
    "lxml_etree_to_string",
    "remove_tags_from_soup"
]
