from typing import TypeVar

""" A custom type to enable type-hinting a class/dataclass reference. """

Class = TypeVar("Class", bound=object)

__all__ = [
    "Class"
]
