from dataclasses import dataclass, field


@dataclass(frozen=True)
class Range:
    start_idx: int
    end_idx: int | None = None
    reverse: bool = field(default=False)

    def __post_init__(self):
        if isinstance(self.end_idx, int):
            assert self.end_idx != self.start_idx  # TODO message to show that one should use an int instead

    def filter(self, li: list) -> list:
        if self.end_idx is None:
            res = li[self.start_idx:]
        else:
            res = li[self.start_idx:self.end_idx]
        return res[::-1] if self.reverse else res
