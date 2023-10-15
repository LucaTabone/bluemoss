import os
import sys
import pytest
from dataclasses import dataclass
from .constants import FOUR_DIVS_HTML

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from bluemoss import Moss, Range, extract


def test_find_first():
    expected_output: str = "Hello 1"
    li: list[Moss] = [
        Moss(
            path="//div",
            path_prefix=""
        ),
        Moss(
            path="div",
            path_prefix="//",
        ),
        Moss(
            path="//div",
            path_prefix="//body"
        ),
        Moss(
            path="//div",
            path_prefix="/html",
        ),
        Moss(
            path="/html//div",
            path_prefix=""
        )
    ]
    for moss in li:
        assert moss.range == Range(0, 1)
        assert extract(moss, FOUR_DIVS_HTML) == expected_output


def test_find_last():
    expected_output: str = "Hello 4"
    li: list[Moss] = [
        Moss(
            path="div",
            path_prefix="//",
            range=Range(-1, None)
        ),
        Moss(
            path="//div",
            path_prefix="",
            range=Range(-1, None)
        )
    ]
    for moss in li:
        assert extract(moss, FOUR_DIVS_HTML) == expected_output


def test_find_range():
    # first two
    expected_output_1: list[str] = ["Hello 1", "Hello 2"]
    moss = Moss(
        path="div",
        path_prefix="//",
        range=Range(0, 2)
    )
    assert extract(moss, FOUR_DIVS_HTML) == expected_output_1

    # middle two
    expected_output_2: list[str] = ["Hello 2", "Hello 3"]
    moss = Moss(
        path="div",
        path_prefix="//",
        range=Range(1, -1)
    )
    assert extract(moss, FOUR_DIVS_HTML) == expected_output_2


def test_find_range_reversed():
    # first two reversed
    expected_output_1: list[str] = ["Hello 2", "Hello 1"]
    moss = Moss(
        path="div",
        path_prefix="//",
        range=Range(0, 2, reverse=True)
    )
    assert extract(moss, FOUR_DIVS_HTML) == expected_output_1

    # middle two reversed
    expected_output_2: list[str] = ["Hello 3", "Hello 2"]
    moss = Moss(
        path="div",
        path_prefix="//",
        range=Range(1, -1, reverse=True)
    )
    assert extract(moss, FOUR_DIVS_HTML) == expected_output_2


def test_find_all():
    moss = Moss(
        path="div",
        path_prefix="//",
        range=Range(0, None)
    )
    assert extract(moss, FOUR_DIVS_HTML) == [f"Hello {i}" for i in range(1, 5)]


def test_find_all_reversed():
    moss = Moss(
        path="div",
        path_prefix="//",
        range=Range(0, None, reverse=True)
    )
    assert extract(moss, FOUR_DIVS_HTML) == [f"Hello {i}" for i in range(4, 0, -1)]


def test_find_range_with_dict_result():
    # first two
    moss = Moss(
        path_prefix="/html",
        children=[
            Moss(key="1", path="div"),
            Moss(key="2", path="div[2]")
        ]
    )
    assert extract(moss, FOUR_DIVS_HTML) == {"1": "Hello 1", "2": "Hello 2"}

    # middle two
    li: list[Moss] = [
        Moss(
            path_prefix="/html",
            children=[
                Moss(key="1", path="div", range=Range(1, 2)),
                Moss(key="2", path="div", range=Range(2, 3))
            ]
        ),
        Moss(
            path_prefix="/html",
            children=[
                Moss(key="1", path="div[2]"),
                Moss(key="2", path="div[3]")
            ]
        )
    ]
    for moss in li:
        assert extract(moss, FOUR_DIVS_HTML) == {"1": "Hello 2", "2": "Hello 3"}


def test_find_range_with_class_result():
    @dataclass
    class MyClass:
        a: str
        b: str

        def __eq__(self, other) -> bool:
            return self.a == other.a and self.b == other.b

    # first two
    moss = Moss(
        target=MyClass,
        path_prefix="/html",
        children=[
            Moss(key="a", path="div"),
            Moss(key="b", path="div[2]")
        ]
    )
    assert extract(moss, FOUR_DIVS_HTML) == MyClass(a="Hello 1", b="Hello 2")

    # middle two
    li: list[Moss] = [
        Moss(
            target=MyClass,
            path_prefix="/html",
            children=[
                Moss(key="a", path="div", range=Range(1, 2)),
                Moss(key="b", path="div", range=Range(2, 3))
            ]
        ),
        Moss(
            target=MyClass,
            path_prefix="/html",
            children=[
                Moss(key="a", path="div[2]"),
                Moss(key="b", path="div[3]")
            ]
        )
    ]
    for moss in li:
        assert extract(moss, FOUR_DIVS_HTML) == MyClass(a="Hello 2", b="Hello 3")


# TODO test bad indices
