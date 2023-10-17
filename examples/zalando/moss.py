from examples.zalando.classes import Article
from bluemoss import extract, Ex, Root, Range


ZALANDO_ARTICLES_MOSS: Root = Root(
    filter=None,
    target=Article,
    path_prefix="/html",
    path="//article[contains(@class, 'z5x6ht')]",
    nodes=[
        Root(key="brand", path="h3"),
        Root(key="img_url", path="img/@src"),
        Root(key="url", path="a", extract=Ex.HREF),
        Root(key="_price_text", path="p/span", filter=-1),
        Root(key="short_description", path="h3", filter=-1),
        Root(key="discount", path="span[contains(@class, 'Km7l2y r9BRio')]"),
        Root(
            key="is_deal",
            path="span[contains(@class, 'DJxzzA') and contains(text(), 'Deal')]",
            extract=Ex.FOUND
        ),
        Root(
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
