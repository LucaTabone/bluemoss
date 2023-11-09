from src.bluemoss import Node, Range, scrape
from ..constants import README_EXAMPLE_HTML as HTML


node = Node('a', filter=3)
assert scrape(node, HTML) == 'DeepMind'

node = Node('a', filter=[0, 2])
assert scrape(node, HTML) == ['Apple', 'Tesla']

node = Node('a', filter=Range(2))
assert scrape(node, HTML) == ['Tesla', 'DeepMind']

node = Node('a', filter=Range(2, 4))
assert scrape(node, HTML) == ['Tesla', 'DeepMind']

node = Node('a', filter=Range(2, 3))
assert scrape(node, HTML) == ['Tesla']

node = Node('a', filter=None)
assert scrape(node, HTML) == ['Apple', 'Google', 'Tesla', 'DeepMind']
