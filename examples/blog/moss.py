from bluemoss import Root, Range, extract
from examples.blog.classes import BlogPost


BLOG_POSTS_MOSS: Root = Root(
    path_prefix="/html",
    path="//div[@class='post']",
    range=Range(0, None),
    target=BlogPost,
    children=[
        Root(key="title", path="a"),
        Root(key="url", path="a[@href]"),
        Root(key="date", path="span[@class='date']"),
        Root(
            path_prefix="",
            range=Range(0, None),
            key="_text_lines",
            path=".//p[not(@*)] | .//li[not(@*)]"
        )
    ]
)


if __name__ == '__main__':
    with open("./static/blog.html", "r") as f:
        for article in extract(BLOG_POSTS_MOSS, f.read()):
            print(article)
