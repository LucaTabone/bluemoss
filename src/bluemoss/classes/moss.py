from __future__ import annotations
from . import Ex
from .range import Range
from inspect import isclass
from .utils import ClassType
from functools import cached_property
from dataclasses import dataclass, field
from ..utils import is_valid_xpath, get_class_init_params


@dataclass(frozen=True)
class BlueMoss:
    path: str = ""
    path_prefix: str = ""
    key: str | None = None
    filter: int | None | Range = 0
    target: ClassType | None = None
    extract: Ex | str = Ex.FULL_TEXT
    transform: callable = lambda x: x
    nodes: list[Node] = field(default_factory=list)

    @property
    def no_path(self) -> bool:
        return self.path == ""

    @property
    def find_single(self) -> bool:
        return isinstance(self.filter, int)
    
    @cached_property
    def full_path(self):
        return f"{self.path_prefix}{self.path}"

    @cached_property
    def keys_in_nodes(self) -> set[str]:
        return {c.key for c in self.nodes if c.key is not None}

    def __post_init__(self):
        assert self.no_path or is_valid_xpath(self.full_path), f"{self.full_path} is not a valid XPath query."

        assert all([c.key is not None for c in self.nodes]) or all([c.key is None for c in self.nodes])
            
        if self.target:
            assert isclass(self.target)
            assert self.keys_in_nodes.issubset(get_class_init_params(self.target))


@dataclass(frozen=True)
class Root(BlueMoss):
    path_prefix: str = field(default="//", init=False)


@dataclass(frozen=True)
class Node(BlueMoss):
    path_prefix: str = field(default=".//", init=False)
