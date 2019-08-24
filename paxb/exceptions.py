"""
Package errors.
"""


class BaseError(Exception):
    """
    Base package exception. All package exception are inherited from it.
    """


class SerializationError(BaseError):
    """
    Serialization error. Raised when any serialization error occurs.
    """


class DeserializationError(BaseError):
    """
    Deserialization error. Raised when any deserialization error occurs.
    """
