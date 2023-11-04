import pytest
from src.bluemoss import Node, PartialKeysException


def test_partial_keys_exception():
    Node(nodes=[])
    Node(nodes=[Node(key='some_key')])
    with pytest.raises(PartialKeysException):
        Node(nodes=[Node(), Node(key='some_key')])
