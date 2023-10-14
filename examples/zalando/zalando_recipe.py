from examples.zalando.zalando_classes import Article
from bluemoss import extract, Extract, Recipe, Range


ZALANDO_ARTICLES_RECIPE: Recipe = Recipe(
    target=Article,
    path_prefix="/html",
    path="//article[contains(@class, 'z5x6ht')]",
    range=Range(0, None),
    children=[
        Recipe(context="brand", path="h3"),
        Recipe(context="img_url", path="img/@src"),
        Recipe(context="url", path="a", extract=Extract.HREF),
        Recipe(context="_price_text", path="p/span", range=Range(-1, None)),
        Recipe(context="short_description", path="h3", range=Range(-1, None)),
        Recipe(context="discount", path="span[contains(@class, 'Km7l2y r9BRio')]"),
        Recipe(
            context="is_deal",
            path="span[contains(@class, 'DJxzzA') and contains(text(), 'Deal')]",
            extract=Extract.FOUND
        ),
        Recipe(
            context="is_sponsored",
            path="span[contains(@class, '_65i7kZ') and contains(text(), 'Sponsored')]",
            extract=Extract.FOUND
        )
    ]
)


with open("./static/shoes.html", "r") as f:
    for article in extract(ZALANDO_ARTICLES_RECIPE, f.read()):
        print(article)
