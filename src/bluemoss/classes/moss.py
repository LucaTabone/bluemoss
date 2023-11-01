from __future__ import annotations
import builtins
from .extract import Ex
from .range import Range
from inspect import isclass
from functools import cached_property
from typing import Callable, Type, Any
from dataclasses import dataclass, field
from ..utils import (
    is_valid_xpath,
    get_all_class_init_params,
    get_required_class_init_params,
)


@dataclass(frozen=True)
class BlueMoss:
    """
    A BlueMoss object is a recipe that describes:

    1. What data to extract from which tags.
    2. How to further transform the extracted data.
    3. Where to place the transformed data, e.g. in a class, dataclass, dict, or list.

    :param xpath:
        The xpath used to find e.g. a single tag, multiple tags, a tag-attribute value, etc.
    :param xpath_prefix:
        An optional prefix to prepend to the `xpath`, e.g. '/', '//', './' or './/'. Useful for defining subclasses
        of BlueMoss, like 'Root' and 'Node', which might use common xpath prefixes such as `.//` for `Root` and `//`
        for `Node`. This simplifies the creation of BlueMoss objects by avoiding manual prefixing of every `xpath`.
    :param target:
        Specifies the class or dataclass to wrap the extracted data. Requires all objects in `nodes` to set their
        'key' parameter to a non-None value. If `target` is None but `nodes` is populated, the extracted data will
        be wrapped in a dict or list, depending on whether all instances in `nodes` set their `key` parameter.
    :param key:
        An optional key for the extracted data. Depending on the parent BlueMoss object's settings, a `key` will
        place the data in a dict or a class/dataclass.
    :param nodes:
        A list of child nodes (BlueMoss instances) for extracting multiple data points from tags matched against
        `full_path`. All BlueMoss instances in `nodes` should either set a 'key' value or none at all.
    :param extract:
        A string or an Ex enum value denoting the data to extract from an HTML tag. If `extract` is a string,
        the function will try to extract the value of the HTML tag attribute specified by `extract`.
    :param transform:
        A Callable for further processing of the extracted data.
    :param filter:
        Enables filtering for specific tags matched against `full_path`. It can be:
        1. int: From all matched tags, the int value denotes the index of the desired HTML tag.
        2. list[int]: A list of ints representing indices of matched tags of interest.
        3. Range: A Range object (see ./range.py for documentation).
        4. None: No filtering is applied; data is extracted from all matched tags.
    """

    xpath: str = ''
    xpath_prefix: str = ''
    key: str | None = None
    target: Type[Any] | None = None
    extract: Ex | str = Ex.FULL_TEXT
    filter: int | list[int] | Range | None = 0
    transform: Callable[[Any], Any] = lambda x: x
    nodes: list[Node] = field(default_factory=list)

    @property
    def no_xpath(self) -> bool:
        """
        :rtype: bool
        :return: True if no xpath was provided, False otherwise.
        """
        return self.xpath == ''

    @property
    def find_single_tag(self) -> bool:
        """
        :rtype: bool
        :return: True if only one tag should be filtered out of the matched tags, False otherwise.
        """
        return isinstance(self.filter, int)

    @cached_property
    def full_xpath(self) -> str:
        """
        :rtype: str
        :return: The xpath to use when querying html with the extract function.
        """
        return f'{self.xpath_prefix}{self.xpath}'

    @cached_property
    def keys_in_nodes(self) -> set[str]:
        """
        If this set is not empty, then we use these keys in the dictionary that instantiates a target object:
            1) If the target value of the parent-node (if any) is not None,
               then we instantiate that class using the dict.
            2) If the target value of the parent node is None, then we simply use the dict as the target object.

        :rtype: set[str]
        :return: The set of all keys in the :param nodes.
        """
        return {c.key for c in self.nodes if c.key is not None}

    @cached_property
    def target_class_name(self) -> str | None:
        if self.target is None:
            return None
        return self.target.__name__

    def __post_init__(self) -> None:
        if not (self.no_xpath or is_valid_xpath(self.full_xpath)):
            """Check the provided xpath for syntactical correctness."""
            raise InvalidXpathException(self)

        if not (
            all([c.key is not None for c in self.nodes])
            or all([c.key is None for c in self.nodes])
        ):
            """
            Asserts that either all (or none) of the BlueMoss instances in :param nodes set the 'key' param.
            - In case none of the instances set a key value, the target object will be a list.
            - I case all of the instances set a value for the 'key' param , then the target is either a dict
              or a class/dataclass, depending on whether the parent node has set a value for the 'target' param.
              If it hasn't, then the target is a dict.
            """
            raise PartialKeysException(self)

        if self.target is None:
            """Early return in case no target was provided."""
            return

        if not isclass(self.target) or self.target.__name__ in dir(builtins):
            """Make sure the value of the 'target' param references a class, which is not a builtin class."""
            raise InvalidTargetTypeException(self)

        if not self.keys_in_nodes.issubset(
            get_all_class_init_params(self.target)
        ):
            """
            Make sure that all keys provided in the instances of the 'nodes'
            param are valid init params for the target class.
            """
            raise InvalidKeysForTargetException(self)

        if not get_required_class_init_params(self.target).issubset(
            self.keys_in_nodes
        ):
            """
            Make sure that the instances in the 'nodes' param cover all mandatory
            initialization parameters of the target class.
            """
            raise MissingTargetKeysException(self)


