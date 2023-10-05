from __future__ import annotations
from lxml import etree
from bs4 import BeautifulSoup
from datetime import date, datetime
from dataclasses import fields, MISSING, Field


def is_valid_xpath(xpath_query: str):
    root = etree.Element("root")
    doc = etree.ElementTree(root)
    try:
        doc.xpath(xpath_query)
        return True
    except etree.XPathEvalError:
        return False


def datetime_to_sql_timestamp(dt: datetime) -> str:
    """ Transform a datetime object to a SQL timestamp. """
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def date_to_sql_date(d: date) -> str:
    """ Transform a datetime object to a SQL timestamp. """
    return d.strftime("%Y-%m-%d")


def update_params_with_defaults(dataclass_type, params: dict[str, any]) -> dict[str, any]:
    return {
        _field.name: params.get(_field.name) or _get_default_value(_field)
        for _field in fields(dataclass_type)
        if _field.name in params
    }


def etree_to_bs4(node: etree.Element) -> BeautifulSoup:
    return BeautifulSoup(_etree_to_string(node), "html.parser")


def _get_default_value(f: Field):
    if f.default != MISSING:
        return f.default
    if f.default_factory != MISSING:
        return f.default_factory()
    raise ValueError(f"The field '{f.name}' does not have a default value nor a default_factory.")


def _etree_to_string(node: etree.Element) -> str:
    return etree.tostring(node, method="html").decode("utf-8")
