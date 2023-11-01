from __future__ import annotations
from lxml import etree
from bs4 import BeautifulSoup
from lxml.html import HtmlElement


def is_valid_xpath(xpath_query: str) -> bool:
    """
    Checks if the given @param xpath_query is a valid XPath expression.
    :rtype: bool
    :return: True if @param xpath_query is a valid XPath expression, False otherwise.
    """
    root = etree.Element('root')
    doc = etree.ElementTree(root)
    try:
        doc.xpath(xpath_query)
        return True
    except etree.XPathEvalError:
        return False


def lxml_etree_to_bs4(tag: HtmlElement | str) -> BeautifulSoup | None:
    """
    Transforms a lxml.html.HtmlElement object to a BeautifulSoup object.
    :rtype: BeautifulSoup | None
    :return: BeautifulSoup representation of the given @param tag if isinstance(tag, HTMLElement), None otherwise.
    """
    if not isinstance(tag, HtmlElement):
        return None
    tag_as_str: str | None = lxml_etree_to_string(tag)
    if tag_as_str is None:
        return None
    return BeautifulSoup(tag_as_str, 'html.parser')


def lxml_etree_to_string(tag: HtmlElement | str) -> str | None:
    """
    Transforms a lxml.html.HtmlElement object to a string.
    :rtype: str | None
    :return: String representation of the given @param tag if isinstance(tag, HTMLElement), None otherwise.
    """
    if not isinstance(tag, HtmlElement):
        return None
    return etree.tostring(tag, method='html').decode('utf-8')


def remove_tags_from_soup(soup: BeautifulSoup, tag_names: list[str]) -> None:
    """
    Removes html-tags with certain ids (@param tag_names) from the given BeautifulSoup object @param soup.
    Exampl: if tag_names is ["h1", "h2"], then all "h1" and "h2" tags will be removed from @param soup.

    :param soup: BeautifulSoup object representing a block of HTML
    :param tag_names: Tag names to be removed HTML
    :return: None
    """
    for data in soup(tag_names):
        data.decompose()


__all__ = [
    'is_valid_xpath',
    'lxml_etree_to_bs4',
    'lxml_etree_to_string',
    'remove_tags_from_soup',
]
