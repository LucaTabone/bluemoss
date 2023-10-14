from src.typings import Dictable
from dataclasses import dataclass, field


@dataclass
class BlogPost(Dictable):
    url: str
    date: str
    title: str
    text: str | None = field(default=None, init=False)
    _text_lines: list[str]

    def __post_init__(self):
        self.text = "\n\n".join([line.strip() for line in self._text_lines if line.strip()])
