from enum import unique, Enum


@unique
class Extract(Enum):
    # found
    FOUND = "found"

    # text
    TEXT = "text"
    TEXT_CONTENT = "text_content"
    TEXT_CONTENT_CLEAN = "text_content_clean"

    # tag
    TAG = "tag"
    ETREE = "etree"
    TAG_AS_STRING = "tag_as_string"

    # href
    HREF = "href"
    HREF_QUERY = "href_query"
    HREF_DOMAIN = "href_domain"
    HREF_ENDPOINT = "href_endpoint"
    HREF_BASE_DOMAIN = "href_base_domain"
    HREF_QUERY_PARAMS = "href_query_params"
    HREF_ENDPOINT_WITH_QUERY = "href_endpoint_with_query"
