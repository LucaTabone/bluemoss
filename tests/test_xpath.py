from __future__ import annotations
import pytest
from .constants import HIGH_NESTING_LEVEL_HTML as HTML
from src.bluemoss import Node, Range, Ex, InvalidXpathException, scrape


def test_valid_xpath():
    Node()
    Node('')
    Node('a')
    Node('/a')
    Node('./a')
    Node('//a')
    Node('.//a')
    Node('///a')


def test_invalid_xpath_1():
    with pytest.raises(InvalidXpathException):
        Node('body///section')


def test_invalid_xpath_2():
    with pytest.raises(InvalidXpathException):
        Node('//')


def test_non_existent_xpath():
    xpath: str = 'h4'
    assert scrape(Node(xpath), HTML) is None
    assert scrape(Node(xpath, filter=3), HTML) is None
    assert scrape(Node(xpath, filter=None), HTML) == []


def test_nested_xpath():
    xpath: str = 'body//section//li/a/../h3'
    assert scrape(Node(xpath, filter=None), HTML) == [
        'Service 1',
        'Service 2',
    ]
    assert scrape(Node(xpath), HTML) == 'Service 1'
    assert scrape(Node(xpath, filter=0), HTML) == 'Service 1'
    assert scrape(Node(xpath, filter=1), HTML) == 'Service 2'
    assert scrape(Node(xpath, filter=Range(0)), HTML) == [
        'Service 1',
        'Service 2',
    ]
    assert scrape(Node(xpath, filter=Range(1)), HTML) == ['Service 2']
    assert scrape(Node(xpath, filter=Range(4)), HTML) == []


def test_nested_xpath_with_tag_attribute_search():
    xpath: str = "body//section//li/a[@href='/info']/../h3"
    assert scrape(Node(xpath, filter=None), HTML) == ['Service 2']
    assert scrape(Node(xpath), HTML) == 'Service 2'


def test_nested_xpath_with_text_search():
    xpath: str = "html//section/ul//h3[text()='Service 1']/../a"
    assert scrape(Node(xpath), HTML) == 'Learn More'
    assert scrape(Node(xpath, extract=Ex.HREF_ENDPOINT), HTML) == '/learn-more'


def test_descendant_axis_flag():
    assert Node().add_descendant_axis_to_xpath is True

    node = Node('h2', add_descendant_axis_to_xpath=False)
    assert scrape(node, HTML) is None

    node.add_descendant_axis_to_xpath = True
    assert scrape(node, HTML) == 'About Us'

    nested_node = Node('main', nodes=[node], add_descendant_axis_to_xpath=False)
    assert scrape(nested_node, HTML) is None

    nested_node.add_descendant_axis_to_xpath = True
    assert scrape(nested_node, HTML) == ['About Us']

    node.add_descendant_axis_to_xpath = False
    assert scrape(nested_node, HTML) == [None]

    node.key = 'key'
    node.add_descendant_axis_to_xpath = True
    assert scrape(nested_node, HTML) == {'key': 'About Us'}

    node.add_descendant_axis_to_xpath = False
    assert scrape(nested_node, HTML) == {'key': None}


def test_xpath_with_preceding_axis():
    assert scrape(Node('//h2'), HTML) == 'About Us'
    assert scrape(Node('./body', extract=Ex.TEXT), HTML) == ''
    assert scrape(Node('/body', extract=Ex.TEXT), HTML) is None


def test_xpath_with_axis_prefix():
    assert Node('div').add_descendant_axis_to_xpath is True
    assert Node('/div').add_descendant_axis_to_xpath is False
    assert Node('./div').add_descendant_axis_to_xpath is False
    assert Node('.//div').add_descendant_axis_to_xpath is False


def test_function_call_xpath():
    assert scrape(Node('count(//a)'), HTML) == 11.0


def test_non_tag_yielding_xpath_with_nodes_1():
    node = Node('count(//a)', nodes=[Node('div'), Node('section')])
    assert scrape(node, HTML) == [None, None]


def test_non_tag_yielding_xpath_with_nodes_2():
    node = Node(
        'div/@class', nodes=[Node('div', key='key_1'), Node('section', key='key_2')]
    )
    assert scrape(node, HTML) == {'key_1': None, 'key_2': None}
