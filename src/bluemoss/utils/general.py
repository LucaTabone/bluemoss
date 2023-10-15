import inspect
from typing import Type
from functools import cache
from dataclasses import fields, Field, MISSING


@cache
def get_init_params(class_ref: Type[any]) -> set[str]:
    assert inspect.isclass(class_ref)
    return set(inspect.getfullargspec(class_ref.__init__).args[1:])


@cache
def get_params_with_default_value(dataclass_type) -> set[str]:
    return {
        f.name for f in fields(dataclass_type)
        if f.default != MISSING or f.default_factory != MISSING
    }


def _get_default_value(f: Field) -> any:
    if f.default != MISSING:
        return f.default
    if f.default_factory != MISSING:
        return f.default_factory()
