import base64
import typing as tp
import datetime as dt


def encode(value):
    """
    Default ``paxb`` value encoder. Encodes attributes or element text data during serialization.
    Supports :py:class:`str`, :py:class:`bytes`, :py:class:`datetime.date` and :py:class:`datetime.datetime` types.

    :param value: value to be encoded
    :return: encoded value string
    :rtype: str
    """

    if isinstance(value, tp.Text):
        return value
    if isinstance(value, tp.ByteString):
        return base64.b64encode(value)
    if isinstance(value, dt.datetime):
        return value.isoformat()
    if isinstance(value, dt.date):
        return value.isoformat()

    return str(value)
