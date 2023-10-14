from lxml import html as lxml_html
from .classes import Extract, Recipe, DictableWithTag
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


def extract(recipe: Recipe, html: str) -> any:
    return _extract(
        recipe=recipe,
        root=lxml_html.fromstring(html)
    )


def _extract(recipe: Recipe, root) -> any:
    if recipe.full_path is None:
        nodes = [root]
    elif not (nodes := root.xpath(recipe.full_path)):
        if recipe.extract == Extract.FOUND:
            return False
        return
    end_index: int = len(nodes) if recipe.range.end_idx is None else recipe.range.end_idx
    try:
        nodes = nodes[recipe.range.start_idx:end_index]
        if recipe.range.reverse:
            nodes = nodes[::-1]
    except IndexError:
        return None
    if not recipe.children:
        res = [
            recipe.transform(_extract_leaf_node(recipe, node))
            for node in nodes
        ]
        return res[0] if recipe.range.find_single else res
    if recipe.target:
        res: list = [_build_target_instance(recipe, node) for node in nodes]
    else:
        res: list = [
            _extract(recipe=_recipe, root=node)
            for _recipe in recipe.children
            for node in nodes
        ]
    return recipe.transform(res[0]) if recipe.range.find_single else recipe.transform(res)


def _extract_leaf_node(recipe: Recipe, node) -> any:
    if type(node).__name__ == '_ElementUnicodeResult':
        return str(node)
    if isinstance(recipe.extract, str):
        return node.get(recipe.extract)
    if not isinstance(recipe.extract, Extract):
        raise ValueError(f"The @param recipe.extract must be a string or Extract value.")
    match recipe.extract:
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


def _build_target_instance(recipe: Recipe, node):
    values: dict[str, any] = {}
    params_with_defaults: set[str] = get_params_with_default_value(recipe.target)
    for _recipe in recipe.children:
        val: any = _extract(recipe=_recipe, root=node)
        if not (val is None and _recipe.context in params_with_defaults):
            values[_recipe.context] = val
    if issubclass(recipe.target, DictableWithTag):
        values |= {"_tag": node}
    return recipe.target(**values)
