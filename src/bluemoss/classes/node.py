from __future__ import annotations
import builtins
from .extract import Ex
from .range import Range
from inspect import isclass
from typing import Callable, Type, Any
from dataclasses import dataclass, field
from ..utils.xpath import xpath_is_valid, xpath_is_function_call
from ..utils import get_all_class_init_params, get_required_class_init_params


@dataclass
class Node:
    """
    A Node object is like a recipe that describes:

    1. What data to extract from which HTML tags.
    2. How to transform the extracted data.
    3. Where to place the scraped data, e.g. in a class, dict, or list.

    :param xpath:
        The xpath used to find e.g. a single tag, multiple tags, a tag-attribute value, etc.
    :param target:
        Specifies the class or dataclass to wrap the extracted data. Requires all objects in `nodes` to set their
        'key' parameter to a non-None value. If `target` is None but `nodes` is populated, the extracted data will
        be wrapped in a dict or list, depending on whether all instances in `nodes` set their `key` parameter.
    :param key:
        An optional key for the extracted data. Depending on the parent Node object's settings, a `key` will
        place the data in a dict or a class/dataclass.
    :param nodes:
        A list of child nodes (Node instances) for extracting multiple data points from tags matched against
        `full_path`. All Node instances in `nodes` should either set a 'key' value or none at all.
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
    :param add_descendant_axis_to_xpath:
         If True, then the scrape() function will add, depending on the node-level, './/' or '//' as a prefix to
         the xpath before executing the xpath query to the current tag.
         The default value of this parameter is True, out of convenience, given that in most cases we would write
         xpaths with './/' or '//' prefixes.
         This convenience is met with the default value of the 'filter' parameter to be 0
         (extract the first tag that was matched against the xpath).

         If :param: xpath already has '.' or '/' as a prefix, then :param: add_descendant_axis_to_xpath
         will be set to False in the __post_init__ method.
    """

    xpath: str = ''
    key: str | None = None
    target: Type[Any] | None = None
    extract: Ex | str = Ex.FULL_TEXT
    filter: int | list[int] | Range | None = 0
    transform: Callable[[Any], Any] = lambda x: x
    nodes: list[Node] = field(default_factory=list)
    add_descendant_axis_to_xpath: bool = field(default=True)

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

    @property
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

    @property
    def target_class_name(self) -> str | None:
        return self.target.__name__ if self.target else None

    def _check_xpath(self) -> None:
        if self.no_xpath:
            return
        if not xpath_is_valid(self.xpath):
            raise InvalidXpathException(self.xpath)
        if (
            self.xpath.startswith('.')
            or self.xpath.startswith('/')
            or xpath_is_function_call(self.xpath)
        ):
            self.add_descendant_axis_to_xpath = False

    def __post_init__(self) -> None:
        self._check_xpath()

        if not (
            all([c.key is not None for c in self.nodes])
            or all([c.key is None for c in self.nodes])
        ):
            """
            Asserts that either all (or none) of the Node instances in :param nodes set the 'key' param.
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

        if not self.keys_in_nodes.issubset(get_all_class_init_params(self.target)):
            """
            Make sure that all keys provided in the instances of the 'nodes'
            param are valid init params for the target class.
            """
            raise InvalidKeysForTargetException(self)

        if not (get_required_class_init_params(self.target) - {'_tag'}).issubset(
            self.keys_in_nodes
        ):
            """
            Make sure that the instances in the 'nodes' param cover all mandatory
            initialization parameters of the target class.
            """
            raise MissingTargetKeysException(self)


class InvalidXpathException(Exception):
    def __init__(self, xpath: str):
        message: str = (
            f'\n{xpath} seems to be an invalid xpath. '
            f'\nFeel free to use ChatGPT to check if your path is compatible with the XPath 1.0 syntax.'
            f'\nNote that xpath queries using XPath syntax of any version higher than 1.0 are not supported.'
        )
        super().__init__(message)


class PartialKeysException(Exception):
    def __init__(self, node: Node):
        message: str = (
            f"\n\nSome Node instances in your nodes list have a key attribute set while others don't."
            f'\nYou can either provide a list of nodes where ALL instances set a key, or NO instances do.'
        )
        super().__init__(message)


class InvalidTargetTypeException(Exception):
    def __init__(self, node: Node):
        message: str = (
            f"\n\nThe type of your target '{node.target_class_name}' is not a custom class nor a dataclass."
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
    def __init__(self, node: Node):
        invalid_keys: set[str] = {
            key
            for key in node.keys_in_nodes
            if key not in get_all_class_init_params(node.target)
        }
        message: str = (
            f'A Node instance in your nodes list defines a key that is no valid init '
            f'parameter for your target {node.target_class_name}: {invalid_keys.pop()}'
        )
        super().__init__(message)


class MissingTargetKeysException(Exception):
    def __init__(self, node: Node):
        missing_keys: list[str] = sorted(
            list((get_required_class_init_params(node.target) - node.keys_in_nodes))
        )
        message: str = f"\n\nMissing keys in nodes list for target '{node.target_class_name}': {missing_keys}"
        super().__init__(message)


__all__ = [
    'Node',
    'InvalidXpathException',
    'PartialKeysException',
    'MissingTargetKeysException',
    'InvalidTargetTypeException',
    'InvalidKeysForTargetException',
]
