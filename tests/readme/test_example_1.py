from constants import HTML
from src.bluemoss import Node, scrape


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
