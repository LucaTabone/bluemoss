from lxml import html as lxml_html
from .classes import Ex, BlueMoss, DictableWithTag, PrettyDict
from .utils import (
    clean_text,
    get_domain,
    etree_to_bs4,
    get_endpoint,
    get_url_query,
    get_base_domain,
    get_url_query_params,
    get_endpoint_with_query,
    get_params_with_default_value,
)


def extract(moss: BlueMoss, html: str) -> any:
    return _extract(moss, lxml_html.fromstring(html))


def _extract(moss: BlueMoss, root) -> any:
    if not (nodes := root.xpath(moss.full_path)):
        if moss.extract == Ex.FOUND:
            return False
        return
    end_index: int = len(nodes) if moss.range.end_idx is None else moss.range.end_idx
    try:
        nodes = nodes[moss.range.start_idx:end_index]
        if moss.range.reverse:
            nodes = nodes[::-1]
    except IndexError:
        return None
    if not moss.nodes:
        res = [
            moss.transform(_extract_from_leaf_node(moss, node))
            for node in nodes
        ]
        return (res[0] if res else None) if moss.range.find_single else res
    if moss.target or moss.target_is_dict or moss.target_is_list:
        res: list = [_build_target_instance(moss, node) for node in nodes]
    else:
        res: list = [
            _extract(_moss, node)
            for _moss in moss.nodes
            for node in nodes
        ]
    return moss.transform(res[0] if res else None) if moss.range.find_single else moss.transform(res)


def _extract_from_leaf_node(moss: BlueMoss, node) -> any:
    if type(node).__name__ == '_ElementUnicodeResult':
        return str(node)
    if isinstance(moss.extract, str):
        return node.get(moss.extract)
    if not isinstance(moss.extract, Ex):
        raise ValueError(f"The @param moss.extract must be a string or Extract value.")
    match moss.extract:
        case None | Ex.ETREE:
            return node
        case Ex.FOUND:
            return node is not None
        case Ex.TEXT:
            return node.text.strip()
        case Ex.FULL_TEXT:
            return clean_text(node.text_content().strip())
        case Ex.TAG:
            return etree_to_bs4(node)
        case Ex.TAG_AS_STRING:
            return etree_to_bs4(node).prettify()
        case Ex.HREF:
            return node.get("href")
        case Ex.HREF_QUERY:
            return get_url_query(node.get("href"))
        case Ex.HREF_DOMAIN:
            return get_domain(node.get("href"))
        case Ex.HREF_ENDPOINT:
            return get_endpoint(node.get("href"))
        case Ex.HREF_BASE_DOMAIN:
            return get_base_domain(node.get("href"))
        case Ex.HREF_QUERY_PARAMS:
            return get_url_query_params(node.get("href"))
        case Ex.HREF_ENDPOINT_WITH_QUERY:
            return get_endpoint_with_query(node.get("href"))


def _build_target_instance(moss: BlueMoss, node):
    if moss.target_is_dict:
        return PrettyDict({c.key: _extract(c, node) for c in moss.nodes})
    elif moss.target_is_list:
        return [_extract(c, node) for c in moss.nodes]
    values: dict[str, any] = {}
    params_with_defaults: set[str] = get_params_with_default_value(moss.target)
    for _moss in moss.nodes:
        val: any = _extract(_moss, node)
        if not (val is None and _moss.key in params_with_defaults):
            values[_moss.key] = val
    if issubclass(moss.target, DictableWithTag):
        values |= {"_tag": node}
    return moss.target(**values)
