from src.bluemoss import Node, scrape
from ..constants import README_EXAMPLE_HTML as HTML


nodes: list[Node] = [
    Node('p'),
    Node('li//p'),
    Node('div/p'),
    Node('div//p'),
    Node('div[contains(@class, "location_")]'),
    Node('body//div[contains(@class, "location_")]'),
]


def test():
    for node in nodes:
        assert scrape(node, HTML) == 'Cupertino'
