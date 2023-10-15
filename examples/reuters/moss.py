from examples.reuters.classes import Article
from bluemoss import Extract, Moss, Range, extract


REUTERS_WORLD_NEWS_ARTICLES_MOSS: Moss = Moss(
    path_prefix="//",
    path="li[contains(@class, 'story-collection')]/div[contains(@class, 'media-story-card')]",
    range=Range(0, None),
    target=Article,
    children=[
        Moss(
            path="a",
            key="url",
            extract=Extract.HREF_ENDPOINT,
            transform=lambda endpoint: f"https://reuters.com{endpoint}"
        ),
        Moss(key="date", path="time"),
        Moss(key="title", path="h3/a"),
        Moss(key="img_url", path="img", extract="src"),
        Moss(key="topic", path="span/a", extract=Extract.TEXT)
    ]
)


if __name__ == '__main__':
    with open("./static/news.html", "r") as f:
        for article in extract(REUTERS_WORLD_NEWS_ARTICLES_MOSS, f.read()):
            print(article)
