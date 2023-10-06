from __future__ import annotations
from lxml import etree
from bs4 import BeautifulSoup
from dataclasses import fields, MISSING, Field


def is_valid_xpath(xpath_query: str):
    root = etree.Element("root")
    doc = etree.ElementTree(root)
    try:
        doc.xpath(xpath_query)
        return True
    except etree.XPathEvalError:
        return False


def update_params_with_defaults(dataclass_type, params: dict[str, any]) -> dict[str, any]:
    return params | {
        _field.name: get_default_value(_field)
        for _field in fields(dataclass_type)
        if _field.name in params and params.get(_field.name, None) is None
    }


def get_default_value(field: Field) -> any:
    if field.default != MISSING:
        return field.default
    if field.default_factory != MISSING:
        return field.default_factory()
    raise None


def etree_to_bs4(node: etree.Element) -> BeautifulSoup:
    return BeautifulSoup(etree_to_string(node), "html.parser")


def etree_to_string(node: etree.Element) -> str:
    return etree.tostring(node, method="html").decode("utf-8")
