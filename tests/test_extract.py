from lxml import etree
from bs4 import BeautifulSoup
from .constants import WITH_LINKS_HTML
from src.bluemoss.utils import url as url_utils
from src.bluemoss import Root, Range, Ex, extract


HTML: str = WITH_LINKS_HTML


def test_found_extraction():
    # tag can be found
    moss = Root("div[@class='id_1']", extract=Ex.FOUND)
    assert extract(moss, HTML) is True

    # tag cannot be found
    moss = Root("div[@class='id_3']", extract=Ex.FOUND)
    assert extract(moss, HTML) is False


def test_text_extraction():
    moss = Root("p", extract=Ex.TEXT)
    assert extract(moss, HTML) == "Lorem 1"

    moss = Root("div", extract=Ex.TEXT)
    assert extract(moss, HTML) == "Ipsum 2"


def test_full_text_extraction():
    moss = Root("div", extract=Ex.FULL_TEXT)
    assert extract(moss, HTML) == "Ipsum 2 Lorem 2 Link 2"


def test_tag_extraction():
    moss = Root("div", extract=Ex.TAG)
    tag: BeautifulSoup = extract(moss, HTML)
    assert isinstance(tag, BeautifulSoup)

    moss = Root("div")
    assert extract(moss, tag.prettify()) == "Ipsum 2 Lorem 2 Link 2"


def test_etree_extraction():
    # 1) extract the found tag as an etree._Element instance
    moss = Root("div", extract=Ex.ETREE)
    elem: etree._Element = extract(moss, HTML)
    assert isinstance(elem, etree._Element)

    # 2) transform the etree._Element into a html string and test the full-text-extraction on it
    html: str = etree.tostring(elem, method="html")
    moss = Root("div")
    assert extract(moss, html) == "Ipsum 2 Lorem 2 Link 2"


def test_tag_as_string_extraction():
    pass


def test_href_extraction():
    pass


def test_href_query_extraction():
    pass


def test_href_domain_extraction():
    pass


def test_href_endpoint_extraction():
    pass


def test_href_base_domain_extraction():
    pass


def test_href_query_params_extraction():
    pass


def test_href_endpoint_with_query_extraction():
    pass
