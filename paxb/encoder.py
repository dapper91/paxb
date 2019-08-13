import base64
import typing as tp
from datetime import datetime


def encode(value):
    """
    Default paxb value encoder. Encodes attributes or element text data during serialization.
    Supports `str`, `bytes` and `datetime` types.

    :param value: value to be encoded
    :return: encoded value string
    """

    if isinstance(value, tp.Text):
        return value
    if isinstance(value, tp.ByteString):
        return base64.b64encode(value)
    if isinstance(value, datetime):
        return value.isoformat()

    return str(value)
