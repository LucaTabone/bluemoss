from . import utils
from lxml import etree, html as lxml_html
from .classes import Ex, BlueMoss, Range, JsonifyWithTag, PrettyDict


def extract(moss: BlueMoss, html: str) -> any:
    return _extract(moss, lxml_html.fromstring(html), 0)


def _extract(moss: BlueMoss, root: etree.Element, level: int) -> any:
    if moss.no_path:
        elems = [root]
    elif not (elems := root.xpath(moss.full_path)):
        if moss.extract == Ex.FOUND:
            return False
        return moss.transform(None if isinstance(moss.filter, int) else [])
    try:
        if isinstance(moss.filter, int):
            elems = [elems[moss.filter]]
        elif isinstance(moss.filter, Range):
            elems = moss.filter.filter(elems)
    except IndexError:
        return moss.transform(None if isinstance(moss.filter, int) else [])
    if moss.nodes:
        if moss.find_single:
            val = moss.transform(_build_target_instance(moss, elems[0], level))
        else:
            val = moss.transform([
                _build_target_instance(moss, elem, level)
                for elem in elems
            ])
    elif moss.find_single:
        val = moss.transform(_extract_from_leaf_node(moss, elems[0]))
    else:
        val = moss.transform([
            _extract_from_leaf_node(moss, elem)
            for elem in elems
        ])
    if moss.key is not None and level == 0:
        return {moss.key: val}
    return val


def _build_target_instance(moss: BlueMoss, elem: etree.Element, level: int):
    if moss.target is None:
        if moss.keys_in_nodes:
            return PrettyDict({node.key: _extract(node, elem, level+1) for node in moss.nodes})
        return [_extract(node, elem, level+1) for node in moss.nodes]
    values: dict[str, any] = {}
    params_with_defaults: set[str] = utils.get_class_params_with_default_value(moss.target)
    for node in moss.nodes:
        val: any = _extract(node, elem, level+1)
        if not (val is None and node.key in params_with_defaults):
            values[node.key] = val
    if issubclass(moss.target, JsonifyWithTag):
        values |= {"_tag": elem}
    # noinspection PyArgumentList
    return moss.target(**values)


def _extract_from_leaf_node(moss: BlueMoss, elem: etree.Element) -> any:
    if type(elem).__name__ == '_ElementUnicodeResult':
        return str(elem)
    if isinstance(moss.extract, str):
        return elem.get(moss.extract)
    match moss.extract:
        case None | Ex.ETREE:
            return elem
        case Ex.FOUND:
            return elem is not None
        case Ex.TEXT:
            return elem.text.strip()
        case Ex.FULL_TEXT:
            return utils.clean_text(elem.text_content().strip())
        case Ex.TAG:
            return utils.etree_to_bs4(elem)
        case Ex.TAG_AS_STRING:
            return utils.etree_to_bs4(elem).prettify()
        case Ex.HREF:
            return elem.get("href")
        case Ex.HREF_QUERY:
            return utils.get_url_query(elem.get("href"))
        case Ex.HREF_DOMAIN:
            return utils.get_domain(elem.get("href"))
        case Ex.HREF_ENDPOINT:
            return utils.get_endpoint(elem.get("href"))
        case Ex.HREF_BASE_DOMAIN:
            return utils.get_base_domain(elem.get("href"))
        case Ex.HREF_QUERY_PARAMS:
            return utils.get_url_query_params(elem.get("href"))
        case Ex.HREF_ENDPOINT_WITH_QUERY:
            return utils.get_endpoint_with_query(elem.get("href"))
