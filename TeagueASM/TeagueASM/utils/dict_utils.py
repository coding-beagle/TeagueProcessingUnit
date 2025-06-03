from typing import Any


def fetch_from_dict_by_val(input_dict: dict[Any, Any], value: Any) -> Any:
    return list(input_dict.keys())[list(input_dict.values()).index(value)]
