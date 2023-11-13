from __future__ import annotations
from lxml import etree
from bs4 import BeautifulSoup
from lxml.html import HtmlElement


def lxml_etree_to_bs4(tag: HtmlElement) -> BeautifulSoup:
    """
    Transforms a lxml.html.HtmlElement object to a BeautifulSoup object.
    :rtype: BeautifulSoup | None
    :return: BeautifulSoup representation of the given @param tag if isinstance(tag, HTMLElement), None otherwise.
    """
    return BeautifulSoup(lxml_etree_to_string(tag), 'html.parser')


def lxml_etree_to_string(tag: HtmlElement) -> str:
    """
    Transforms a lxml.html.HtmlElement object to a string.
    :rtype: str | None
    :return: String representation of the given @param tag if isinstance(tag, HTMLElement), None otherwise.
    """
    return etree.tostring(tag).decode('utf-8').strip()


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


__all__ = ['lxml_etree_to_bs4', 'lxml_etree_to_string', 'remove_tags_from_soup']
