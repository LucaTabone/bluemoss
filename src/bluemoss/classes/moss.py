from __future__ import annotations
import builtins
from .extract import Ex
from .range import Range
from inspect import isclass
from .utils import Class
from functools import cached_property
from dataclasses import dataclass, field
from ..utils import is_valid_xpath, get_all_class_init_params, get_required_class_init_params


@dataclass(frozen=True)
class BlueMoss:
    """
    A BlueMoss object is a recipe that describes
        1.) what data to extract from which tags
        2.) how to further transform the extracted data
        3.) where to place the transformed data, e.g. in a class, dataclass, dict or list

    :param xpath:
        The xpath used to find e.g. a single tag, multiple tags, a tag-attribute value etc.
    :param xpath_prefix:
        An optional prefix to prepend to :param xpath, e.g. '/', '//', './' or './/'
        This is useful because we can now define a subclass of BlueMoss, as done below with the classes
        'Root' and 'Node', which have widely used xpath prefixes like .// for Root and // for Node.
        This simply provides a bit more ease when creating BlueMoss objects,
        as you do not have to always manually prefix every :param xpath with .// or // etc.
    :param target:
        Defines the class/dataclass in which to wrap the extracted data.
        This requires all objects in :param nodes to set their 'key' parameter to a non-None value.

        If :param target is None while :param nodes is not empty, then the extracted data will be placed
        either into a dict or list: If all instances in :param node set their key parameter,
        then the data will be placed into a dict, otherwise into a list.
    :param key:
        An optional key to provide the extracted data with. Setting a value for 'key' will place the extracted data
        either in a dict (no target in the parent BlueMoss object defined) or into a class/dataclass (requires
        a target to be defined in the parent BlueMoss object).
    :param nodes:
        A list of child-nodes (BlueMoss instances) which enable us to extract multiple data-points from the tag(s)
        that were matched against self.full_path.

        Note that providing a 'nodes' list with BlueMoss instances where some set a 'key' value
        and some not, will yield an Exception in the __post_init__ method. The BlueMoss instances in the nodes list
        either all set a 'key' value, or none of them do.
    :param extract:
        A string or an Ex enum-value to specify what data we want to extract from a html-tag.
        If isinstance(extract, str) then we will attempt to extract the attribute-value for the html-tag-attribute
        defined by :param extract from the currently matched html-tag.
    :param transform:
         A callable that enables us to further process the data we extracted.
    :param filter:
        The :param filter enables us to filter for specific tags that we were able to match against self.full_path.
        This parameter can have 4 different types:
            1) int:
                Among all html-tags that we could match against self.full_path, an int value for :param filter
                reflects the index of the html-tag that we are interested in.
                The default value for :param filter is an int with value 0 which translates to the
                default behaviour, that we extract the first matched html-tag.
            2) list[int]:
                A list if ints reflecting the indices of the matched html-tags that we are interested in.
                E.g. if we have matched the following tags [tag_1, tag_2, tag_3] and :param filter is [2, 0, 5, 2],
                then we will transform our matched tags to the list [tag_3, tag_1, None, tag_3]
                before extracting data from them.
            3) Range:
                A Range object is a simple way to filter for a subset of subsequent html-tags among the matched tags.
                Let's consider our example from above where we have matched the tags [tag_1, tag_2, tag_3]
                against self.full_path.

                3.1) Range(1) would filter for all matched tags from index 1 and onwards: [tag_2, tag_3]
                3.2) Range(0, 2) would filter for the matched tags at index 0 and 1: [tag_1, tag_2].
                     In our example Range(0, 2) would yield the same result as Range(0, -1) similar to how
                     the python range specifier [0:2] would yield the same result as [0:-1].
                3.3) Range(1, reverse=True) would filter for the same tags as in 3.1,
                     but would return them in reverse order: [tag_3, tag_2].
            4) None:
                If we set :param filter to None, then we will apply no filter onto the matched tags.
                Use this setting when want to extract data from all the matched tags.
    """

    xpath: str = ""
    xpath_prefix: str = ""
    key: str | None = None
    target: Class | None = None
    extract: Ex | str = Ex.FULL_TEXT
    transform: callable = lambda x: x
    filter: int | list[int] | Range | None = 0
    nodes: list[Node] = field(default_factory=list)

    @property
    def no_xpath(self) -> bool:
        """
        :rtype: bool
        :return: True if no xpath was provided, False otherwise.
        """
        return self.xpath == ""

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
        return f"{self.xpath_prefix}{self.xpath}"

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

    def __post_init__(self):
        if not (self.no_xpath or is_valid_xpath(self.full_xpath)):
            """ Check the provided xpath for syntactical correctness. """
            raise InvalidXpathException(self)

        if not (
            all([c.key is not None for c in self.nodes]) or
            all([c.key is None for c in self.nodes])
        ):
            """
            Asserts that either all (or none) of the BlueMoss instances in :param nodes set the 'key' param.
            - In case none of the instances set a key value, the target object will be a list.
            - I case all of the instances set a value for the 'key' param , then the target is either a dict 
              or a class/dataclass, depending on whether the parent node has set a value for the 'target' param.
              If it hasn't, then the target is a dict.
            """
            raise PartialKeysException()
            
        if self.target is None:
            """ Early return in case no target was provided. """
            return

        if not isclass(self.target) or self.target.__name__ in dir(builtins):
            """ Make sure the value of the 'target' param references a class, which is not a builtin class. """
            raise InvalidTargetTypeException(self)

        if not self.keys_in_nodes.issubset(get_all_class_init_params(self.target)):
            """
            Make sure that all keys provided in the instances of the 'nodes' 
            param are valid init params for the target class.
            """
            raise InvalidKeysForTargetException(self)

        if not get_required_class_init_params(self.target).issubset(self.keys_in_nodes):
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
    xpath_prefix: str = field(default="//", init=False)


@dataclass(frozen=True)
class Node(BlueMoss):
    """
    BlueMoss subclass which comes with :param xpath_prefix set to './/'.
    This class is suited to be used as a child node in a BlueMoss tree as the preceding '.' char
    tells us to match :param full_path against the tag(s) matched in the parent node.
    """
    xpath_prefix: str = field(default=".//", init=False)


class InvalidXpathException(Exception):
    def __init__(self, moss: BlueMoss):
        message: str = (
            f"\n{moss.full_xpath} seems to be an invalid xpath. "
            f"\nFeel free to use ChatGPT to check if your path is compatible with the XPath 1.0 syntax."
            f"\nNote that xpath queries using XPath syntax of any version higher than 1.0 are not supported."
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
            f"\n\nThe type of your target '{moss.target.__name__}' is not a custom class nor a dataclass."
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
        invalid_keys: set[str] = {
            key for key in moss.keys_in_nodes
            if key not in get_all_class_init_params(moss.target)
        }
        message: str = (
            f"A Node instance in your nodes list defines a key that is no valid init "
            f"parameter for your target {moss.target.__name__}: {invalid_keys.pop()}"
        )
        super().__init__(message)


class MissingTargetKeysException(Exception):
    def __init__(self, moss: BlueMoss):
        missing_keys: list[str] = sorted(list((get_required_class_init_params(moss.target) - moss.keys_in_nodes)))
        message: str = (
            f"\n\nMissing keys in nodes list for target '{moss.target.__name__}': {missing_keys}"
        )
        super().__init__(message)


__all__ = [
    "BlueMoss",
    "Root",
    "Node",
    "InvalidXpathException",
    "PartialKeysException",
    "MissingTargetKeysException",
    "InvalidTargetTypeException",
    "InvalidKeysForTargetException"
]
