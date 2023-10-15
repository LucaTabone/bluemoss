from examples.zalando.classes import Article
from bluemoss import extract, Extract, Moss, Range


ZALANDO_ARTICLES_MOSS: Moss = Moss(
    target=Article,
    path_prefix="/html",
    path="//article[contains(@class, 'z5x6ht')]",
    range=Range(0, None),
    children=[
        Moss(key="brand", path="h3"),
        Moss(key="img_url", path="img/@src"),
        Moss(key="url", path="a", extract=Extract.HREF),
        Moss(key="_price_text", path="p/span", range=Range(-1, None)),
        Moss(key="short_description", path="h3", range=Range(-1, None)),
        Moss(key="discount", path="span[contains(@class, 'Km7l2y r9BRio')]"),
        Moss(
            key="is_deal",
            path="span[contains(@class, 'DJxzzA') and contains(text(), 'Deal')]",
            extract=Extract.FOUND
        ),
        Moss(
            key="is_sponsored",
            path="span[contains(@class, '_65i7kZ') and contains(text(), 'Sponsored')]",
            extract=Extract.FOUND
        )
    ]
)


if __name__ == '__main__':
    with open("./static/shoes.html", "r") as f:
        for article in extract(ZALANDO_ARTICLES_MOSS, f.read()):
            print(article)
