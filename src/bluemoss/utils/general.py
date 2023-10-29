import inspect
from functools import cache


@cache
def get_class_init_params(cls) -> set[str]:
    assert inspect.isclass(cls)
    return set(inspect.getfullargspec(cls.__init__).args[1:])


__all__ = [
    "get_class_init_params"
]
