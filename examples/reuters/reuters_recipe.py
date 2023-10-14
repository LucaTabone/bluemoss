from src.typings import Extract
from src.classes.recipe import Recipe
from src.extract import extract
from src.classes.range import Range
from examples.reuters.reuters_classes import Article


REUTERS_WORLD_NEWS_ARTICLES_RECIPE: Recipe = Recipe(
    path_prefix="//",
    path="li[contains(@class, 'story-collection')]/div[contains(@class, 'media-story-card')]",
    range=Range(0, None),
    target=Article,
    children=[
        Recipe(
            path="a",
            context="url",
            extract=Extract.HREF_ENDPOINT,
            transform=lambda endpoint: f"https://reuters.com{endpoint}"
        ),
        Recipe(context="date", path="time"),
        Recipe(context="title", path="h3/a"),
        Recipe(context="img_url", path="img", extract="src"),
        Recipe(context="topic", path="span/a", extract=Extract.TEXT)
    ]
)


with open("./static/news.html", "r") as f:
    for article in extract(REUTERS_WORLD_NEWS_ARTICLES_RECIPE, f.read()):
        print(article)
