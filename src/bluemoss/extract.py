from . import utils
from lxml.html import HtmlElement
from lxml import html as lxml_html
from .classes import Ex, BlueMoss, Range, JsonifyWithTag, PrettyDict, Class


def extract(moss: BlueMoss, html: str) -> any:
    """ Main function of bluemoss: Scrapes :param html with the scraping-recipe defined by :param moss.
    
    :param moss: BlueMoss object. Defines how to scrape :param html.
    :param html: HTML doc to be scraped.
    :rtype: any
    :return: data extracted from :param html
    """

    tag: HtmlElement = lxml_html.fromstring(html)
    return _extract(0, moss, tag)


def _extract(
        level: int,
        moss: BlueMoss,
        tag: HtmlElement | str | None
) -> any:
    """ Internal main function, which is recursively called in order to scrape :param tag using :param moss.
        
    :param moss: Defines how to scrape :param tag.
    :param tag: The html-tag to be scraped.
    :param level:
        The depth level of the current Bluemoss node :param moss (0 at root-level).
        The reason for why we keep track of the depth level of @param moss in relation to it's root node, is because
        we want to allow for the root node (BlueMoss object, level = 0) to define a value for its parameter 'key'
        in which case we want to return a dict with just one key-value-pair (key pointing to the extracted data).
    :rtype: any
    :return: data extracted from :param html
    """

    if moss.no_xpath:
        """ if no xpath was defined, we continue to work with the current tag """
        tags: list[HtmlElement] = [tag]
    else:
        """ find matching tags """
        tags: list[HtmlElement | str] = tag.xpath(moss.full_xpath)
        """ filter the matched tags against moss.filter """
        tags: list[HtmlElement | str | None] = _filter_matched_tags(moss, tags)

    if len(tags) == 0:
        """ We either did not find any matching tags or we found matching tags but did not filter any of them. """
        return moss.transform(None if moss.find_single_tag else [])

    if moss.nodes:
        """ len(moss.nodes) > 0 """
        val: list[list | dict | Class | None] = [_build_target(level, moss, tag) for tag in tags]
    else:
        """ len(moss.nodes) == 0 """
        val: list[any] = [_extract_from_leaf_node(moss, tag) for tag in tags]

    if moss.find_single_tag:
        """
        len(val) == 1
        
        If moss.find_single_tag is True, then we explicitly intent to match only one html-tag.
        """
        val: any = val[0]

    if level == 0 and moss.key is not None:
        """
        About this if-condition:
            1) level == 0: @param moss is most outer parent node (root node)
            2) moss.key is not None: extracted data (val) shall be wrapped in a dictionary (since level == 0)
            
        Why do we only want to get here if @param level is 0?
            - If level > 0, then moss.key will be used in the function '_build_target'.
            - So, a way to make use of moss.key when level == 0, is to build a dictionary 
              where moss.key points to @param val.
        """
        return {moss.key: moss.transform(val)}

    return moss.transform(val)


def _filter_matched_tags(
        moss: BlueMoss,
        tags: list[HtmlElement | str]
) -> list[HtmlElement | str | None]:
    """ Filter the matched tags. """

    if moss.find_single_tag:
        """ moss.filter is an int => we want to filter for a single tag """
        try:
            return [tags[moss.filter]]
        except IndexError:
            return []

    """ moss.filter is not an int => we want to filter for multiple tags """

    if isinstance(moss.filter, Range):
        """ moss.filter is a Range object => filter for multiple subsequent tags """
        return moss.filter.filter(tags)

    if isinstance(moss.filter, list):
        """ moss.filter is a list of integers => filter for the tags whose index is contained in moss.filter """
        _tags: list[HtmlElement | str | None] = []
        for idx in moss.filter:
            try:
                _tags.append(tags[idx])
            except IndexError:
                _tags.append(None)
        return _tags

    """ moss.filter is None => return all matched tags """
    return tags


def _build_target(
        level: int,
        moss: BlueMoss,
        tag: HtmlElement | str | None
) -> list | dict | Class | None:
    """
    Builds the target instance (list, dict or class/dataclass instance) of :param moss.
    Called by '_extract' function in case :param moss defines its 'nodes' parameter.

    :rtype: list | dict | Class (class/dataclass instance)
    :return:
        1. Class instance if the 'target' param of :param moss is not None.
        2. List or Dict if the 'target' param of :param moss is None:
            2.1: Dict if all nodes in :param moss define their 'key' param.
            2.2: List if all nodes have their 'key' param set to None.
    """

    if tag is None:
        return

    if moss.target is None:
        """ the target type will be derived by """
        if moss.keys_in_nodes:
            """ the target is a dict """
            return PrettyDict({node.key: _extract(level+1, node, tag) for node in moss.nodes})
        """ the target is a list """
        return [_extract(level+1, node, tag) for node in moss.nodes]

    """ the target is a class/dataclass """

    """ :param values: dictionary to instantiate moss.target """
    values: dict[str, any] = {
        node.key: _extract(level+1, node, tag)
        for node in moss.nodes
    }

    if issubclass(moss.target, JsonifyWithTag):
        """ 
        If moss.target inherits from JsonifyWithTag, the intention is to provide 
        the current html-tag @param tag to our target-instance using the key '_tag'.
        """
        values |= {"_tag": tag}

    """ Instantiate and return the target-object. """
    # noinspection PyArgumentList
    return moss.target(**values)


def _extract_from_leaf_node(
        moss: BlueMoss,
        tag: HtmlElement | str | None
) -> any:
    """
    Extracts data from a leaf node.
    A leaf node is a BlueMoss object with an empty 'nodes' list (moss.nodes == []).

    :rtype: any
    :return: data extracted from :param moss.
    """

    if tag is None:
        return None

    if isinstance(tag, str):
        """ 
        @param tag is a string if moss.xpath endswith with e.g. /@href,  /@class or /text(),
        i.e. when we do not select for a tag but for a tag-property, like text or an attribute.
        """
        return str(tag)

    if isinstance(moss.extract, str):
        """ extract the value of the tag-attribute defined by moss.extract """
        return tag.get(moss.extract)

    """ extract data from @param tag by match-casing moss.extract """
    match moss.extract:
        case Ex.FULL_TEXT:
            return utils.clean_text(tag.text_content().strip())
        case Ex.ETREE_ELEMENT:
            return tag
        case Ex.TEXT:
            return tag.text.strip()
        case Ex.BS4_TAG:
            return utils.lxml_etree_to_bs4(tag)
        case Ex.TAG_AS_STRING:
            return utils.lxml_etree_to_bs4(tag).prettify()
        case Ex.HREF:
            return tag.get("href")
        case Ex.HREF_QUERY:
            return utils.get_url_query(tag.get("href"))
        case Ex.HREF_DOMAIN:
            return utils.get_domain(tag.get("href"))
        case Ex.HREF_ENDPOINT:
            return utils.get_endpoint(tag.get("href"))
        case Ex.HREF_BASE_DOMAIN:
            return utils.get_base_domain(tag.get("href"))
        case Ex.HREF_QUERY_PARAMS:
            return utils.get_url_query_params(tag.get("href"))
        case Ex.HREF_ENDPOINT_WITH_QUERY:
            return utils.get_endpoint_with_query(tag.get("href"))
        case _:
            raise NotImplementedError
