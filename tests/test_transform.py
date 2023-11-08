from __future__ import annotations
import pytest
from dataclasses import dataclass
from .constants import HIGH_NESTING_LEVEL_HTML as HTML
from src.bluemoss import Node, Range, Ex, scrape


def test_domain_extract_via_transform():
    node = Node(
        "footer//li[contains(text(), 'mail')]/a",
        extract=Ex.HREF,
        transform=lambda mail: mail.split('@')[-1] if mail else None,
    )
    assert scrape(node, HTML) == 'example.com'


def test_zip_code_extract_via_transform():
    node = Node(
        "address//div[contains(@class, 'contact-cell')]/p[2]",
        transform=lambda address: int(address.split(' ')[-1]),
    )
    assert scrape(node, HTML) == 12345


def test_attempt_transform_on_none():
    node = Node('h4', transform=lambda none_val: none_val.split())
    with pytest.raises(AttributeError):
        scrape(node, HTML)


def test_usage_and_non_usage_of_transform_param():
    @dataclass
    class Address:
        line_1: str
        line_2: str

    expected: Address = Address(line_1='123 Main Street', line_2='City, State 12345')
    for node in [
        Node(
            'address//p',
            filter=Range(1),
            transform=lambda lines: Address(lines[0], lines[1]),
        ),
        Node(
            'address',
            target=Address,
            nodes=[
                Node('p', filter=1, key='line_1'),
                Node('p', filter=2, key='line_2'),
            ],
        ),
    ]:
        assert scrape(node, HTML) == expected
