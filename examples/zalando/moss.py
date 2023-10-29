from examples.zalando.classes import Article
from bluemoss import extract, Ex, Root, Node


ZALANDO_ARTICLES_MOSS: Root = Root(
    filter=None,
    target=Article,
    xpath="article[contains(@class, 'z5x6ht')]",
    nodes=[
        Node(key="brand", xpath="h3"),
        Node(key="img_url", xpath="img/@src"),
        Node(key="url", xpath="a", extract=Ex.HREF),
        Node(key="_price_text", xpath="p/span", filter=-1),
        Node(key="short_description", xpath="h3", filter=-1),
        Node(key="discount", xpath="span[contains(@class, 'Km7l2y r9BRio')]"),
        Node(
            key="is_deal",
            extract=Ex.BS4_TAG,
            transform=lambda tag: tag is not None,
            xpath="span[contains(@class, 'DJxzzA') and contains(text(), 'Deal')]"
        ),
        Node(
            key="is_sponsored",
            extract=Ex.BS4_TAG,
            transform=lambda tag: tag is not None,
            xpath="span[contains(@class, '_65i7kZ') and contains(text(), 'Sponsored')]"
        )
    ]
)


if __name__ == '__main__':
    with open("./static/shoes.html", "r") as f:
        for article in extract(ZALANDO_ARTICLES_MOSS, f.read()):
            print(article)
