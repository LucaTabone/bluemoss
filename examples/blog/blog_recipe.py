from bluemoss import Recipe, Range, extract
from examples.blog.blog_classes import BlogPost


BLOG_POSTS_RECIPE: Recipe = Recipe(
    path_prefix="/html",
    path="//div[@class='post']",
    range=Range(0, None),
    target=BlogPost,
    children=[
        Recipe(context="title", path="a"),
        Recipe(context="url", path="a[@href]"),
        Recipe(context="date", path="span[@class='date']"),
        Recipe(
            path_prefix="",
            range=Range(0, None),
            context="_text_lines",
            path=".//p[not(@*)] | .//li[not(@*)]"
        )
    ]
)


with open("./static/blog.html", "r") as f:
    for article in extract(BLOG_POSTS_RECIPE, f.read()):
        print(article)
