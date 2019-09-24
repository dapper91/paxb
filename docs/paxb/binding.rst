.. _binding:

XML binding
===========

model
-----

The :py:func:`paxb.model` decorator is used to describe a mapping of a python class to an xml element.
All encountered class fields are mapped to the xml subelements. In the following example ``User`` class
attributes ``name`` and ``surname`` are mapped to the corresponding xml elements. The model:

.. code-block:: python

    import paxb as pb

    @pb.model
    class User:
        name = pb.field()
        surname = pb.field()

has a complete mapping description for the document

.. code-block:: xml

    <User>
        <name>Alex</name>
        <surname>Ivanov</surname>
    </User>

By default class name is used as an xml tag name for a mapping. The default behavior can be altered using
decorator ``name`` argument. The ``User`` class can be rewritten as follows:

.. code-block:: python

    import paxb as pb

    @pb.model(name='user')
    class User:
        name = pb.field()
        surname = pb.field()

.. code-block:: xml

    <user>
        <name>Alex</name>
        <surname>Ivanov</surname>
    </user>


field
-----

The :py:func:`paxb.field` function describes a mapping of a python class field to an xml subelement.
In the following example fields ``name`` and ``surname`` are mapped to the corresponding xml subelements.
The name of the fields is used as an xml tag name for a mapping.

.. code-block:: python

    import paxb as pb

    @pb.model
    class User:
        name = pb.field()
        surname = pb.field()

.. code-block:: xml

    <User>
        <name>Alex</name>
        <surname>Ivanov</surname>
    </User>

Similarly to the :py:func:`paxb.model` decorator the default behavior can be altered using the ``name`` argument.

.. code-block:: python

    import paxb as pb

    @pb.model
    class User:
        name = pb.field(name="Name")
        surname = pb.field(name="Surname")

.. code-block:: xml

    <User>
        <Name>Alex</Name>
        <Surname>Ivanov</Surname>
    </User>


attribute
---------

The :py:func:`paxb.attr` function describes a mapping of a python class field to an xml element attribute.
In the following example fields ``name`` and ``surname`` are mapped to the corresponding ``User`` element
attributes. The name of the fields is used as an xml tag name for a mapping.

.. code-block:: python

    import paxb as pb

    @pb.model
    class User:
        name = pb.attr()
        surname = pb.attr()

.. code-block:: xml

    <User name="Alex" surname="Ivanov"/>

Similarly to the :py:func:`paxb.field` function the default behavior can be altered using ``name`` argument.

.. code-block:: python

    import paxb as pb

    @pb.model
    class User:
        name = pb.attribute(name="Name")
        surname = pb.attribute(name="Surname")

.. code-block:: xml

    <User Name="Alex" Name="Ivanov"/>


nested
------

The :py:func:`paxb.nested` function is used to describe a mapping of a python class to an xml element. It is
similar to the :py:func:`paxb.model` decorator, but declares a nested one. Beyond that it acts the same.
The following example illustrates using nested classes:

.. code-block:: python

    imort paxb as pb

    @pb.model
    class Passport:
        series = pb.attribute()
        number = pb.attribute()

    @pb.model
    class User:
        name = pb.attribute()
        surname = pb.attribute()
        passport = pb.nested(Passport)

.. code-block:: xml

    <User name="Alex" surname="Ivanov">
        <Passport series="4581" number="451672"/>
    </User>


as_list
-------

The :py:func:`paxb.as_list` function describes a mapping of a python class field to xml subelements.
The corresponding subelements will be deserialized to a list. An element of a list can be field,
nested class or wrapper (will be described later). Look at the example:

.. code-block:: python

    import paxb as pb

    @pb.model
    class User:
        emails = pb.as_list(pb.field(name="Email"))

.. code-block:: xml

    <User>
        <Email>alex@mail.ru</Email>
        <Email>alex@gmail.com</Email>
        <Email>alex@yandex.ru</Email>
    </User>


wrapper
-------

It is common case when a mapped element is placed in a subelement but declaring a nested class is redundant.
Here the :py:func:`paxb.wrapper` function comes forward. Let's look at the example:

.. code-block:: python

    import paxb as pb

    @pb.model
    class User:
        email = pb.wrapper('contacts', pb.field())

.. code-block:: xml

    <User>
        <contacts>
            <email>alex@gmail.com</email>
        </contacts>
    </User>

Here ``email`` is a direct field of the ``User`` class but in the xml tree it is placed in ``contacts`` subelement.

One :py:func:`paxb.wrapper` can be can be wrapped by another:

.. code-block:: python

    import paxb as pb

    @pb.model
    class User:
        email = pb.wrapper('info', pb.wrapper('contacts', pb.field()))
        ...

.. code-block:: xml

    <User>
        <info>
            <contacts>
                <email>alex@gmail.com</email>
            </contacts>
        </info>
    </User>

A path can be used instead of a tag name. The following model is equivalent to the former one:

.. code-block:: python

    import paxb as pb

    @pb.model
    class User:
        email = pb.wrapper('info/contacts', pb.field())


let's put it all together
-------------------------

All the functions can be mixed together. Look at the more advanced example:

.. code-block:: xml

    <envelope>
        <user name="Alexey" surname="Ivanov" age="26">

            <birthdate year="1992" month="06" day="14"/>

            <contacts>
                <phone>+79204563539</phone>
                <email>alex@gmail.com</email>
                <email>alex@mail.ru</email>
            </contacts>

            <documents>
                <passport series="3127" number="836815"/>
            </documents>

            <occupations>
                <occupation title="yandex">
                    <address>Moscow</address>
                    <employees>8854</employees>
                </occupation>
                <occupation title="skbkontur">
                    <address>Yekaterinburg</address>
                    <employees>7742</employees>
                </occupation>
            </occupations>

        </user>
    </envelope>


.. code-block:: python

    import paxb as pb

    @pb.model(name='occupation')
    class Occupation:
        title = pb.attribute()
        address = pb.field()
        employees = pb.field()

    @pb.model(name='user')
    class User:
        name = pb.attribute()
        surname = pb.attribute()
        age = pb.attribute()

        phone = pb.wrap('contacts', pb.field())
        emails = pb.wrap('contacts', pb.as_list(pb.field(name='email')))

        passport_series = pb.wrap('documents/passport', pb.attribute('series'))
        passport_number = pb.wrap('documents/passport', pb.attribute('number'))

        occupations = pb.wrap('occupations', pb.lst(pb.nested(Occupation)))
