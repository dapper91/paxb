.. _errors:

Errors
======

The package has two main exceptions: :py:exc:`paxb.exceptexcions.SerializationError` and
:py:class:`paxb.exceptexcions.DeserializationError`.

:py:class:`paxb.exceptexcions.DeserializationError` is raised when any deserialization error occurs.
The most common case it is raised is a required element is not found in an xml tree. Look at the example:

.. doctest::
    :options: -IGNORE_EXCEPTION_DETAIL

    >>> import paxb as pb
    >>>
    >>> @pb.model
    ... class User:
    ...     name = pb.attribute()
    ...
    >>> xml_str = '<User/>'
    >>> pb.from_xml(User, xml_str)
    Traceback (most recent call last):
    ...
    paxb.exceptions.DeserializationError: required attribute '/User[1]/name' not found


This error is raised when either of :py:func:`paxb.field`, :py:func:`paxb.attr`, :py:func:`paxb.nested`
or :py:func:`paxb.wrapper` element not found. This behaviour can be altered by passing a default value to an element:

.. doctest::

    >>> import paxb as pb
    >>>
    >>> @pb.model
    ... class User:
    ...     name = pb.attr(default='Alex')
    ...
    >>> xml_str = '<User/>'
    >>> pb.from_xml(User, xml_str)
    User(name='Alex')

The same applies to :py:func:`paxb.field`, :py:func:`paxb.nested` and :py:func:`paxb.wrapper`.


:py:class:`paxb.exceptexcions.SerializationError` is raised when any serialization error occurs.
The most common case it is raised is a required element is not set. Look at the example:

.. doctest::
    :options: -IGNORE_EXCEPTION_DETAIL

    >>> import paxb as pb
    >>>
    >>> @pb.model
    ... class User:
    ...     name = pb.attr()
    ...
    >>> obj = User(name=None)
    >>> pb.to_xml(obj)
    Traceback (most recent call last):
    ...
    paxb.exceptions.SerializationError: required attribute 'name' is not set

This error is raised when either of :py:func:`paxb.field`, :py:func:`paxb.attr`, :py:func:`paxb.nested`
or :py:func:`paxb.wrapper` element is not set. This behaviour can be altered by passing a default value to an element:

.. doctest::

    >>> import paxb as pb
    >>>
    >>> @pb.model
    ... class User:
    ...     name = pb.attr(default='Alex')
    ...
    >>> obj = User()
    >>> pb.to_xml(obj)
    b'<User name="Alex" />'
