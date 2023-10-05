from lxml import etree
from _types import DataClass
from datetime import date, datetime
from dataclasses import fields, MISSING


def is_valid_xpath(xpath_query):
    root = etree.Element("root")
    doc = etree.ElementTree(root)
    try:
        doc.xpath(xpath_query)
        return True
    except etree.XPathEvalError:
        return False


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
