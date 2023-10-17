from lxml import html as lxml_html
from .classes import Ex, BlueMoss, Range, DictableWithTag, PrettyDict
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
    if not (elems := root.xpath(moss.full_path)):
        if moss.extract == Ex.FOUND:
            return False
        return
    try:
        if isinstance(moss.filter, int):
            elems = [elems[moss.filter]]
        elif isinstance(moss.filter, Range):
            elems = moss.filter.filter(elems)
    except IndexError:
        return None
    if not moss.nodes:
        res = [
            moss.transform(_extract_from_leaf_node(moss, elem))
            for elem in elems
        ]
        return (res[0] if res else None) if moss.find_single else res
    if moss.target or moss.target_is_dict or moss.target_is_list:
        res: list = [_build_target_instance(moss, elem) for elem in elems]
    else:
        res: list = [
            _extract(_moss, elem)
            for _moss in moss.nodes
            for elem in elems
        ]
    return moss.transform(res[0] if res else None) if moss.find_single else moss.transform(res)


def _extract_from_leaf_node(moss: BlueMoss, elem) -> any:
    if type(elem).__name__ == '_ElementUnicodeResult':
        return str(elem)
    if isinstance(moss.extract, str):
        return elem.get(moss.extract)
    if not isinstance(moss.extract, Ex):
        raise ValueError(f"The @param moss.extract must be a string or Extract value.")
    match moss.extract:
        case None | Ex.ETREE:
            return elem
        case Ex.FOUND:
            return elem is not None
        case Ex.TEXT:
            return elem.text.strip()
        case Ex.FULL_TEXT:
            return clean_text(elem.text_content().strip())
        case Ex.TAG:
            return etree_to_bs4(elem)
        case Ex.TAG_AS_STRING:
            return etree_to_bs4(elem).prettify()
        case Ex.HREF:
            return elem.get("href")
        case Ex.HREF_QUERY:
            return get_url_query(elem.get("href"))
        case Ex.HREF_DOMAIN:
            return get_domain(elem.get("href"))
        case Ex.HREF_ENDPOINT:
            return get_endpoint(elem.get("href"))
        case Ex.HREF_BASE_DOMAIN:
            return get_base_domain(elem.get("href"))
        case Ex.HREF_QUERY_PARAMS:
            return get_url_query_params(elem.get("href"))
        case Ex.HREF_ENDPOINT_WITH_QUERY:
            return get_endpoint_with_query(elem.get("href"))


def _build_target_instance(moss: BlueMoss, elem):
    if moss.target_is_dict:
        return PrettyDict({c.key: _extract(c, elem) for c in moss.nodes})
    elif moss.target_is_list:
        return [_extract(c, elem) for c in moss.nodes]
    values: dict[str, any] = {}
    params_with_defaults: set[str] = get_params_with_default_value(moss.target)
    for _moss in moss.nodes:
        val: any = _extract(_moss, elem)
        if not (val is None and _moss.key in params_with_defaults):
            values[_moss.key] = val
    if issubclass(moss.target, DictableWithTag):
        values |= {"_tag": elem}
    return moss.target(**values)
