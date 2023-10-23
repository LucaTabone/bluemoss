from dataclasses import dataclass, field


@dataclass(frozen=True)
class Range:
    start_idx: int
    end_idx: int | None = None
    reverse: bool = field(default=False)

    def __post_init__(self):
        if isinstance(self.end_idx, int):
            if self.end_idx == self.start_idx:
                raise EqualIndicesException(self.start_idx)

    def filter(self, li: list) -> list:
        if self.end_idx is None:
            res = li[self.start_idx:]
        else:
            res = li[self.start_idx:self.end_idx]
        return res[::-1] if self.reverse else res


class EqualIndicesException(Exception):
    def __init__(self, index: int):
        message: str = (
            f"\n\nYou have defined a Range instance with start_idx={index} and end_idx={index}."
            f"\nMake sure to provide unequal values for your 'start_idx' and 'end_idx' parameters."
            f"\n\nPro Tips:"
            f"\n1) You can define a Range instance with just one value, "
            f"e.g. Range(2) which will filter all matched html-tags from index 2 onwards."
            f"\n2) An instance like Range(0, 2) will filter for the first two matched html-tags."
        )
        super().__init__(message)


__all__ = [
    "Range",
    "EqualIndicesException"
]
