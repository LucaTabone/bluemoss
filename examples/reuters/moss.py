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
            context="url",
            extract=Extract.HREF_ENDPOINT,
            transform=lambda endpoint: f"https://reuters.com{endpoint}"
        ),
        Moss(context="date", path="time"),
        Moss(context="title", path="h3/a"),
        Moss(context="img_url", path="img", extract="src"),
        Moss(context="topic", path="span/a", extract=Extract.TEXT)
    ]
)


with open("./static/news.html", "r") as f:
    for article in extract(REUTERS_WORLD_NEWS_ARTICLES_MOSS, f.read()):
        print(article)
