from bluemoss import Jsonify
from dataclasses import dataclass


@dataclass
class ArticlePreview(Jsonify):
    url: str
    date: str
    title: str
    topic: str
    img_url: str
