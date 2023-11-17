from bluemoss import scrape, Ex, Node
from examples.webshop.classes import Article


ARTICLES_NODE: Node = Node(
    filter=None,
    target=Article,
    xpath="article[contains(@class, 'z5x6ht')]",
    nodes=[
        Node(key='brand', xpath='h3'),
        Node(key='img_url', xpath='img/@src'),
        Node(key='url', xpath='a', extract=Ex.HREF),
        Node(key='_price_text', xpath='p/span', filter=-1),
        Node(key='short_description', xpath='h3', filter=-1),
        Node(key='discount', xpath="span[contains(@class, 'Km7l2y r9BRio')]"),
        Node(
            key='is_deal',
            extract=Ex.BS4_TAG,
            transform=lambda tag: tag is not None,
            xpath="span[contains(@class, 'DJxzzA') and contains(text(), 'Deal')]",
        ),
        Node(
            key='is_sponsored',
            extract=Ex.BS4_TAG,
            transform=lambda tag: tag is not None,
            xpath="span[contains(@class, '_65i7kZ') and contains(text(), 'Sponsored')]",
        ),
    ],
)


if __name__ == '__main__':
    with open('static/webshop.html', 'r') as f:
        for article in scrape(ARTICLES_NODE, f.read()):
            print(article)
