from __future__ import annotations
from lxml import etree
from typing import Callable
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from utils import is_valid_xpath, DataClass, update_params_with_defaults


@dataclass
class Recipe:
    path: str = field(default="/")
    context: str | None = field(default=None)
    target: DataClass | None = field(default=None)
    children: list[Recipe] = field(default_factory=list)
    transform: Callable[[str], any] | None = field(default=lambda x: x)

    @property
    def find_all(self) -> bool:
        return not self.path.endswith("]")

    def __post_init__(self):
        """ Some assertions after instance initiation. """

        """ Make sure @param self.path is a valid XPath query. """
        assert is_valid_xpath(self.path)

        """ Make sure that at most one of the value @param target or @param context is specified. """
        assert self.target is None or self.context is None

        if not self.target:
            """
            If no @param target is specified, we expect to have 0 or 1 recipe-children.
            In case we have no recipe children, we will directly extract data from the tag(s) specified by @param path.
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
        target_class_params: set[str] = set(self.target.__dataclass_fields__.keys())
        for recipe in self.children:
            assert recipe.context in target_class_params, \
                f"{recipe.context} is no valid parameter of the target-class"


def extract(recipe: Recipe, html: str) -> any:
    return _extract(recipe, etree.fromstring(str(BeautifulSoup(html, 'lxml'))))


def _extract(recipe: Recipe, root) -> any:
    if not (nodes := root.xpath(recipe.path)):
        return
    if not recipe.children:
        return [recipe.transform(node) for node in nodes]
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
    return recipe.transform(res) if recipe.find_all else recipe.transform(res[0])
