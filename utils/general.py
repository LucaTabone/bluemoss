from dataclasses import fields, Field, MISSING


def update_params_with_defaults(dataclass_type, params: dict[str, any]) -> dict[str, any]:
    defaults = {}
    for _field in fields(dataclass_type):
        if _field.name in params and params.get(_field.name, None) is None:
            defaults[_field.name] = _get_default_value(_field)
    return params | defaults


def _get_default_value(field: Field) -> any:
    if field.default != MISSING:
        return field.default
    if field.default_factory != MISSING:
        return field.default_factory()
