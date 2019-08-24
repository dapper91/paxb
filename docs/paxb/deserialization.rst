.. _deserialization:

Deserialization
===============

``paxb`` implements an API for deserializing an xml string to a python object.
To serialize an object just pass a class and an xml string to a :py:func:`paxb.from_xml` method:

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
    >>> xml_str = '<User name="Alex" surname="Ivanov"><email>alex@gmail.com</email><phone>+79123457323</phone></User>'
    >>> pb.from_xml(User, xml_str)
    User(name='Alex', surname='Ivanov', email='alex@gmail.com', phone='+79123457323')


By default :py:func:`paxb.from_xml` method deserializes an object from a root element in an xml tree, class name
is used as an element name, the element namespace is empty. The default behaviour can be altered
using :py:func:`paxb.from_xml` additional arguments. Look at the example:

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
    >>> xml_str = '<root xmlns:test="http://www.test.org"><test:user name="Alex" surname="Ivanov"><test:email>alex@gmail.com</test:email><test:phone>+79123457323</test:phone></test:user></root>'
    >>> pb.from_xml(User, xml_str, envelope='root', name='user', ns='test', ns_map={'test': 'http://www.test.org'}, required=True)
    User(name='Alex', surname='Ivanov', email='alex@gmail.com', phone='+79123457323')


The ``required`` argument tells the deserializer to raise an exception if the element not found in the xml tree,
otherwise ``None`` will be returned (see :ref:`Errors <errors>`).

By default all fields deserialized as :py:class:`str` types. The default behaviour can be altered using a
``converter`` parameter. See :py:func:`attr.ib`.

.. doctest::

    >>> import datetime
    >>> import paxb as pb
    >>>
    >>> @pb.model
    ... class User:
    ...     age = pb.attribute(converter=int)
    ...     birthdate = pb.field(converter=datetime.date.fromisoformat)
    ...
    >>> xml_str = '<User age="26"><birthdate>1993-08-21</birthdate></User>'
    >>> pb.from_xml(User, xml_str)
    User(age=26, birthdate=datetime.date(1993, 8, 21))


To deserialize an object from a json document use python :py:mod:`json` package:

.. doctest::

    >>> import json
    >>> import paxb as pb
    >>>
    >>> @pb.model
    ... class User:
    ...     name = pb.attribute()
    ...     surname = pb.attribute()
    ...     email = pb.field()
    ...     phone = pb.field()
    ...
    >>> json_str = '{"name": "Alex", "surname": "Ivanov", "email": "alex@gmail.com", "phone": "+79123457323"}'
    >>> User(**json.loads(json_str))
    User(name='Alex', surname='Ivanov', email='alex@gmail.com', phone='+79123457323')
