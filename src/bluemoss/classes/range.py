from dataclasses import dataclass, field


@dataclass(frozen=True)
class Range:
    start_idx: int
    end_idx: int | None = field(default=None)
    reverse: bool = field(default=False)

    def __post_init__(self):
        assert self.end_idx is None or abs(self.end_idx - self.start_idx) >= 1

    @property
    def find_single(self) -> bool:
        return (
                self.start_idx == -1 and self.end_idx is None or
                self.end_idx is not None and abs(self.end_idx - self.start_idx) == 1
        )

    @property
    def find_range(self) -> bool:
        return not self.find_single

    @property
    def find_all(self) -> bool:
        return self.find_range and self.start_idx == 0 and self.end_idx is None
