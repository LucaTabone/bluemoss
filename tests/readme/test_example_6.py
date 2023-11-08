from constants import HTML
from src.bluemoss import Node, scrape


node = Node(
    'li',
    filter=None,
    key='companies',
    nodes=[
        Node('a', key='name'),
        Node('p', key='headquarters'),
        Node(
            'a/@href',
            key='id',
            transform=lambda href: href.split("=")[1]
        )
    ]
)

assert scrape(node, HTML) == {
    'companies': [
        {
            'id': 'apple',
            'name': 'Apple',
            'headquarters': 'Cupertino, California'
        },
        {
            'id': 'google',
            'name': 'Google',
            'headquarters': 'Mountain View, California'
        },
        {
            'id': 'tesla',
            'name': 'Tesla',
            'headquarters': 'Austin, Texas'
        },
        {
            'id': 'deepmind',
            'name': 'DeepMind',
            'headquarters': 'London, United Kingdom'
        }
    ]
}
