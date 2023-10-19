from __future__ import annotations
from . import Ex
from typing import Type
from .range import Range
from inspect import isclass
from functools import cached_property
from dataclasses import dataclass, field
from ..utils import is_valid_xpath, get_init_params


@dataclass(frozen=True)
class BlueMoss:
    path: str = ""
    path_prefix: str = ""
    key: str | None = None
    filter: int | None | Range = 0
    target: Type[any] | None = None
    extract: Ex | str = Ex.FULL_TEXT
    transform: callable = lambda x: x
    nodes: list[BlueMoss] = field(default_factory=list)
    
    @cached_property
    def full_path(self):
        return f"{self.path_prefix}{self.path}"

    @cached_property
    def target_is_dict(self) -> bool:
        return self.target is None and all([c.key for c in self.nodes])

    @cached_property
    def target_is_list(self) -> bool:
        return self.target is None and all([c.key is None for c in self.nodes])

    @cached_property
    def keys_in_nodes(self) -> set[str]:
        return {c.key for c in self.nodes if c.key is not None}

    @property
    def find_single(self) -> bool:
        return isinstance(self.filter, int)

    @property
    def no_path(self) -> bool:
        return self.path == ""

    def __post_init__(self):
        """ Some assertions after instance initiation. """

        assert is_valid_xpath(self.full_path) or self.no_path, f"{self.full_path} is not a valid XPath query."

        assert self.target or self.target_is_list or self.target_is_dict
            
        if self.target is None:
            return

        assert isclass(self.target)

        assert get_init_params(self.target)

        assert self.keys_in_nodes.issubset(get_init_params(self.target))


@dataclass(frozen=True)
class Root(BlueMoss):
    path_prefix: str = field(default="//")


@dataclass(frozen=True)
class Node(BlueMoss):
    path_prefix: str = field(default=".//")
