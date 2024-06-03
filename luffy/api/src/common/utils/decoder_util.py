import base64


def decode_val(val: str) -> str:
    decoded_data = base64.b64decode(val)
    return decoded_data.decode("utf-8")
