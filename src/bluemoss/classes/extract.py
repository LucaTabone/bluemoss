from enum import unique, Enum


@unique
class Ex(Enum):
    """
    The 'Ex' enum provides a variety of values that make it easy to extract specific data from a html-tag.
    An 'Ex' enum value can be used to set 'extract' parameter of a 'Node' instance.

    Note that setting the 'extract' parameter of a 'Node' instance only has an effect when the Node instance
    is a leaf node, i.e. its 'nodes' parameter is an empty list.

    :param TEXT: Yields the text contained in a html-tag excluding the text contained in child html-tags.
    :param FULL_TEXT: Yields the text contained in a html-tag including the text contained in child html-tags.
    :param BS4_TAG: Yields the current html tag as a BeautifulSoup object.
    :param TAG_AS_STRING: Yields the current html tag as a string.
    :param LXML_HTML_ELEMENT: Yields the current tag as a lxml.html.HtmlElement object.
    :param HREF: Yields the href attribute of a tag.
    :param HREF_QUERY:
        Yields the query-string part of a href attribute of a tag.
        E.g. the tag <a href="https://example.com?foo=bar">https://example.com</a> will yield "foo=bar".
    :param HREF_DOMAIN:
        Yields the entire domain including subdomains of a href attribute of a tag.
        E.g. the tag <a href="https://sub1.sub2.example.com?foo=bar">https://sub1.sub2.example.com</a>
        will yield "sub1.sub2.example.com".
    :param HREF_ENDPOINT:
        Yields the endpoint without the query-string of a href attribute of a tag.
        E.g. the tag <a href="https://example.com/products/page1?foo=bar">https://example.com</a>
        will yield "/products/page1".
    :param HREF_ENDPOINT_WITH_QUERY:
        Yields the endpoint with the query-string of a href attribute of a tag.
        E.g. the tag <a href="https://example.com/products/page1?foo=bar">https://example.com</a>
        will yield "/products/page1?foo=bar".
    :param HREF_BASE_DOMAIN:
        Yields the base-domain of a href attribute of a tag.
        E.g. the tag <a href="https://sub1.sub2.example.com?foo=bar">https://sub1.sub2.example.com</a>
        will yield "example.com". If no base-domain can be found in the href attribute it will yield the None value.
    :param HREF_QUERY_PARAMS:
        Yields the query-params as a dict of the href attribute of a tag.
        E.g. the tag <a href="https://example.com/products/page1?foo1=bar1&foo2=bar2&foo1=bar3">https://example.com</a>
        will yield the dictionary {"foo1": ["bar1", "bar3"], "foo2": ["bar2"]}.
    """

    # text
    TEXT = 'text'
    FULL_TEXT = 'full_text'

    # tag
    BS4_TAG = 'tag'
    TAG_AS_STRING = 'tag_as_string'
    LXML_HTML_ELEMENT = 'lxml_html_etree_element'

    # href
    HREF = 'href'
    HREF_QUERY = 'href_query'
    HREF_DOMAIN = 'href_domain'
    HREF_ENDPOINT = 'href_endpoint'
    HREF_BASE_DOMAIN = 'href_base_domain'
    HREF_QUERY_PARAMS = 'href_query_params'
    HREF_ENDPOINT_WITH_QUERY = 'href_endpoint_with_query'


__all__ = ['Ex']
