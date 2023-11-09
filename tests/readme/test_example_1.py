from src.bluemoss import Node, scrape
from ..constants import README_EXAMPLE_HTML as HTML


nodes: list[Node] = [
    Node('a'),
    Node('div/a'),
    Node('div/a'),
    Node('body//a'),
    Node('body//div/a'),
    Node('a', filter=0)
]

for node in nodes:
    assert scrape(node, HTML) == 'Apple'
