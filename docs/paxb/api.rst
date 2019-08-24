.. _api:

Developer Interface
===================

.. currentmodule:: paxb


.. automodule:: paxb


Binding
-------

.. autodecorator:: model
.. autofunction:: attribute
.. autofunction:: field
.. autofunction:: nested
.. autofunction:: as_list
.. autofunction:: wrapper

.. data:: attr

    Alias for :py:func:`paxb.attribute`

.. data:: wrap

    Alias for :py:func:`paxb.wrapper`

.. data:: lst

    Alias for :py:func:`paxb.as_list`



Serialization/Deserialization
-----------------------------

.. autofunction:: from_xml
.. autofunction:: to_xml(obj, envelope=None, name=None, ns=None, ns_map=None, encoder=default_encoder, **kwargs)
.. autofunction:: paxb.encoder.encode

Exceptions
----------

.. automodule:: paxb.exceptions
    :members:
