from examples.reuters.classes import Article
from bluemoss import Ex, Root, Node, extract


REUTERS_WORLD_NEWS_ARTICLES_MOSS: Root = Root(
    filter=None,
    xpath="li[contains(@class, 'story-collection')]/div[contains(@class, 'media-story-card')]",
    target=Article,
    nodes=[
        Node(
            xpath="a",
            key="url",
            extract=Ex.HREF_ENDPOINT,
            transform=lambda endpoint: f"https://reuters.com{endpoint}"
        ),
        Node(key="date", xpath="time"),
        Node(key="title", xpath="h3/a"),
        Node(key="img_url", xpath="img", extract="src"),
        Node(key="topic", xpath="span/a", extract=Ex.TEXT)
    ]
)


if __name__ == '__main__':
    with open("./static/news.html", "r") as f:
        for article in extract(REUTERS_WORLD_NEWS_ARTICLES_MOSS, f.read()):
            print(article)
