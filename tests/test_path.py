from __future__ import annotations
import pytest
from .constants import HIGH_NESTING_LEVEL_HTML as HTML
from src.bluemoss import Root, Range, Ex, InvalidXpathException, extract


def test_valid_paths():
    Root()
    Root('')
    Root('a')
    Root('//a')


def test_invalid_path_1():
    with pytest.raises(InvalidXpathException):
        Root('body///section')


def test_invalid_path_2():
    with pytest.raises(InvalidXpathException):
        Root('//')


def test_invalid_path_3():
    with pytest.raises(InvalidXpathException):
        Root('///a')


def test_non_existent_path():
    xpath: str = 'h4'
    assert extract(Root(xpath), HTML) is None
    assert extract(Root(xpath, filter=3), HTML) is None
    assert extract(Root(xpath, filter=None), HTML) == []


def test_nested_path():
    xpath: str = 'body//section//li/a/../h3'
    assert extract(Root(xpath, filter=None), HTML) == [
        'Service 1',
        'Service 2',
    ]
    assert extract(Root(xpath), HTML) == 'Service 1'
    assert extract(Root(xpath, filter=0), HTML) == 'Service 1'
    assert extract(Root(xpath, filter=1), HTML) == 'Service 2'
    assert extract(Root(xpath, filter=Range(0)), HTML) == [
        'Service 1',
        'Service 2',
    ]
    assert extract(Root(xpath, filter=Range(1)), HTML) == ['Service 2']
    assert extract(Root(xpath, filter=Range(4)), HTML) == []


def test_nested_path_with_tag_attribute_search():
    xpath: str = "body//section//li/a[@href='/info']/../h3"
    assert extract(Root(xpath, filter=None), HTML) == ['Service 2']
    assert extract(Root(xpath), HTML) == 'Service 2'


def test_nested_path_with_text_search():
    xpath: str = "html//section/ul//h3[text()='Service 1']/../a"
    assert extract(Root(xpath), HTML) == 'Learn More'
    assert (
        extract(Root(xpath, extract=Ex.HREF_ENDPOINT), HTML) == '/learn-more'
    )
