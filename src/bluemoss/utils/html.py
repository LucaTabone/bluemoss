from lxml import etree
from bs4 import BeautifulSoup


def is_valid_xpath(xpath_query: str):
    root = etree.Element("root")
    doc = etree.ElementTree(root)
    try:
        doc.xpath(xpath_query)
        return True
    except etree.XPathEvalError:
        return False


def lxml_etree_to_bs4(node: etree.Element) -> BeautifulSoup:
    return BeautifulSoup(lxml_etree_to_string(node), "html.parser")


def lxml_etree_to_string(node: etree.Element) -> str:
    return etree.tostring(node, method="html").decode("utf-8")


def remove_tags_from_soup(soup: BeautifulSoup, tag_names: list[str]) -> str:
    """
    Removes specific HTML tags from a BeautifulSoup object.

    :param soup: BeautifulSoup object representing a block of HTML
    :param tag_names: Tag names to be removed HTML
    """
    for data in soup(tag_names):
        data.decompose()
    return soup.prettify()


__all__ = [
    "is_valid_xpath",
    "lxml_etree_to_bs4",
    "lxml_etree_to_string",
    "remove_tags_from_soup"
]
