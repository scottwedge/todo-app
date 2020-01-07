# TODO: Improve so that it can take any number of K:V pairs


def generate_message_json(http_status_code, value, key="message"):
    return {key: value}, http_status_code
