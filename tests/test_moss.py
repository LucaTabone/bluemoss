import pytest
from src.bluemoss import Root, Node, PartialKeysException


def test_partial_keys_exception():
    Root(nodes=[])
    Root(nodes=[Node(key='some_key')])
    with pytest.raises(PartialKeysException):
        Root(nodes=[Node(), Node(key='some_key')])
