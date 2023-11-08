import pytest
from dataclasses import dataclass
from .constants import FOUR_DIVS_HTML as HTML
from src.bluemoss import Node, Range, scrape, EqualIndicesException


def test_find_first():
    expected_output: str = 'Hello 1'
    assert scrape(Node('div'), HTML) == expected_output
    assert scrape(Node('html//div'), HTML) == expected_output


def test_find_last():
    node = Node('div', filter=-1)
    assert scrape(node, HTML) == 'Hello 4'


def test_find_range():
    # first two
    node = Node('div', filter=Range(0, 2))
    assert scrape(node, HTML) == ['Hello 1', 'Hello 2']

    # middle two
    node = Node('div', filter=Range(1, -1))
    assert scrape(node, HTML) == ['Hello 2', 'Hello 3']


def test_find_range_reversed():
    # first two reversed
    node = Node('div', filter=Range(0, 2, reverse=True))
    assert scrape(node, HTML) == ['Hello 2', 'Hello 1']

    # middle two reversed
    node = Node('div', filter=Range(1, -1, True))
    assert scrape(node, HTML) == ['Hello 3', 'Hello 2']


def test_find_all():
    node = Node('div', filter=None)
    assert scrape(node, HTML) == [f'Hello {i}' for i in range(1, 5)]


def test_find_all_reversed():
    node = Node('div', filter=Range(0, None, True))
    assert scrape(node, HTML) == [f'Hello {i}' for i in range(4, 0, -1)]


def test_find_with_list_of_ints():
    node = Node('div', filter=[1, 2, 5, 1, 7])
    assert scrape(node, HTML) == ['Hello 2', 'Hello 3', None, 'Hello 2', None]


def test_find_with_list_of_ints_and_dict_target():
    node = Node('div', filter=[0, 1, 2, 5, 1, 7], nodes=[Node('h1', key='caption')])
    assert scrape(node, HTML) == [
        {'caption': 'Hello 1'},
        {'caption': None},
        {'caption': None},
        None,
        {'caption': None},
        None,
    ]


def test_find_range_with_dict_result():
    # first two
    node = Node(xpath='html', nodes=[Node('div', key='1'), Node('div[2]', key='2')])
    assert scrape(node, HTML) == {'1': 'Hello 1', '2': 'Hello 2'}

    # middle two
    li: list[Node] = [
        Node(
            'html',
            nodes=[
                Node('div', key='1', filter=1),
                Node('div', key='2', filter=2),  # Node("div[3]", key="2")
            ],
        ),
        Node('html', nodes=[Node('div[2]', key='1'), Node('div[3]', key='2')]),
    ]
    for node in li:
        assert scrape(node, HTML) == {'1': 'Hello 2', '2': 'Hello 3'}


def test_find_range_with_class_result():
    @dataclass
    class MyClass:
        a: str
        b: str

        def __eq__(self, other) -> bool:
            return self.a == other.a and self.b == other.b

    # first two
    node = Node(
        'html',
        target=MyClass,
        nodes=[Node('div', key='a'), Node('div[2]', key='b')],
    )
    assert scrape(node, HTML) == MyClass(a='Hello 1', b='Hello 2')

    # middle two
    li: list[Node] = [
        Node(
            'html',
            target=MyClass,
            nodes=[
                Node('div', key='a', filter=1),
                Node('div', key='b', filter=2),
            ],
        ),
        Node(
            'html',
            target=MyClass,
            nodes=[Node('div[2]', key='a'), Node('div[3]', key='b')],
        ),
    ]
    for node in li:
        assert scrape(node, HTML) == MyClass(a='Hello 2', b='Hello 3')


def test_bad_indexing():
    # 1) find many
    node = Node('div', filter=Range(5))
    assert scrape(node, HTML) == []

    # 2) find single & valid (but out of bound) indexing for Range object
    node = Node('div', filter=5)
    assert scrape(node, HTML) is None

    # 3) find single & valid indexing for Range object
    node = Node('div', filter=Range(3, -1))
    assert scrape(node, HTML) == []

    # 4) invalid indexing for Range object
    with pytest.raises(EqualIndicesException):
        Node('div', filter=Range(5, 5))
