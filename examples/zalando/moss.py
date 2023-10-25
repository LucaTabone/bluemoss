from examples.zalando.classes import Article
from bluemoss import extract, Ex, Root, Node


ZALANDO_ARTICLES_MOSS: Root = Root(
    filter=None,
    target=Article,
    path="article[contains(@class, 'z5x6ht')]",
    nodes=[
        Node(key="brand", path="h3"),
        Node(key="img_url", path="img/@src"),
        Node(key="url", path="a", extract=Ex.HREF),
        Node(key="_price_text", path="p/span", filter=-1),
        Node(key="short_description", path="h3", filter=-1),
        Node(key="discount", path="span[contains(@class, 'Km7l2y r9BRio')]"),
        Node(
            key="is_deal",
            path="span[contains(@class, 'DJxzzA') and contains(text(), 'Deal')]",
            extract=Ex.FOUND
        ),
        Node(
            key="is_sponsored",
            path="span[contains(@class, '_65i7kZ') and contains(text(), 'Sponsored')]",
            extract=Ex.FOUND
        )
    ]
)


if __name__ == '__main__':
    with open("./static/shoes.html", "r") as f:
        for article in extract(ZALANDO_ARTICLES_MOSS, f.read()):
            print(article)
