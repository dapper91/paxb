.. _attrs:

attrs library integration
=========================

Since ``paxb`` is based on `attrs <https://www.attrs.org/en/stable/index.html>`_ library ``paxb`` and ``attrs``
APIs can be mixed together.


Decorator :py:func:`paxb.model` accepts :py:func:`attr.s` function
arguments as ``**kwargs`` and internally passes them to it. For example you can pass ``str=True`` argument
to ask ``attrs`` library to generate ``__str__`` method for a class.


Functions :py:func:`paxb.attr`, :py:func:`paxb.field` and :py:func:`paxb.nested` accept :py:func:`attr.ib`
function arguments as ``**kwargs`` and internally passes them to it. For example you can pass ``default``
or ``factory`` argument to set a default value for a class field or ``converter`` argument to convert a value
to an appropriate type. Look at the example:

.. doctest::

    >>> import paxb as pb
    >>>
    >>> @pb.model
    ... class Model:
    ...     field = pb.field(default='1', converter=int)
    ...
    >>> Model()
    Model(field=1)


``paxb`` in conjuction with ``attrs`` library can be used as a flexible xml-to-json converter and vise versa. All you
need is just to declare a model, fields and field types, the rest is up to ``paxb``.

Suppose you have an xml document ``user.xml``:

.. code-block:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <doc:envelope xmlns:doc="http://www.test1.org">
        <doc:user name="Alex" surname="Ivanov" age="26">

            <doc:contacts>
                <doc:phone>+79204563539</doc:phone>
                <doc:email>alex@gmail.com</doc:email>
                <doc:email>alex@mail.ru</doc:email>
            </doc:contacts>

            <data:occupations xmlns:data="http://www.test2.org">
                <data:occupation title="yandex">
                    <data:address>Moscow</data:address>
                    <data:employees>8854</data:employees>
                </data:occupation>
                <data:occupation title="skbkontur">
                    <data:address>Yekaterinburg</data:address>
                    <data:employees>7742</data:employees>
                </data:occupation>
            </data:occupations>

        </doc:user>
    </doc:envelope>


First you need to describe models. Then deserialize the document to an object and call :py:func:`attr.asdict`
``attrs`` library API method:


.. testcode::

    import json
    import attr
    import paxb as pb

    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <doc:envelope xmlns:doc="http://www.test1.org">
        <doc:user name="Alex" surname="Ivanov" age="26">

            <doc:contacts>
                <doc:phone>+79204563539</doc:phone>
                <doc:email>alex@gmail.com</doc:email>
                <doc:email>alex@mail.ru</doc:email>
            </doc:contacts>

            <data:occupations xmlns:data="http://www.test2.org">
                <data:occupation title="yandex">
                    <data:address>Moscow</data:address>
                    <data:employees>8854</data:employees>
                </data:occupation>
                <data:occupation title="skbkontur">
                    <data:address>Yekaterinburg</data:address>
                    <data:employees>7742</data:employees>
                </data:occupation>
            </data:occupations>

        </doc:user>
    </doc:envelope>
    '''

    @pb.model(name="occupation")
    class Occupation:
        title = pb.attribute()
        address = pb.field()
        employees = pb.field(converter=int)

    @pb.model(name="user", ns="doc")
    class User:
        name = pb.attribute()
        surname = pb.attribute()
        age = pb.attribute(converter=int)

        phone = pb.wrap("contacts", pb.field())
        emails = pb.wrap("contacts", pb.as_list(pb.field(name="email")))

        occupations = pb.wrap("occupations", pb.lst(pb.nested(Occupation)), ns="data")

    user = pb.from_xml(User, xml, envelope="doc:envelope", ns_map={
        "doc": "http://www.test1.org",
        "data": "http://www.test2.org",
    })

    print(json.dumps(attr.asdict(user), indent=4))


`Output`:

.. testoutput::

    {
        "name": "Alex",
        "surname": "Ivanov",
        "age": 26,
        "phone": "+79204563539",
        "emails": [
            "alex@gmail.com",
            "alex@mail.ru"
        ],
        "occupations": [
            {
                "title": "yandex",
                "address": "Moscow",
                "employees": 8854
            },
            {
                "title": "skbkontur",
                "address": "Yekaterinburg",
                "employees": 7742
            }
        ]
    }
