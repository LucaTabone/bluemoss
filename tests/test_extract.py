import pytest
from .constants import WITH_LINKS_HTML
from src.bluemoss.utils import url as url_utils
from src.bluemoss import Root, Range, Ex, extract


html: str = WITH_LINKS_HTML


def test_found_extraction():
    # tag can be found
    moss = Root("div[contains(@class, 'id_1')]", extract=Ex.FOUND)
    assert extract(moss, html) is True

    # tag cannot be found
    moss = Root("div[contains(@class, 'id_3')]", extract=Ex.FOUND)
    assert extract(moss, html) is False


def test_text_extraction():
    pass


def test_text_content_extraction():
    pass


def test_clean_text_content_extraction():
    pass


def test_tag_extraction():
    pass


def test_etree_extraction():
    pass


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
