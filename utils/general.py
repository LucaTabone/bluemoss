from functools import cache
from dataclasses import fields, Field, MISSING


@cache
def get_params_with_default_value(dataclass_type) -> set[str]:
    return {
        f.name for f in fields(dataclass_type)
        if f.default != MISSING or f.default_factory != MISSING
    }


def _get_default_value(field: Field) -> any:
    if field.default != MISSING:
        return field.default
    if field.default_factory != MISSING:
        return field.default_factory()
