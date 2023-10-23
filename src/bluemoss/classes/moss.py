from __future__ import annotations
import builtins
from .utils import ClassType
from .extract import Ex
from .range import Range
from inspect import isclass
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
        if not (self.no_path or is_valid_xpath(self.full_path)):
            raise InvalidXpathException(self)

        if not (
                all([c.key is not None for c in self.nodes]) or
                all([c.key is None for c in self.nodes])
        ):
            raise PartialKeysException()
            
        if self.target is None:
            return

        if not isclass(self.target) or self.target.__name__ in dir(builtins):
            raise InvalidTargetTypeException(self)

        if not self.keys_in_nodes.issubset(get_class_init_params(self.target)):
            raise InvalidKeysForTargetException(self)


@dataclass(frozen=True)
class Root(BlueMoss):
    path_prefix: str = field(default="//", init=False)


@dataclass(frozen=True)
class Node(BlueMoss):
    path_prefix: str = field(default=".//", init=False)


class InvalidXpathException(Exception):
    def __init__(self, moss: BlueMoss):
        message: str = (
            f"\n{moss.full_path} seems to be an invalid xpath. "
            f"Feel free to use ChatGPT to check if your path is compatible with the XPath 1.0 syntax. "
            f"Note that xpath queries using XPath syntax of any version higher than 1.0 are not supported."
        )
        super().__init__(message)


class PartialKeysException(Exception):
    def __init__(self):
        message: str = (
            f"\n\nSome Node instances in your nodes list have a key attribute set while others don't."
            f"\nYou can either provide a list of nodes where ALL instances set a key, or NO instances do."
        )
        super().__init__(message)


class InvalidTargetTypeException(Exception):
    def __init__(self, moss: BlueMoss):
        message: str = (
            f"\n\nThe type of your target '{str(moss.target)}' is not a custom class nor a dataclass."
            f"\nMake sure the target either refers to a class or a dataclass."
            f"\n\nPro Tips:"
            f"\n1) If you want your target to be a DICT, "
            f"then you don't have to set the 'target' parameter. All you have to do is to provide keys "
            f"with all Node instances in your 'nodes' list."
            f"\n2) If you want your target to be a LIST, then you also don't need to set your 'target' parameter. "
            f"Just provide the list of Node instances in your 'nodes' list "
            f"without any of the Node instances having set the 'key' parameter."
        )
        super().__init__(message)


class InvalidKeysForTargetException(Exception):
    def __init__(self, moss: BlueMoss):
        target_fields: set[str] = get_class_init_params(moss.target)
        invalid_fields: set[str] = {field for field in moss.keys_in_nodes if field not in target_fields}
        message: str = (
            f"A Node instance in your 'nodes' list defines a key that is no valid init "
            f"parameter for your target {str(moss.target)}: {invalid_fields.pop()}"
        )
        super().__init__(message)


__all__ = [
    "BlueMoss",
    "Root",
    "Node",
    "InvalidXpathException",
    "PartialKeysException",
    "InvalidTargetTypeException",
    "InvalidKeysForTargetException"
]
