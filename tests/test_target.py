from __future__ import annotations
import pytest
from dataclasses import dataclass
from src.bluemoss.classes.dict import Jsonify
from .constants import WITH_LINKS_HTML as HTML
from src.bluemoss.utils import url as url_utils
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


def test_invalid_target_type():
    with pytest.raises(InvalidTargetTypeException):
        Root(target=list)
    with pytest.raises(InvalidTargetTypeException):
        Root(target=dict)
    with pytest.raises(InvalidTargetTypeException):
        Root(target=set)


def test_invalid_keys_for_target():
    with pytest.raises(InvalidKeysForTargetException):
        Root(target=Link, nodes=[Node(key='domain')])


def test_missing_keys_for_target():
    expected_message_ending: str = (
        "Missing keys in nodes list for target 'Link': ['url']"
    )
    with pytest.raises(MissingTargetKeysException) as exc_info:
        Root(target=Link)
        assert str(exc_info.value).endswith(expected_message_ending)
