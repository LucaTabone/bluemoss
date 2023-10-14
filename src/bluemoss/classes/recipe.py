from __future__ import annotations
from . import Extract
from .range import Range
from typing import Callable
from ..utils import is_valid_xpath
from dataclasses import dataclass, field, is_dataclass, fields


@dataclass(frozen=True)
class Recipe:
    # xpath
    path: str = field(default="")
    path_prefix: str = field(default=".//")
    
    # search range
    range: Range = Range(0, 1)
    
    # extraction
    context: str | None = field(default=None)
    target: object | None = field(default=None)
    transform: Callable[[str], any] | None = field(default=lambda x: x)
    extract: Extract | str | None = field(default=Extract.TEXT_CONTENT_CLEAN)
    
    # child recipes
    children: list[Recipe] = field(default_factory=list)
    
    @property
    def full_path(self):
        return f"{self.path_prefix}{self.path}"

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
