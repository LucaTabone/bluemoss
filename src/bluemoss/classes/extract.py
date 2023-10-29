from enum import unique, Enum


@unique
class Ex(Enum):
    # text
    TEXT = "text"
    FULL_TEXT = "full_text"

    # tag
    BS4_TAG = "tag"
    ETREE_ELEMENT = "etree_element"
    TAG_AS_STRING = "tag_as_string"

    # href
    HREF = "href"
    HREF_QUERY = "href_query"
    HREF_DOMAIN = "href_domain"
    HREF_ENDPOINT = "href_endpoint"
    HREF_BASE_DOMAIN = "href_base_domain"
    HREF_QUERY_PARAMS = "href_query_params"
    HREF_ENDPOINT_WITH_QUERY = "href_endpoint_with_query"


__all__ = [
    "Ex"
]
