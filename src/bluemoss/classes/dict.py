import abc
from enum import Enum
from lxml import etree
from json import dumps
from bs4 import BeautifulSoup
from ..utils import lxml_etree_to_bs4
from dataclasses import dataclass
from datetime import datetime, date
from collections import OrderedDict


class PrettyDict(dict):
    def __str__(self) -> str:
        return '{\n' + ',\n'.join(f'    {repr(k)}: {repr(v)}' for k, v in self.items()) + '\n}'


@dataclass
class Jsonify(abc.ABC):
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

    @property
    def json(self) -> str:
        return dumps(self.dict, indent=4)

    @property
    def dict(self) -> OrderedDict:
        d: dict = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return OrderedDict([
            (key, self.dictify(d[key]))
            for key in self.__dataclass_fields__ if key in d
        ])

    def dictify(self, val: any) -> any:
        if isinstance(val, Enum):
            return val.value
        if isinstance(val, datetime):
            return val.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(val, date):
            return val.strftime("%Y-%m-%d")
        if isinstance(val, Jsonify):
            return val.dict
        if isinstance(val, list):
            return [self.dictify(v) for v in val]
        if isinstance(val, set):
            return {self.dictify(v) for v in val}
        if isinstance(val, OrderedDict):
            return OrderedDict([
                (self.dictify(k), self.dictify(v))
                for (k, v) in val.items()
            ])
        if isinstance(val, dict):
            return {self.dictify(k): self.dictify(v) for k, v in val.items()}
        if hasattr(val, "__dict__"):
            return val.__dict__
        return val


@dataclass
class JsonifyWithTag(Jsonify):
    """
    Some dataclass instances may need access to their source-html-tag.
    Those dataclasses can inherit from DictableWithTag and thus also get the benefits of the Dictable class.
    """
    _tag: etree._Element

    def __post_init__(self):
        super().__post_init__()

    @property
    def lxml_etree_tag(self) -> etree._Element:
        return self._tag

    @property
    def bs4_tag(self) -> BeautifulSoup:
        return lxml_etree_to_bs4(self._tag)

    @property
    def source_line(self) -> int:
        """ The line within the source-html-doc in which @param self._tag was found. """
        return self._tag.sourceline


__all__ = [
    "PrettyDict",
    "Jsonify",
    "JsonifyWithTag"
]
