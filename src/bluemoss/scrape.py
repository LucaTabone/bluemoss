from __future__ import annotations
from . import utils
from lxml.html import HtmlElement
from typing import Type, Any, cast
from lxml import html as lxml_html
from .classes import Ex, Node, Range, JsonifyWithTag


def scrape(node: Node, html: str) -> Any:
    """Main function of bluemoss: Scrapes :param html with the scraping-recipe defined by :param node.

    :param node: Node object. Defines how to scrape :param html.
    :param html: HTML doc to be scraped.
    :rtype: Any
    :return: data extracted from :param html
    """
    # noinspection PyTypeChecker
    tag: HtmlElement = lxml_html.fromstring(html)
    return _scrape(node, tag, 0)


def _scrape(node: Node, tag: HtmlElement, level: int) -> Any:
    """Internal main function, which is recursively called in order to scrape :param tag using :param node.

    :param node: Defines how to scrape :param tag.
    :param tag: The html-tag to be scraped.
    :param level:
        The depth level of the current Bluemoss node :param moss (0 at root-level).
        The reason for why we keep track of the depth level of @param moss in relation to it's root node, is because
        we want to allow for the root node (level == 0) to define a value for its parameter 'key' in which case
        we want to return a dict with just one key-value-pair (key pointing to the extracted data).
    :rtype: Any
    :return: data extracted from :param html
    """

    if not isinstance(tag, HtmlElement):
        return None

    if node.no_xpath:
        # if no xpath was defined, we continue to work with the current tag
        tags = [tag]
    else:
        if node.add_descendant_axis_to_xpath:
            xpath = ('//' if level == 0 else './/') + node.xpath
        else:
            xpath = node.xpath
        # find matching tags
        tags = tag.xpath(xpath)
        if not isinstance(tags, list):
            tags = [tags]  # type: ignore[unreachable]
        # filter the matched tags against node.filter
        tags = _filter_tags(node, tags)

    if len(tags) == 0:
        # We either did not find any matching tags or we found matching tags but did not filter any of them.
        return node.transform(None if node.find_single_tag else [])

    if node.target or node.nodes:
        val = [_build_target(node, tag, level) for tag in tags]
    else:
        # len(node.nodes) == 0 and node.target is None
        val = [_scrape_leaf_node(node, tag) for tag in tags]

    if isinstance(node.filter, int):
        # node.filter is an int => we want to filter for a single tag
        assert len(val) == 1
        val = val[0]  # type: ignore

    if level == 0 and node.key is not None:
        # About this if-condition:
        #     1) level == 0: @param moss is most outer parent node (root node)
        #     2) moss.key is not None: extracted data (val) shall be wrapped in a dictionary

        # Why do we only want to get here if @param level is 0?
        #     - If level > 0, then moss.key will be used in the function '_build_target'.
        #     - So, a way to make use of moss.key when level == 0, is to build a dictionary
        #       where moss.key points to @param val.
        return {node.key: node.transform(val)}

    return node.transform(val)


def _filter_tags(node: Node, tags: list[Any]) -> list[Any]:
    """filters the tags matched against node.xpath using node.filter"""

    if isinstance(node.filter, int):
        # node.filter is an int => we want to filter for a single match
        try:
            return [tags[node.filter]]
        except IndexError:
            return []

    # node.filter is not an int => we want to filter for multiple matches

    if isinstance(node.filter, Range):
        # node.filter is a Range object => filter for multiple subsequent matches
        return node.filter.filter(tags)

    if isinstance(node.filter, list):
        # node.filter is a list of integers => filter for the matches whose index is contained in node.filter
        _tags: list[Any] = []
        for idx in node.filter:
            try:
                _tags.append(tags[idx])
            except IndexError:
                _tags.append(None)
        return _tags

    # node.filter is None
    return tags


def _build_target(
    node: Node, tag: Any, level: int
) -> list[Any] | dict[str, Any] | Type[Any] | None:
    """
    Builds the target instance (list, dict or class/dataclass instance) of :param node.
    Called by '_extract' function in case :param node defines its 'nodes' parameter.

    :rtype: list | dict | Class (class/dataclass instance)
    :return:
        1. Class instance if the 'target' param of :param node is not None.
        2. List or Dict if the 'target' param of :param node is None:
            2.1: Dict if all nodes in :param node define their 'key' param.
            2.2: List if all nodes have their 'key' param set to None.
    """

    if tag is None:
        return None

    if node.target is None:
        if node.keys_in_nodes:
            # the target is a dict
            return {
                _node.key: _scrape(_node, tag, level + 1)  # type: ignore
                for _node in node.nodes
            }
        # the target is a list
        return [_scrape(_node, tag, level + 1) for _node in node.nodes]

    # the target is a class/dataclass

    # :param values: dictionary to instantiate node.target
    values: dict[str, Any] = {
        _node.key: _scrape(_node, tag, level + 1) for _node in node.nodes  # type: ignore
    }

    if issubclass(node.target, JsonifyWithTag):
        # If node.target inherits from JsonifyWithTag, the intention is to provide
        # the current html-tag @param tag to our target-instance using the key '_tag'.
        values |= {'_tag': tag}

    # noinspection PyArgumentList
    return node.target(**values)  # type: ignore


def _scrape_leaf_node(node: Node, tag: Any) -> Any:
    """
    Extracts data from a leaf node.
    A leaf node is a Node object with an empty 'nodes' list (node.nodes == []).

    :rtype: Any
    :return: data extracted from :param node.
    """

    if tag is None:
        return None

    if not isinstance(tag, HtmlElement):
        # @param tag is a string if node.xpath endswith with e.g. /@href,  /@class or /text(),
        # i.e. when we do not select for a tag but for a tag-property, like text or an attribute.
        return tag

    if isinstance(node.extract, str):
        # extract the value of the tag-attribute defined by node.extract
        return tag.get(node.extract)

    # extract data from @param tag by match-casing node.extract
    if node.extract == Ex.FULL_TEXT:
        return utils.clean_text(tag.xpath('string(.)'))
    elif node.extract == Ex.LXML_HTML_ELEMENT:
        return tag
    elif node.extract == Ex.TEXT:
        return tag.text.strip()
    elif node.extract == Ex.BS4_TAG:
        return utils.lxml_etree_to_bs4(tag)
    elif node.extract == Ex.TAG_AS_STRING:
        return cast(Any, utils.lxml_etree_to_bs4(tag)).prettify()
    elif node.extract == Ex.HREF:
        return tag.get('href')
    elif node.extract == Ex.HREF_QUERY:
        return utils.get_url_query(tag.get('href'))
    elif node.extract == Ex.HREF_DOMAIN:
        return utils.get_domain(tag.get('href'))
    elif node.extract == Ex.HREF_ENDPOINT:
        return utils.get_endpoint(tag.get('href'))
    elif node.extract == Ex.HREF_BASE_DOMAIN:
        return utils.get_base_domain(tag.get('href'))
    elif node.extract == Ex.HREF_QUERY_PARAMS:
        return utils.get_url_query_params(tag.get('href'))
    elif node.extract == Ex.HREF_ENDPOINT_WITH_QUERY:
        return utils.get_endpoint_with_query(tag.get('href'))
    else:
        raise NotImplementedError


__all__ = ['scrape']
