from examples.blog.classes import BlogPost
from bluemoss import BlueMoss, Root, Node, Range, extract


BLOG_POSTS_MOSS: BlueMoss = Root(
    filter=None,
    target=BlogPost,
    path="div[@class='post']",
    nodes=[
        Node("a", key="title"),
        Node("a/@href", key="url"),
        Node("span[@class='date']", key="date"),
        Node("p[not(@*)] | .//li[not(@*)]", key="_text_lines", filter=None)
    ]
)


if __name__ == '__main__':
    with open("./static/blog.html", "r") as f:
        for article in extract(BLOG_POSTS_MOSS, f.read()):
            print(article)
