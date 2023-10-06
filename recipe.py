from __future__ import annotations
from lxml import etree
from typing import Callable
from typings import Extract
from bs4 import BeautifulSoup
from dataclasses import dataclass, field, is_dataclass, fields
from utils import is_valid_xpath, update_params_with_defaults, etree_to_bs4


@dataclass
class Recipe:
    path: str = field(default="/")
    end_index: int = field(default=1)
    start_index: int = field(default=0)
    context: str | None = field(default=None)
    target: object | None = field(default=None)
    extract: Extract | str | None = field(default=None)
    children: list[Recipe] = field(default_factory=list)
    transform: Callable[[str], any] | None = field(default=lambda x: x)

    @property
    def find_single_node(self) -> bool:
        return self.end_index is not None and abs(self.end_index - self.start_index) == 1

    def __post_init__(self):
        """ Some assertions after instance initiation. """

        """ Assert that @param self.path is a valid XPath query. """
        assert is_valid_xpath(self.path)

        """ Assert @param self.target is either None or a dataclass. """
        assert self.target is None or is_dataclass(self.target)

        """ Assert that @param self.transform is either None or a callable. """
        assert self.transform is None or callable(self.transform)

        """ Assert that @param self.extract is either None or a valid Extract. """
        assert self.extract is None or isinstance(self.extract, Extract)

        """ 
        Assert that at lest one but not both parameters 
        @param self.extract and @param self.children are set.
        """
        assert not (self.extract is None and len(self.children) == 0)

        """ Assert that at most one of the value @param target or @param context is specified. """
        assert self.target is None or self.context is None

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
    return _extract(recipe, etree.fromstring(str(BeautifulSoup(html, 'lxml'))))


def _extract(recipe: Recipe, root) -> any:
    if not (nodes := root.xpath(recipe.path)):
        return
    try:
        nodes = nodes[recipe.start_index:recipe.end_index]
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
            extracted_fields: dict[str, any] = {
                _recipe.context: _extract(recipe=_recipe, root=node)
                for _recipe in recipe.children
            }
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
        # extract tag property directly
        return node.get(recipe.extract)
    if not isinstance(recipe.extract, Extract):
        raise ValueError(f"The @param recipe.extract must be a string or Extract value.")
    match recipe.extract:
        case None | Extract.ETREE:
            return node
        case Extract.TEXT:
            return node.text.strip()
        case Extract.TAG:
            return etree_to_bs4(node)
        case Extract.TAG_AS_STRING:
            return etree_to_bs4(node).prettify()
