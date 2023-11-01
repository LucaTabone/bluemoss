from lxml import etree
from bs4 import BeautifulSoup
from src.bluemoss import Root, Ex, extract
from .constants import WITH_LINKS_HTML as HTML


def test_text_extraction():
    moss = Root('p', extract=Ex.TEXT)
    assert extract(moss, HTML) == 'Lorem 1'

    moss = Root('div', extract=Ex.TEXT)
    assert extract(moss, HTML) == 'Ipsum 2'


def test_full_text_extraction():
    moss = Root('div', extract=Ex.FULL_TEXT)
    assert extract(moss, HTML) == 'Ipsum 2\nLorem 2\nLink 2'


def test_tag_extraction():
    moss = Root('div', extract=Ex.BS4_TAG)
    tag: BeautifulSoup = extract(moss, HTML)
    assert isinstance(tag, BeautifulSoup)

    moss = Root('div')
    assert extract(moss, tag.prettify()) == 'Ipsum 2\nLorem 2\nLink 2'


def test_etree_extraction():
    # 1) extract the found tag as an etree._Element instance
    moss = Root('div', extract=Ex.LXML_HTML_ELEMENT)
    elem: etree._Element = extract(moss, HTML)
    assert isinstance(elem, etree._Element)

    # 2) transform the etree._Element into a html string and test the full-text-extraction on it
    html: str = etree.tostring(elem, method='html')
    moss = Root('div')
    assert extract(moss, html) == 'Ipsum 2\nLorem 2\nLink 2'


def test_tag_as_string_extraction():
    moss = Root('div', extract=Ex.TAG_AS_STRING)
    html: str = extract(moss, HTML)
    assert isinstance(html, str)
    moss = Root('div')
    assert extract(moss, html) == 'Ipsum 2\nLorem 2\nLink 2'


def test_href_extraction():
    moss = Root('a', filter=2, extract=Ex.HREF)
    assert extract(moss, HTML) == 'https://www.nvidia.com/link3?p=3&q=3'


def test_href_extraction_with_xpath():
    for moss in [
        Root('a/@href', filter=2),
        Root('a/@href', filter=2, extract=Ex.HREF_BASE_DOMAIN),
        Root('a/@href', filter=2, extract='some_random_tag_attribute'),
    ]:
        assert extract(moss, HTML) == 'https://www.nvidia.com/link3?p=3&q=3'


def test_href_query_extraction():
    moss = Root('a', extract=Ex.HREF_QUERY)
    assert extract(moss, HTML) == 'p=1&q=1'


def test_href_domain_extraction():
    moss = Root('a', filter=3, extract=Ex.HREF_DOMAIN)
    assert extract(moss, HTML) == 'chat.openai.com'


def test_href_base_domain_extraction():
    moss = Root('a', filter=3, extract=Ex.HREF_BASE_DOMAIN)
    assert extract(moss, HTML) == 'openai.com'


def test_href_endpoint_extraction():
    moss = Root('a', filter=3, extract=Ex.HREF_ENDPOINT)
    assert extract(moss, HTML) == '/page4/link4'


def test_href_endpoint_with_query_extraction():
    moss = Root('a', filter=3, extract=Ex.HREF_ENDPOINT_WITH_QUERY)
    assert extract(moss, HTML) == '/page4/link4?p=4&q=4&p=5'


def test_href_query_params_extraction():
    moss = Root('a', filter=3, extract=Ex.HREF_QUERY_PARAMS)
    assert extract(moss, HTML) == {'p': ['4', '5'], 'q': ['4']}
