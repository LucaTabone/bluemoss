from lxml import html as lxml_html
from .classes import Extract, Moss, DictableWithTag, PrettyDict
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


def extract(moss: Moss, html: str) -> any:
    return _extract(
        moss=moss,
        root=lxml_html.fromstring(html)
    )


def _extract(moss: Moss, root) -> any:
    if moss.full_path is None:
        nodes = [root]
    elif not (nodes := root.xpath(moss.full_path)):
        if moss.extract == Extract.FOUND:
            return False
        return
    end_index: int = len(nodes) if moss.range.end_idx is None else moss.range.end_idx
    try:
        nodes = nodes[moss.range.start_idx:end_index]
        if moss.range.reverse:
            nodes = nodes[::-1]
    except IndexError:
        return None
    if not moss.children:
        res = [
            moss.transform(_extract_leaf_node(moss, node))
            for node in nodes
        ]
        return res[0] if moss.range.find_single else res
    if moss.target or moss.target_is_dict or moss.target_is_list:
        res: list = [_build_target_instance(moss, node) for node in nodes]
    else:
        res: list = [
            _extract(moss=_moss, root=node)
            for _moss in moss.children
            for node in nodes
        ]
    return moss.transform(res[0]) if moss.range.find_single else moss.transform(res)


def _extract_leaf_node(moss: Moss, node) -> any:
    if type(node).__name__ == '_ElementUnicodeResult':
        return str(node)
    if isinstance(moss.extract, str):
        return node.get(moss.extract)
    if not isinstance(moss.extract, Extract):
        raise ValueError(f"The @param moss.extract must be a string or Extract value.")
    match moss.extract:
        case None | Extract.ETREE:
            return node
        case Extract.FOUND:
            return node is not None
        case Extract.TEXT:
            return node.text.strip()
        case Extract.TEXT_CONTENT:
            return node.text_content().strip()
        case Extract.TEXT_CONTENT_CLEAN:
            return clean_text(node.text_content())
        case Extract.TAG:
            return etree_to_bs4(node)
        case Extract.TAG_AS_STRING:
            return etree_to_bs4(node).prettify()
        case Extract.HREF:
            return node.get("href")
        case Extract.HREF_QUERY:
            return get_url_query(node.get("href"))
        case Extract.HREF_DOMAIN:
            return get_domain(node.get("href"))
        case Extract.HREF_ENDPOINT:
            return get_endpoint(node.get("href"))
        case Extract.HREF_BASE_DOMAIN:
            return get_base_domain(node.get("href"))
        case Extract.HREF_QUERY_PARAMS:
            return get_url_query_params(node.get("href"))
        case Extract.HREF_ENDPOINT_WITH_QUERY:
            return get_endpoint_with_query(node.get("href"))


def _build_target_instance(moss: Moss, node):
    if moss.target_is_dict:
        return PrettyDict({c.key: _extract(moss=c, root=node) for c in moss.children})
    elif moss.target_is_list:
        return [_extract(moss=c, root=node) for c in moss.children]
    values: dict[str, any] = {}
    params_with_defaults: set[str] = get_params_with_default_value(moss.target)
    for _moss in moss.children:
        val: any = _extract(moss=_moss, root=node)
        if not (val is None and _moss.key in params_with_defaults):
            values[_moss.key] = val
    if issubclass(moss.target, DictableWithTag):
        values |= {"_tag": node}
    return moss.target(**values)
