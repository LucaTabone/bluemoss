from __future__ import annotations
from . import Ex
from typing import Type
from .range import Range
from inspect import isclass
from functools import cached_property
from dataclasses import dataclass, field
from ..utils import is_valid_xpath, get_init_params


@dataclass(frozen=True)
class Root:
    # xpath
    path: str
    path_prefix: str = field(default="//")
    
    # search range
    range: Range = Range(0, 1)
    
    # extraction
    key: str | None = field(default=None)
    target: Type[any] | None = field(default=None)
    transform: callable = field(default=lambda x: x)
    extract: Ex | str = field(default=Ex.TEXT_CONTENT_CLEAN)
    
    # child nodes
    children: list[Root | Node] = field(default_factory=list)
    
    @cached_property
    def full_path(self):
        return f"{self.path_prefix}{self.path}"

    @cached_property
    def target_is_dict(self) -> bool:
        return self.target is None and all([c.key for c in self.children])

    @cached_property
    def target_is_list(self) -> bool:
        return self.target is None and len(self.children) > 1 and all([c.key is None for c in self.children])

    @cached_property
    def keys_in_children(self) -> set[str]:
        return {c.key for c in self.children if c.key is not None}

    def __post_init__(self):
        """ Some assertions after instance initiation. """

        assert is_valid_xpath(self.full_path), f"{self.full_path} is not a valid XPath query."

        assert len(self.children) <= 1 or self.target or self.target_is_list or self.target_is_dict
            
        if self.target is None:
            return

        assert isclass(self.target)

        assert get_init_params(self.target)

        assert self.keys_in_children.issubset(get_init_params(self.target))


@dataclass(frozen=True)
class Node(Root):
    path_prefix: str = field(default=".//")
