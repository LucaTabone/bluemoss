import abc
from json import dumps
from enum import Enum, unique
from datetime import datetime, date
from collections import OrderedDict
from dataclasses import dataclass, field


@unique
class Extract(Enum):
    # text
    TEXT = "text"

    # tag
    TAG = "tag"
    ETREE = "etree"
    TAG_AS_STRING = "tag_as_string"

    # href
    HREF = "href"
    HREF_QUERY = "href_query"
    HREF_DOMAIN = "href_domain"
    HREF_ENDPOINT = "href_endpoint"
    HREF_BASE_DOMAIN = "href_base_domain"
    HREF_ENDPOINT_WITH_QUERY = "href_endpoint_with_query"


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
        if type(val) == list:
            return [_val.dict if hasattr(_val, "dict") else self.dictify(_val) for _val in val]
        if isinstance(val, Dictable):
            return val.dict
        if isinstance(val, dict):
            return val
        if hasattr(val, "__dict__"):
            return val.__dict__
        return val


@dataclass
class DictableWithTag(Dictable):
    """
    Some dataclass instances may need access to their source-html-tag.
    Those dataclasses can inherit from DictableWithTag and thus also get the benefits of the Dictable class.
    """
    _tag: BeautifulSoup | Tag

    def __post_init__(self):
        super().__post_init__()

    @property
    def tag(self) -> BeautifulSoup | Tag:
        return self._tag

    @property
    def source_line(self) -> int:
        """ The line within the source-html-doc in which @param self._tag was found. """
        return self._tag.sourceline
