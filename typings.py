import abc
from json import dumps
from enum import Enum, unique
from datetime import datetime
from collections import OrderedDict
from functools import cached_property
from dataclasses import dataclass, field
from utils import datetime_to_sql_timestamp
from typing import Protocol, Callable, TypeVar


class _DataClassProtocol(Protocol):
    """ A generic type to use as a type-hint for dataclasses. """
    __dict__: dict
    __call__: Callable
    __annotations__: dict


DataClass = TypeVar("DataClass", bound=_DataClassProtocol)


@unique
class Extract:
    TAG = "tag"
    TEXT = "text"
    HREF = "href"
    HREF_TLD = "href_tld"
    HREF_DOMAIN = "href_domain"
    HREF_ENDPOINT = "href_endpoint"
    HREF_ENDPOINT_NO_QUERY = "href_endpoint_no_query"


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
    __dataclass_fields__: dict | None = field(default=None)

    def __str__(self) -> str:
        return self.json

    @cached_property
    def json(self) -> str:
        return dumps(self.dict, indent=4)

    @property
    def dict(self) -> OrderedDict:
        d: dict = self.clean_dict(self.__dict__)
        return OrderedDict([
            (key, self.dictify(d[key]))
            for key in self.__dataclass_fields__ if key in d
        ])

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
            return self.clean_dict(val)
        if hasattr(val, "__dict__"):
            return self.clean_dict(dict(val))
        return val

    @classmethod
    def clean_dict(
            cls,
            d: dict,
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
