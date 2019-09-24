"""
``paxb`` is a library that provides an API for mapping between XML documents and Python objects.

``paxb`` library implements the following functionality:

- Deserialize XML documents to Python objects
- Validate deserialized data
- Access and update Python object fields
- Serialize Python objects to XML documents

``paxb`` provides an efficient way of mapping between an XML document and a Python object. Using ``paxb``
developers can write less boilerplate code emphasizing on application domain logic.

Since ``paxb`` based on `attrs <https://www.attrs.org/en/stable/index.html>`_ library ``paxb`` and ``attrs``
API can be mixed together.
"""

from .__about__ import (
    __title__,
    __description__,
    __url__,
    __version__,
    __author__,
    __email__,
    __license__
)
from .paxb import (
    as_list,
    attribute,
    field,
    from_xml,
    nested,
    model,
    to_xml,
    wrapper,
)
from . import exceptions as exc


# shortcuts
attr = attribute
wrap = wrapper
lst = as_list


__all__ = [
    '__title__',
    '__description__',
    '__url__',
    '__version__',
    '__author__',
    '__email__',
    '__license__',

    'as_list',
    'attr',
    'attribute',
    'exc',
    'field',
    'from_xml',
    'lst',
    'nested',
    'model',
    'to_xml',
    'wrap',
    'wrapper',
]
