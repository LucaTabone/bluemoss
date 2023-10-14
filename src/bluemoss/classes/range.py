from dataclasses import dataclass, field


@dataclass(frozen=True)
class Range:
    start_idx: int
    end_idx: int | None = field(default=None)
    return_first: bool = field(default=False)
    reverse: bool = field(default=False)

    @property
    def find_all(self) -> bool:
        return self.start_idx == 0 and self.end_idx is None

    @property
    def find_single(self) -> bool:
        return (
                self.return_first or
                self.start_idx == -1 and self.end_idx is None or
                self.end_idx is not None and abs(self.end_idx - self.start_idx) == 1
        )

    @property
    def find_range(self) -> bool:
        return not self.find_single

    def __eq__(self, other):
        return self.start_idx == other.start_idx and self.end_idx == other.end_idx