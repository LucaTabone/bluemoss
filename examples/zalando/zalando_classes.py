from src.classes.types_ import Dictable
from dataclasses import dataclass


@dataclass
class Article(Dictable):
    url: str
    brand: str
    img_url: str
    discount: str
    is_deal: bool
    is_sponsored: bool
    short_description: str
    _price_text: str