@dataclass(frozen=True)
class Root(BlueMoss):
    """
    BlueMoss subclass which comes with :param xpath_prefix set to '//'.
    This class is suited to be used as the most outer parent node in a BlueMoss tree.
    """

    xpath_prefix: str = field(default='//', init=False)


@dataclass(frozen=True)
class Node(BlueMoss):
    """
    BlueMoss subclass which comes with :param xpath_prefix set to './/'.
    This class is suited to be used as a child node in a BlueMoss tree as the preceding '.' char
    tells us to match :param full_path against the tag(s) matched in the parent node.
    """

    xpath_prefix: str = field(default='.//', init=False)


class InvalidXpathException(Exception):
    def __init__(self, moss: BlueMoss):
        message: str = (
            f'\n{moss.full_xpath} seems to be an invalid xpath. '
            f'\nFeel free to use ChatGPT to check if your path is compatible with the XPath 1.0 syntax.'
            f'\nNote that xpath queries using XPath syntax of any version higher than 1.0 are not supported.'
        )
        super().__init__(message)


class PartialKeysException(Exception):
    def __init__(self, moss: BlueMoss):
        message: str = (
            f"\n\nSome Node instances in your nodes list have a key attribute set while others don't."
            f'\nYou can either provide a list of nodes where ALL instances set a key, or NO instances do.'
        )
        super().__init__(message)


class InvalidTargetTypeException(Exception):
    def __init__(self, moss: BlueMoss):
        message: str = (
            f"\n\nThe type of your target '{moss.target_class_name}' is not a custom class nor a dataclass."
            f'\nMake sure the target either refers to a class or a dataclass.'
            f'\n\nPro Tips:'
            f'\n1) If you want your target to be a DICT, '
            f"then you don't have to set the 'target' parameter. All you have to do is to provide keys "
            f"with all Node instances in your 'nodes' list."
            f"\n2) If you want your target to be a LIST, then you also don't need to set your 'target' parameter. "
            f"Just provide the list of Node instances in your 'nodes' list "
            f"without any of the Node instances having set the 'key' parameter."
        )
        super().__init__(message)


class InvalidKeysForTargetException(Exception):
    def __init__(self, moss: BlueMoss):
        invalid_keys: set[str] = {
            key
            for key in moss.keys_in_nodes
            if key not in get_all_class_init_params(moss.target)
        }
        message: str = (
            f'A Node instance in your nodes list defines a key that is no valid init '
            f'parameter for your target {moss.target_class_name}: {invalid_keys.pop()}'
        )
        super().__init__(message)


class MissingTargetKeysException(Exception):
    def __init__(self, moss: BlueMoss):
        missing_keys: list[str] = sorted(
            list(
                (
                    get_required_class_init_params(moss.target)
                    - moss.keys_in_nodes
                )
            )
        )
        message: str = f"\n\nMissing keys in nodes list for target '{moss.target_class_name}': {missing_keys}"
        super().__init__(message)


__all__ = [
    'BlueMoss',
    'Root',
    'Node',
    'InvalidXpathException',
    'PartialKeysException',
    'MissingTargetKeysException',
    'InvalidTargetTypeException',
    'InvalidKeysForTargetException',
]
