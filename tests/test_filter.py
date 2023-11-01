import pytest
from dataclasses import dataclass
from .constants import FOUR_DIVS_HTML as HTML
from src.bluemoss import Root, Node, Range, extract, EqualIndicesException


def test_find_first():
    expected_output: str = 'Hello 1'
    assert extract(Root('div'), HTML) == expected_output
    assert extract(Root('html//div'), HTML) == expected_output


def test_find_last():
    moss = Root('div', filter=-1)
    assert extract(moss, HTML) == 'Hello 4'


def test_find_range():
    # first two
    moss = Root('div', filter=Range(0, 2))
    assert extract(moss, HTML) == ['Hello 1', 'Hello 2']

    # middle two
    moss = Root('div', filter=Range(1, -1))
    assert extract(moss, HTML) == ['Hello 2', 'Hello 3']


def test_find_range_reversed():
    # first two reversed
    moss = Root('div', filter=Range(0, 2, reverse=True))
    assert extract(moss, HTML) == ['Hello 2', 'Hello 1']

    # middle two reversed
    moss = Root('div', filter=Range(1, -1, True))
    assert extract(moss, HTML) == ['Hello 3', 'Hello 2']


def test_find_all():
    moss = Root('div', filter=None)
    assert extract(moss, HTML) == [f'Hello {i}' for i in range(1, 5)]


def test_find_all_reversed():
    moss = Root('div', filter=Range(0, None, True))
    assert extract(moss, HTML) == [f'Hello {i}' for i in range(4, 0, -1)]


def test_find_with_list_of_ints():
    moss = Root('div', filter=[1, 2, 5, 1, 7])
    assert extract(moss, HTML) == ['Hello 2', 'Hello 3', None, 'Hello 2', None]


def test_find_range_with_dict_result():
    # first two
    moss = Root(
        xpath='html', nodes=[Node('div', key='1'), Node('div[2]', key='2')]
    )
    assert extract(moss, HTML) == {'1': 'Hello 1', '2': 'Hello 2'}

    # middle two
    li: list[Root] = [
        Root(
            'html',
            nodes=[
                Node('div', key='1', filter=1),
                Node('div', key='2', filter=2),  # Node("div[3]", key="2")
            ],
        ),
        Root('html', nodes=[Node('div[2]', key='1'), Node('div[3]', key='2')]),
    ]
    for moss in li:
        assert extract(moss, HTML) == {'1': 'Hello 2', '2': 'Hello 3'}


def test_find_range_with_class_result():
    @dataclass
    class MyClass:
        a: str
        b: str

        def __eq__(self, other) -> bool:
            return self.a == other.a and self.b == other.b

    # first two
    moss = Root(
        'html',
        target=MyClass,
        nodes=[Node('div', key='a'), Node('div[2]', key='b')],
    )
    assert extract(moss, HTML) == MyClass(a='Hello 1', b='Hello 2')

    # middle two
    li: list[Root] = [
        Root(
            'html',
            target=MyClass,
            nodes=[
                Node('div', key='a', filter=1),
                Node('div', key='b', filter=2),
            ],
        ),
        Root(
            'html',
            target=MyClass,
            nodes=[Node('div[2]', key='a'), Node('div[3]', key='b')],
        ),
    ]
    for moss in li:
        assert extract(moss, HTML) == MyClass(a='Hello 2', b='Hello 3')


def test_bad_indexing():
    # 1) find many
    moss = Root('div', filter=Range(5))
    assert extract(moss, HTML) == []

    # 2) find single & valid (but out of bound) indexing for Range object
    moss = Root('div', filter=5)
    assert extract(moss, HTML) is None

    # 3) find single & valid indexing for Range object
    moss = Root('div', filter=Range(3, -1))
    assert extract(moss, HTML) == []

    # 4) invalid indexing for Range object
    with pytest.raises(EqualIndicesException):
        Root('div', filter=Range(5, 5))
