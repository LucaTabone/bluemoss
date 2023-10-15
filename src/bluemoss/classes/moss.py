from __future__ import annotations
from . import Extract
from .range import Range
from inspect import isclass
from typing import Callable, Type
from dataclasses import dataclass, field
from ..utils import is_valid_xpath, get_init_params


@dataclass(frozen=True)
class Moss:
    # xpath
    path: str = field(default="")
    path_prefix: str = field(default=".//")
    
    # search range
    range: Range = Range(0, 1)
    
    # extraction
    key: str | None = field(default=None)
    target: Type[any] | None = field(default=None)
    transform: Callable[[str], any] | None = field(default=lambda x: x)
    extract: Extract | str | None = field(default=Extract.TEXT_CONTENT_CLEAN)
    
    # child nodes
    children: list[Moss] = field(default_factory=list)
    
    @property
    def full_path(self):
        return f"{self.path_prefix}{self.path}"

    @property
    def target_is_dict(self) -> bool:
        return self.target is None and all([c.key for c in self.children])

    def __post_init__(self):
        """ Some assertions after instance initiation. """

        """ Assert that @param self.full_path is a valid XPath query. """
        assert self.full_path is None or is_valid_xpath(self.full_path),\
            f"{self.full_path} is not a valid XPath query."

        """ 
        Assert that at lest one but not both parameters 
        @param self.extract and @param self.children are set.
        """
        assert not (self.extract is None and len(self.children) == 0)

        """
        Make sure that all children have specified their @param key, 
        which translates to the parameter/key of the dataclass @param target,
        i.e. the data extracted from one child-moss is assigned to exactly 
        one parameter of an instance of @param target.
        """
        if len(self.children) > 1:
            keys: set[str] = {c.key for c in self.children if c.key}
            assert len(self.children) == len(keys)
            
        if self.target is None:
            return

        assert isclass(self.target)

        """
        Make sure that the @param key of all children are actual parameters 
        of the dataclass @param target.
        """
        class_params: set[str] = get_init_params(self.target)
        for c in self.children:
            assert c.key in class_params, \
                f"'{c.key}' is no initialization-parameter of class '{self.target.__name__}'"
