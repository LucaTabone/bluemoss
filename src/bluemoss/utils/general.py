from __future__ import annotations
import inspect
from typing import Type, Any
from dataclasses import fields, MISSING, is_dataclass


def get_required_class_init_params(cls: Type[Any] | None) -> set[str]:
    """
    :param cls: class reference
    :rtype: set[str]
    :return: The set of required initialization parameters for the given class.
    """
    if cls is None:
        return set()
    return get_all_class_init_params(cls) - get_optional_class_init_params(cls)


def get_all_class_init_params(cls: Type[Any] | None) -> set[str]:
    """
    :param cls: class reference
    :rtype: set[str]
    :return: The set of all initialization parameters for the given class.
    """
    if cls is None:
        return set()
    return set(inspect.getfullargspec(cls.__init__).args[1:])


def get_optional_class_init_params(cls: Type[Any] | None) -> set[str]:
    """
    :param cls: class reference
    :rtype: set[str]
    :return: The set of optional initialization parameters for the given class.
    """
    if cls is None:
        return set()
    if is_dataclass(cls):
        return {
            f.name
            for f in fields(cls)
            if f.default != MISSING or f.default_factory != MISSING
        }
    return {
        name
        for name, param in inspect.signature(cls.__init__).parameters.items()
        if param.default != inspect.Parameter.empty
    }


__all__ = [
    'get_all_class_init_params',
    'get_optional_class_init_params',
    'get_required_class_init_params',
]
