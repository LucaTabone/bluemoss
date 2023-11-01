from __future__ import annotations
from bs4 import BeautifulSoup
from src.bluemoss import utils
from datetime import date, datetime
from dataclasses import dataclass, field
from lxml import html as lxml_html, etree


@dataclass
class PersonDataClass:
    name: str
    birthday: date
    address: str | None = field(default=None)
    friends: list[PersonDataClass] = field(default_factory=list)
    last_updated: datetime | None = field(default=None, init=False)


class PersonClass:
    def __init__(
        self,
        name: str,
        birthday: date,
        friends: list[PersonClass],
        address: str | None = None,
    ):
        self.name = name
        self.birthday = birthday
        self.address = address
        self.friends = friends
        self.last_updated = datetime.now()


CLASS_INIT_PARAMS: set[str] = {'name', 'birthday', 'address', 'friends'}


# general.py
def test_get_init_params():
    assert (
        utils.get_all_class_init_params(PersonDataClass) == CLASS_INIT_PARAMS
    )
    assert utils.get_all_class_init_params(PersonClass) == CLASS_INIT_PARAMS


def test_get_optional_init_params():
    assert utils.get_optional_class_init_params(PersonDataClass) == {
        'address',
        'friends',
        'last_updated',
    }
    assert utils.get_optional_class_init_params(PersonClass) == {'address'}


# text.py
def test_clean_text():
    text: str = """
        Hello world!
                        Here.

        This is a test.



            Hello world!


        Test.
            Hello world!


    """
    assert (
        utils.clean_text(text)
        == 'Hello world!\nHere.\nThis is a test.\nHello world!\nTest.\nHello world!'
    )
    assert utils.clean_text(None) is None


def test_get_infix():
    text: str = '    Hello world!  '
    assert utils.get_infix(text, 'He', 'orld!') == 'llo w'
    assert utils.get_infix('', 'He', 'orld!') is None
    assert (
        utils.get_infix(text, 'NonExistentPrefix', 'NonExistentSuffix') is None
    )


# html.py
def test_etree_to_bs4():
    html: str = '<html><body><p>Hello world!</p></body></html>'
    soup: BeautifulSoup = utils.lxml_etree_to_bs4(lxml_html.fromstring(html))
    assert isinstance(soup, BeautifulSoup)
    assert str(soup) == html


def test_remove_tags():
    html: str = """<html><body><p>Hello world!</p><h1>Headline</h1><p>This is code.</p></body></html>"""

    for (tags_to_remove, expected_html) in [
        ('p', '<html><body><h1>Headline</h1></body></html>'),
        ('body', '<html></html>'),
        ('html', ''),
    ]:
        soup = BeautifulSoup(html, 'html.parser')
        utils.remove_tags_from_soup(soup, tags_to_remove)
        assert str(soup) == expected_html


def test_etree_to_string():
    html: str = '<html><body><p>Hello world!</p></body></html>'
    elem: etree.Element = lxml_html.fromstring(html)
    assert utils.lxml_etree_to_string(elem) == html


# url.py

URLS: list[str | None] = [
    'https://example.com/path/to/resource',
    'https://sub1.example.net/resource',
    'https://sub1.sub2.example.org/path/to/resource2?query=val',
    'https://www.sub3.example.com?p=q',
    'https://example2.org/path/to/resource3?p=v&q=w&p=z&a=b',
    '    ',
    '',
    None,
]


def test_get_base_domain():
    base_domains: list[str] = [
        'example.com',
        'example.net',
        'example.org',
        'example.com',
        'example2.org',
        None,
        None,
        None,
    ]
    for i, url in enumerate(URLS):
        assert utils.get_base_domain(url) == base_domains[i]


def test_get_domain():
    domains: list[str] = [
        'example.com',
        'sub1.example.net',
        'sub1.sub2.example.org',
        'sub3.example.com',
        'example2.org',
        None,
        None,
        None,
    ]
    for i, url in enumerate(URLS):
        assert utils.get_domain(url) == domains[i]


def test_get_endpoint():
    endpoints: list[str] = [
        '/path/to/resource',
        '/resource',
        '/path/to/resource2',
        None,
        '/path/to/resource3',
        None,
        None,
        None,
    ]
    for i, url in enumerate(URLS):
        assert utils.get_endpoint(url) == endpoints[i]


def test_get_url_query():
    queries: list[str | None] = [
        None,
        None,
        'query=val',
        'p=q',
        'p=v&q=w&p=z&a=b',
        None,
        None,
        None,
    ]
    for i, url in enumerate(URLS):
        assert queries[i] == utils.get_url_query(url)


def test_get_endpoint_with_query():
    endpoints_with_query: list[str] = [
        '/path/to/resource',
        '/resource',
        '/path/to/resource2?query=val',
        '?p=q',
        '/path/to/resource3?p=v&q=w&p=z&a=b',
        None,
        None,
        None,
    ]
    for i, url in enumerate(URLS):
        assert endpoints_with_query[i] == utils.get_endpoint_with_query(url)


def test_get_url_query_params():
    query_params: list[dict[str, str]] = [
        {},
        {},
        {'query': ['val']},
        {'p': ['q']},
        {'p': ['v', 'z'], 'q': ['w'], 'a': ['b']},
        {},
        {},
        {},
    ]
    for i, url in enumerate(URLS):
        assert query_params[i] == utils.get_url_query_params(url)
