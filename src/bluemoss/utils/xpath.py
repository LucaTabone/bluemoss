import re
from lxml import etree
from functools import cache


@cache
def xpath_is_function_call(xpath: str) -> bool:
    return re.match(r'\w+(-[\w]+)?\(', xpath) is not None


@cache
def xpath_is_valid(xpath_query: str) -> bool:
    """
    Checks if the given @param xpath_query is a valid XPath expression.
    :rtype: bool
    :return: True if @param xpath_query is a valid XPath expression, False otherwise.
    """
    root = etree.Element('root')
    doc = etree.ElementTree(root)
    try:
        doc.xpath(xpath_query)
        return True
    except etree.XPathEvalError:
        return False


__all__ = ['xpath_is_function_call', 'xpath_is_valid']
