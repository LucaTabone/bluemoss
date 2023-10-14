from bluemoss import Dictable
from dataclasses import dataclass


@dataclass
class Article(Dictable):
    url: str
    date: str
    title: str
    topic: str
    img_url: str
