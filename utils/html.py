from lxml import etree
from bs4 import BeautifulSoup


def is_valid_xpath(xpath_query: str):
    root = etree.Element("root")
    doc = etree.ElementTree(root)
    try:
        doc.xpath(xpath_query)
        return True
    except etree.XPathEvalError:
        return False


def etree_to_bs4(node: etree.Element) -> BeautifulSoup:
    return BeautifulSoup(etree_to_string(node), "html.parser")


def etree_to_string(node: etree.Element) -> str:
    return etree.tostring(node, method="html").decode("utf-8")
