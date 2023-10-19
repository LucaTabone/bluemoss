from __future__ import annotations
from dataclasses import dataclass
from .constants import WITH_LINKS_HTML
from src.bluemoss.classes.dict import Dictable
from src.bluemoss.utils import url as url_utils
from src.bluemoss import BlueMoss, Root, Node, Ex, extract


HTML: str = WITH_LINKS_HTML


@dataclass
class Links(Dictable):
    links: list[Link]


@dataclass
class Link(Dictable):
    url: str

    @property
    def domain(self):
        return url_utils.get_domain(self.url)

    @property
    def base_domain(self):
        return url_utils.get_base_domain(self.url)

    @property
    def endpoint(self):
        return url_utils.get_endpoint(self.url)

    @property
    def dict(self):
        return super().dict | {
            "domain": self.domain,
            "base_domain": self.base_domain,
            "endpoint": self.endpoint
        }


MOSS_WITH_TARGET: BlueMoss = Root(
    target=Links,
    nodes=[
        Node(
            path="a",
            key="links",
            target=Link,
            filter=None,
            nodes=[
                Node(
                    key="url",
                    extract=Ex.HREF
                )
            ]
        )
    ]
)


MOSS_WITHOUT_TARGET: BlueMoss = Root(
    path="a",
    key="links",
    filter=None,
    nodes=[
        Node(
            key="url",
            extract=Ex.HREF
        ),
        Node(
            key="domain",
            extract=Ex.HREF_DOMAIN
        ),
        Node(
            key="base_domain",
            extract=Ex.HREF_BASE_DOMAIN
        ),
        Node(
            key="endpoint",
            extract=Ex.HREF_ENDPOINT
        )
    ]
)


def test_extract_equality():
    assert extract(MOSS_WITH_TARGET, HTML).dict == extract(MOSS_WITHOUT_TARGET, HTML)
