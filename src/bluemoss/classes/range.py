from __future__ import annotations
from lxml.html import HtmlElement
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Range:
    """
    A Range instance can be provided to the 'filter' parameter of a 'Node' instance.
    It basically tells the 'extract' function to filter out a sequence of subsequent html-tags
    that where matched against the 'xpath' parameter of the 'Node' instance.

    Example. Let's assume we have matched the following html-tags against our xpath: [tag_1, tag_2, tag_3]
        1) Range(1) would filter for all tags from index 1 and onwards: [tag_2, tag_3],
           i.e. Range(x) is equivalent to the list-filtering-notation [x:]
        2) Range(0, 2) would filter for the tags at index 0 and 1: [tag_1, tag_2],
           i.e. Range(x, y) is equivalent to the list-filtering-notation [x:y].
        3) Range(1, reverse=True) would filter for the same tags as in 3.1,
           but would return them in reverse order: [tag_3, tag_2],
           i.e. Range(x, reverse=True) is equivalent to the list-filtering-notation [x:][::-1].
        4) Range(1, 10, reverse=True) would yield [tag_3, tag_2], equivalent to the notation [x:y][::-1]
    """

    start_idx: int
    end_idx: int | None = None
    reverse: bool = field(default=False)

    def __post_init__(self) -> None:
        """If end_idx is not provided, assert that start_idx is not equal to end_idx."""
        if isinstance(self.end_idx, int):
            if self.end_idx == self.start_idx:
                raise EqualIndicesException(self.start_idx)

    def filter(self, li: list[HtmlElement]) -> list[HtmlElement]:
        """Method to filter a list of elements against the configuration of this Range instance."""
        if self.end_idx is None:
            res = li[self.start_idx :]
        else:
            res = li[self.start_idx : self.end_idx]
        return res[::-1] if self.reverse else res


class EqualIndicesException(Exception):
    def __init__(self, index: int):
        message: str = (
            f'\n\nYou have defined a Range instance with start_idx={index} and end_idx={index}.'
            f"\nMake sure to provide unequal values for your 'start_idx' and 'end_idx' parameters."
            f'\n\nPro Tips:'
            f'\n1) You can define a Range instance with just one value, '
            f'e.g. Range(2) which will filter all matched html-tags from index 2 onwards.'
            f'\n2) An instance like Range(0, 2) will filter for the first two matched html-tags.'
        )
        super().__init__(message)


__all__ = ['Range', 'EqualIndicesException']
