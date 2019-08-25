.. _serialization:

Serialization
=============

``paxb`` implements an API for serializing an python object to an xml string.
To serialize an object just pass it to a :py:func:`paxb.to_xml` method:

.. doctest::

    >>> import paxb as pb
    >>>
    >>> @pb.model
    ... class User:
    ...     name = pb.attribute()
    ...     surname = pb.attribute()
    ...     email = pb.field()
    ...     phone = pb.field()
    ...
    >>> obj = User(name='Alex', surname='Ivanov', email='alex@gmail.com', phone='+79123457323')
    >>>
    >>> xml_string = pb.to_xml(obj)
    >>> print(xml_string)
    b'<User name="Alex" surname="Ivanov"><email>alex@gmail.com</email><phone>+79123457323</phone></User>'

By default :py:func:`paxb.to_xml` method serializes an object to a root element in an xml tree,
class name is used as the element name, the element namespace is empty.
The default behaviour can be altered using :py:func:`paxb.to_xml` argument. Look at the example:

.. doctest::

    >>> import paxb as pb
    >>>
    >>> @pb.model
    ... class User:
    ...     name = pb.attribute()
    ...     surname = pb.attribute()
    ...     email = pb.field()
    ...     phone = pb.field()
    ...
    >>> obj = User(name='Alex', surname='Ivanov', email='alex@gmail.com', phone='+79123457323')
    >>>
    >>> xml_string = pb.to_xml(obj, envelope='root', name='user', ns='test', ns_map={'test': 'http://www.test.org'}, encoding='unicode')
    >>> print(xml_string)
    <root xmlns:test="http://www.test.org"><test:user name="Alex" surname="Ivanov"><test:email>alex@gmail.com</test:email><test:phone>+79123457323</test:phone></test:user></root>

The ``encoding`` argument is an additional argument passed to :py:func:`xml.etree.ElementTree.tostring`  method.

Encoder
-------

By default an object fields serialized using the following rules:

- :py:class:`str` field is serialized as it is.
- :py:class:`bytes` field serialized using base64 encoding.
- :py:class:`datetime.datetime` field serialized as iso formatted string.
- :py:class:`datetime.date` field serialized as iso formatted string.
- other types serialized using :py:meth:`__str__`.

The default behaviour can be altered using ``encoder`` argument. Encoder must be a callable object that accepts
an encoded value and returns its :py:class:`str` representation.


Since ``paxb`` is based on :py:mod:`attr` library, :py:func:`attr.asdict` function can
be used to serialize an object to a json string:

.. doctest::

    >>> import attr
    >>> import json
    >>> import paxb as pb
    >>>
    >>> @pb.model
    ... class User:
    ...     name = pb.attribute()
    ...     surname = pb.attr()
    ...     email = pb.field()
    ...     phone = pb.field()
    ...
    >>> obj = User(name='Alex', surname='Ivanov', email='alex@gmail.com', phone='+79123457323')
    >>>
    >>> obj_dict = attr.asdict(obj)
    >>> json.dumps(obj_dict)
    '{"name": "Alex", "surname": "Ivanov", "email": "alex@gmail.com", "phone": "+79123457323"}'
