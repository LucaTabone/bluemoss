from src.bluemoss import Node, scrape
from ..constants import README_EXAMPLE_HTML as HTML


node = Node(
    'li',
    filter=None,
    key='companies',
    nodes=[
        Node('a', key='name'),
        Node('p', key='headquarters'),
        Node('a/@href', key='id', transform=lambda href: href.split('=')[1]),
    ],
)


def test():
    assert scrape(node, HTML) == {
        'companies': [
            {'id': 'apple', 'name': 'Apple', 'headquarters': 'Cupertino'},
            {'id': 'google', 'name': 'Google', 'headquarters': 'Mountain View'},
            {'id': 'tesla', 'name': 'Tesla', 'headquarters': 'Austin'},
            {
                'id': 'deepmind',
                'name': 'DeepMind',
                'headquarters': 'London',
            },
        ]
    }
