import pytest
from dataclasses import dataclass
from .constants import FOUR_DIVS_HTML
from src.bluemoss import Root, Node, Range, extract


html: str = FOUR_DIVS_HTML


def test_find_first():
    expected_output: str = "Hello 1"
    assert extract(Root("div"), html) == expected_output
    assert extract(Root("html//div"), html) == expected_output


def test_find_last():
    moss = Root("div", range=Range(-1, None))
    assert extract(moss, html) == "Hello 4"


def test_find_range():
    # first two
    moss = Root("div", range=Range(0, 2))
    assert extract(moss, html) == ["Hello 1", "Hello 2"]

    # middle two
    moss = Root("div",range=Range(1, -1))
    assert extract(moss, html) == ["Hello 2", "Hello 3"]


def test_find_range_reversed():
    # first two reversed
    moss = Root("div", range=Range(0, 2, reverse=True))
    assert extract(moss, html) == ["Hello 2", "Hello 1"]

    # middle two reversed
    moss = Root("div", range=Range(1, -1, reverse=True))
    assert extract(moss, html) == ["Hello 3", "Hello 2"]


def test_find_all():
    moss = Root("div", range=Range(0, None))
    assert extract(moss, html) == [f"Hello {i}" for i in range(1, 5)]


def test_find_all_reversed():
    moss = Root("div", range=Range(0, None, reverse=True))
    assert extract(moss, html) == [f"Hello {i}" for i in range(4, 0, -1)]


def test_find_range_with_dict_result():
    # first two
    moss = Root(
        path="html",
        nodes=[
            Node("div", key="1"),
            Node("div[2]", key="2")
        ]
    )
    assert extract(moss, html) == {"1": "Hello 1", "2": "Hello 2"}

    # middle two
    li: list[Root] = [
        Root(
            "html",
            nodes=[
                Node("div", key="1", range=Range(1, 2)),
                Node("div", key="2", range=Range(2, 3))
            ]
        ),
        Root(
            "html",
            nodes=[
                Node("div[2]", key="1"),
                Node("div[3]", key="2")
            ]
        )
    ]
    for moss in li:
        assert extract(moss, html) == {"1": "Hello 2", "2": "Hello 3"}


def test_find_range_with_class_result():
    @dataclass
    class MyClass:
        a: str
        b: str

        def __eq__(self, other) -> bool:
            return self.a == other.a and self.b == other.b

    # first two
    moss = Root(
        "html",
        target=MyClass,
        nodes=[
            Node("div", key="a"),
            Node("div[2]", key="b")
        ]
    )
    assert extract(moss, html) == MyClass(a="Hello 1", b="Hello 2")

    # middle two
    li: list[Root] = [
        Root(
            "html",
            target=MyClass,
            nodes=[
                Node("div", key="a", range=Range(1, 2)),
                Node("div", key="b", range=Range(2, 3))
            ]
        ),
        Root(
            "html",
            target=MyClass,
            nodes=[
                Node("div[2]", key="a"),
                Node("div[3]", key="b")
            ]
        )
    ]
    for moss in li:
        assert extract(moss, html) == MyClass(a="Hello 2", b="Hello 3")


def test_bad_indexing():
    # 1) find many
    moss = Root("div", range=Range(5, None))
    assert extract(moss, html) == []

    # 2) find single & valid (but out of bound) indexing for Range object
    moss = Root("div", range=Range(5, 6))
    assert extract(moss, html) is None

    # 3) find single & valid indexing for Range object
    moss = Root("div", range=Range(3, -1))
    assert extract(moss, html) == []

    # 4) invalid indexing for Range object
    with pytest.raises(AssertionError):
        Root("div", range=Range(5, 5))
