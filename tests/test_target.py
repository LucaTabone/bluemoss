from __future__ import annotations
import pytest
from datetime import datetime
from dataclasses import dataclass
from .constants import WITH_LINKS_HTML as HTML
from src.bluemoss.utils import url as url_utils
from src.bluemoss.classes.jsonify import Jsonify
from src.bluemoss import (
    BlueMoss,
    Root,
    Node,
    Ex,
    extract,
    InvalidTargetTypeException,
    InvalidKeysForTargetException,
    MissingTargetKeysException,
)


@dataclass
class Links(Jsonify):
    links: list[Link]


@dataclass
class Link(Jsonify):
    url: str

    @property
    def domain(self) -> str:
        return url_utils.get_domain(self.url)

    @property
    def base_domain(self) -> str:
        return url_utils.get_base_domain(self.url)

    @property
    def endpoint(self) -> str:
        return url_utils.get_endpoint(self.url)

    @property
    def dict(self) -> dict:
        return {
            'url': self.url,
            'domain': self.domain,
            'endpoint': self.endpoint,
            'base_domain': self.base_domain,
        }


MOSS_WITH_TARGET: BlueMoss = Root(
    target=Links,
    nodes=[
        Node(
            xpath='a',
            key='links',
            target=Link,
            filter=None,
            nodes=[Node(key='url', extract=Ex.HREF)],
        )
    ],
)


MOSS_WITHOUT_TARGET: BlueMoss = Root(
    xpath='a',
    key='links',
    filter=None,
    nodes=[
        Node(key='url', extract=Ex.HREF),
        Node(key='domain', extract=Ex.HREF_DOMAIN),
        Node(key='base_domain', extract=Ex.HREF_BASE_DOMAIN),
        Node(key='endpoint', extract=Ex.HREF_ENDPOINT),
    ],
)


def test_extract_equality():
    assert extract(MOSS_WITH_TARGET, HTML).dict == extract(
        MOSS_WITHOUT_TARGET, HTML
    )


def test_target_is_list():
    moss = Root('html', nodes=[Node('a', filter=None)])
    assert extract(moss, HTML) == [['Link 1', 'Link 2', 'Link 3', 'Link 4']]


def test_target_is_dict():
    moss = Root('html', nodes=[Node('a', key='links', filter=None)])
    assert extract(moss, HTML) == {
        'links': ['Link 1', 'Link 2', 'Link 3', 'Link 4']
    }


def test_invalid_target_type():
    with pytest.raises(InvalidTargetTypeException):
        Root(target=list, nodes=[Node(key='some_key')])
    with pytest.raises(InvalidTargetTypeException):
        Root(target=dict, nodes=[Node(key='some_key')])
    with pytest.raises(InvalidTargetTypeException):
        Root(target=set, nodes=[Node(key='some_key')])


def test_invalid_keys_for_target():
    with pytest.raises(InvalidKeysForTargetException):
        Root(target=Link, nodes=[Node(key='domain')])


def test_missing_keys_for_target():
    @dataclass
    class _Link:
        url: str
        created_at: datetime

    expected_message_ending: str = (
        "Missing keys in nodes list for target '_Link': ['created_at']"
    )

    with pytest.raises(MissingTargetKeysException) as exc_info:
        Root(target=_Link, nodes=[Node(key='url')])

    assert str(exc_info.value).endswith(expected_message_ending)
