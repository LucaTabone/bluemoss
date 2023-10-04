import abc
from enum import Enum
from json import dumps
from lxml import etree
from datetime import date, datetime
from collections import OrderedDict
from functools import cached_property
from typing import Protocol, Callable, TypeVar
from dataclasses import dataclass, fields, MISSING


class _DataClassProtocol(Protocol):
    """ A generic type to use as a type-hint for dataclasses. """
    __dict__: dict
    __call__: Callable
    __annotations__: dict


DataClass = TypeVar("DataClass", bound=_DataClassProtocol)


@dataclass
class Dictable(abc.ABC):
    """
    An abstract dataclass to provide a .dict and a .json property, in order to turn any dataclass
    instance into a python dict or json object, while
        1. considering the order of parameters as they are defined within each dataclass that inherits from Dictable.
        2. dropping all protected parameters (those which begin with an underscore).

    Consider a dataclass instance p of type Profile(header: Header, pages: list[list[[Page]])
    while Profile, Header and Page are all dataclasses which inherit from Dictable.
    If you now execute .dict on p, the method will not only dictify @param p.header,
    but also all Page instances within the nested list of lists of @param p.pages.
    """

    def __init__(self):
        self.__dataclass_fields__ = None

    def __post_init__(self):
        pass

    def __str__(self) -> str:
        return self.json

    @cached_property
    def json(self) -> str:
        return dumps(self.dict, indent=4)

    @property
    def dict(self) -> OrderedDict:
        d: dict = clean_dict(self.__dict__)
        return OrderedDict([
            (key, self.dictify(d[key]))
            for key in self.__dataclass_fields__ if key in d
        ])

    @property
    def db_dict(self) -> OrderedDict:
        """
        Transform the dict property into a dictionary that can be
        used in a create/upsert operation with Prisma.
        """
        d: OrderedDict = self.dict
        for k in d.keys():
            if isinstance(d[k], dict):
                d[k] = dumps(d[k])
        return d

    def dictify(self, val: any) -> any:
        if isinstance(val, Enum):
            return val.value
        if isinstance(val, datetime):
            return datetime_to_sql_timestamp(val)
        if type(val) == list:
            return [_val.dict if hasattr(_val, "dict") else self.dictify(_val) for _val in val]
        if hasattr(val, "dict"):
            return val.dict
        if isinstance(val, dict):
            return clean_dict(val)
        if hasattr(val, "__dict__"):
            return clean_dict(dict(val))
        return val

    def custom_dict(self, keys: list[str]) -> OrderedDict:
        return OrderedDict({k: getattr(self, k) for k in keys})


def is_valid_xpath(xpath_query):
    root = etree.Element("root")
    doc = etree.ElementTree(root)
    try:
        doc.xpath(xpath_query)
        return True
    except etree.XPathEvalError:
        return False


def clean_dict(
    d: dict | None,
    ignore_protected: bool = True,
    remove_empty_values: bool = False,
    ignore_keys: set[str] | None = None
) -> OrderedDict:
    """
    @param d: The dictionary to be cleaned.
    @param remove_empty_values: Whether to remove emojis from the values in @param d.
    @param remove_empty_values: Whether to remove empty values from @param d, e.g. None, '' or [].
    @param ignore_keys: A set of keys which shall definitely be removed from the given dict @param d.
    @param ignore_protected: Whether to remove keys which start with a '_' character.
    @return: A clean version of the given dict @param d, where all keys within @param ignore_keys and all keys
             which reference empty or None-values are removed.
    """
    res = OrderedDict()
    for k, v in d.items():
        if not (
            (ignore_protected and type(k) == str and k.startswith("_")) or
            (remove_empty_values and v != 0 and not v) or
            (ignore_keys and k in ignore_keys)
        ):
            res[k] = v
    return res


def update_params_with_defaults(target: DataClass, params: dict[str, any]) -> dict[str, any]:
    """
    Update missing extracted fields with default values from the target dataclass.

    :param target: Target information dataclass for the scraping process
    :param params: Extracted parameters from the scraped HTML
    :return: Extracted paramaters updated with default values
    """

    def get_default_value(field) -> any:
        """
        Retrieve the default value for a given dataclass field if exists.

        :param field: Dataclass field for which we want to find a default value.
        :return: default value if exists else None
        """
        if field.default != MISSING:
            return field.default
        if field.default_factory != MISSING:
            return field.default_factory()

    return {
        field.name: params.get(field.name) or get_default_value(field)
        for field in fields(target)
        if field.name in params
    }


def datetime_to_sql_timestamp(dt: datetime) -> str:
    """ Transform a datetime object to a SQL timestamp. """
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def date_to_sql_date(d: date) -> str:
    """ Transform a datetime object to a SQL timestamp. """
    return d.strftime("%Y-%m-%d")
