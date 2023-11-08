from constants import HTML
from src.bluemoss import Node, scrape


nodes: list[Node] = [
    Node('p') ,
    Node('li//p'),
    Node('div/p'),
    Node('div//p'),
    Node('div[contains(@class, "location_")]'),
    Node('body//div[contains(@class, "location_")]')
]

for node in nodes:
    assert scrape(node, HTML) == 'Cupertino, California'
