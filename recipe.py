from __future__ import annotations
from copy import deepcopy
from typing import Callable
import utils.url as url_utils
from lxml import html as lxml_html, etree
from typings import Extract, DictableWithTag
from utils.html import is_valid_xpath, etree_to_bs4
from utils.general import update_params_with_defaults
from dataclasses import dataclass, field, is_dataclass, fields


@dataclass(frozen=True)
class Recipe:
    # xpath
    path: str = field(default="")
    path_prefix: str = field(default=".//")
    
    # indices
    start_idx: int = field(default=0)
    end_idx: int | None = field(default=1)
    
    # extraction
    context: str | None = field(default=None)
    target: object | None = field(default=None)
    extract: Extract | str | None = field(default=Extract.TEXT_CONTENT)
    transform: Callable[[str], any] | None = field(default=lambda x: x)
    
    # child recipes
    children: list[Recipe] = field(default_factory=list)

    @property
    def find_single_node(self) -> bool:
        return self.end_idx is not None and abs(self.end_idx - self.start_idx) == 1

    @property
    def find_all_nodes(self) -> bool:
        return self.start_idx == 0 and self.end_idx is None
    
    @property
    def full_path(self):
        return f"{self.path_prefix}{self.path}"
    
    def clone(self) -> Recipe:
        return deepcopy(self)

    def __post_init__(self):
        """ Some assertions after instance initiation. """

        """ Assert that @param self.full_path is a valid XPath query. """
        assert self.full_path is None or is_valid_xpath(self.full_path),\
            f"{self.full_path} is not a valid XPath query."

        """ Assert @param self.target is either None or a dataclass. """
        assert self.target is None or is_dataclass(self.target)

        """ Assert that @param self.transform is either None or a callable. """
        assert self.transform is None or callable(self.transform)

        """ 
        Assert that at lest one but not both parameters 
        @param self.extract and @param self.children are set.
        """
        assert not (self.extract is None and len(self.children) == 0)

        if not self.target:
            """
            If no @param target is specified, we expect to have 0 or 1 recipe-children.
            In case we have no recipe children, we'll directly extract data from the tag(s) specified by @param path.
            In case we have one recipe child, we will not continue our search with that recipe-child.                 
            """
            assert len(self.children) <= 1
            return

        """ @param target is specified. """

        """
        Make sure that we have at least one or more children specified 
        from which we inject the extracted data into @param target.
        """
        assert len(self.children) > 0

        """
        Make sure that all child-recipes have specified their @param context, 
        which translates to the parameter/key of the dataclass @param target,
        i.e. the data extracted from one child-recipe is assigned to exactly 
        one parameter of an instance of @param target.
        """
        assert all([c.context for c in self.children])

        """
        Make sure that the @param context of all children are actual parameters 
        of the dataclass @param target.
        """
        target_class_params: set[str] = set(f.name for f in fields(self.target))
        for recipe in self.children:
            assert recipe.context in target_class_params, \
                f"{recipe.context} is no valid parameter of the target-class"


def extract(recipe: Recipe, html: str) -> any:
    return _extract(
        recipe=recipe,
        root=lxml_html.fromstring(html)
    )


def _extract(recipe: Recipe, root) -> any:
    if recipe.full_path is None:
        nodes = [root]
    elif not (nodes := root.xpath(recipe.full_path)):
        return
    end_index: int = len(nodes) if recipe.end_idx is None else recipe.end_idx
    try:
        nodes = nodes[recipe.start_idx:end_index]
    except IndexError:
        return None
    if not recipe.children:
        res = [
            recipe.transform(_extract_leaf_node(recipe, node))
            for node in nodes
        ]
        return res[0] if recipe.find_single_node else res
    if recipe.target:
        res: list = []
        for node in nodes:
            extracted_fields: dict[str, any] = (
                {
                    _recipe.context: _extract(recipe=_recipe, root=node)
                    for _recipe in recipe.children
                }
                |
                ({"_tag": etree_to_bs4(node)} if issubclass(recipe.target, DictableWithTag) else {})
            )
            updated_fields: dict[str, any] = update_params_with_defaults(recipe.target, extracted_fields)
            res.append(recipe.target(**updated_fields))
    else:
        res: list = [
            _extract(recipe=_recipe, root=node)
            for _recipe in recipe.children
            for node in nodes
        ]
    return recipe.transform(res[0]) if recipe.find_single_node else recipe.transform(res)


def _extract_leaf_node(recipe: Recipe, node: etree.Element) -> any:
    if isinstance(recipe.extract, str):
        return node.get(recipe.extract)
    if not isinstance(recipe.extract, Extract):
        raise ValueError(f"The @param recipe.extract must be a string or Extract value.")
    match recipe.extract:
        case None | Extract.ETREE:
            return node
        case Extract.TEXT:
            return node.text.strip()
        case Extract.TEXT_CONTENT:
            return node.text_content().strip()
        case Extract.TAG:
            return etree_to_bs4(node)
        case Extract.TAG_AS_STRING:
            return etree_to_bs4(node).prettify()
        case Extract.HREF:
            return node.get("href")
        case Extract.HREF_QUERY:
            return url_utils.get_query(node.get("href"))
        case Extract.HREF_DOMAIN:
            return url_utils.get_domain(node.get("href"))
        case Extract.HREF_ENDPOINT:
            return url_utils.get_endpoint(node.get("href"))
        case Extract.HREF_BASE_DOMAIN:
            return url_utils.get_base_domain(node.get("href"))
        case Extract.HREF_QUERY_PARAMS:
            return url_utils.get_query_params(node.get("href"))
        case Extract.HREF_ENDPOINT_WITH_QUERY:
            return url_utils.get_endpoint_with_query(node.get("href"))
