from typing import List, Any

# TODO: Improve so that it can take any number of K:V pairs


def generate_message_json(http_status_code, value, key="message"):
    return {key: value}, http_status_code


def check_attr(attrs: List[str], obj: Any) -> bool:
    for attr in attrs:
        getattr(obj, attr)
