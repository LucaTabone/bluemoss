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
        message = ""
        super().__init__(message)


__all__ = [
    "Range",
    "EqualIndicesException"
]
