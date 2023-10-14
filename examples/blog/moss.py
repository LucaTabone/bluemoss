from bluemoss import Moss, Range, extract
from examples.blog.classes import BlogPost


BLOG_POSTS_MOSS: Moss = Moss(
    path_prefix="/html",
    path="//div[@class='post']",
    range=Range(0, None),
    target=BlogPost,
    children=[
        Moss(context="title", path="a"),
        Moss(context="url", path="a[@href]"),
        Moss(context="date", path="span[@class='date']"),
        Moss(
            path_prefix="",
            range=Range(0, None),
            context="_text_lines",
            path=".//p[not(@*)] | .//li[not(@*)]"
        )
    ]
)


if __name__ == '__main__':
    with open("./static/blog.html", "r") as f:
        for article in extract(BLOG_POSTS_MOSS, f.read()):
            print(article)
