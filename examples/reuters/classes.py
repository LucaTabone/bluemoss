from bluemoss import Jsonify
from dataclasses import dataclass


@dataclass
class Article(Jsonify):
    url: str
    date: str
    title: str
    topic: str
    img_url: str
