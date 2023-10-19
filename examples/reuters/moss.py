from examples.reuters.classes import Article
from bluemoss import Ex, Root, Node, extract


REUTERS_WORLD_NEWS_ARTICLES_MOSS: Root = Root(
    filter=None,
    path="li[contains(@class, 'story-collection')]/div[contains(@class, 'media-story-card')]",
    target=Article,
    nodes=[
        Node(
            path="a",
            key="url",
            extract=Ex.HREF_ENDPOINT,
            transform=lambda endpoint: f"https://reuters.com{endpoint}"
        ),
        Node(key="date", path="time"),
        Node(key="title", path="h3/a"),
        Node(key="img_url", path="img", extract="src"),
        Node(key="topic", path="span/a", extract=Ex.TEXT)
    ]
)


if __name__ == '__main__':
    with open("./static/news.html", "r") as f:
        for article in extract(REUTERS_WORLD_NEWS_ARTICLES_MOSS, f.read()):
            print(article)
