====
paxb
====

.. image:: https://travis-ci.org/dapper91/paxb.svg?branch=master
    :target: https://travis-ci.org/dapper91/paxb
    :alt: Build status
.. image:: https://img.shields.io/pypi/l/paxb.svg
    :target: https://pypi.org/project/paxb
    :alt: License
.. image:: https://img.shields.io/pypi/pyversions/paxb.svg
    :target: https://pypi.org/project/paxb
    :alt: Supported Python versions
.. image:: https://codecov.io/gh/dapper91/paxb/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dapper91/paxb
    :alt: Code coverage


Python Architecture for XML Binding
-----------------------------------

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


Installation
------------

You can install paxb with pip:

.. code-block:: console

    $ pip install paxb


Requirements
------------

- `attrs <https://www.attrs.org/en/stable/index.html>`_


Documentation
-------------

Documentation is available at `Read the Docs <https://paxb.readthedocs.io/en/latest/>`_.


Quick start
===========

Suppose you have an xml document ``user.xml``:

.. code-block:: xml

    <?xml version="1.0" encoding="utf-8"?>
    <doc:envelope xmlns="http://www.test.org"
                  xmlns:doc="http://www.test1.org">
        <doc:user name="Alex" surname="Ivanov" age="26">

            <doc:birthdate year="1992" month="06" day="14"/>

            <doc:contacts>
                <doc:phone>+79204563539</doc:phone>
                <doc:email>alex@gmail.com</doc:email>
                <doc:email>alex@mail.ru</doc:email>
            </doc:contacts>

            <doc:documents>
                <doc:passport series="3127" number="836815"/>
            </doc:documents>

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


To deserialize the document you could use `xml <https://docs.python.org/3/library/xml.html>`_ library api to parse
the document and then access and modify the parsed xml DOM manually. Such an imperative code has a lot of boilerplate
operations that takes a lot of time and can lead to bugs. Instead you can use ``paxb`` api to write a declarative
style code. All you need to describe field mappings and types, ``paxb`` will serialize and deserialize data for you:

.. code-block:: python

    import json
    import re
    from datetime import date

    import attr
    import paxb as pb


    @pb.model(name='occupation', ns='data', ns_map={'data': 'http://www.test2.org'})
    class Occupation:
        title = pb.attr()
        address = pb.field()
        employees = pb.field(converter=int)


    @pb.model(name='user', ns='doc', ns_map={'doc': 'http://www.test1.org'})
    class User:
        name = pb.attr()
        surname = pb.attr()
        age = pb.attr(converter=int)

        birth_year = pb.wrap('birthdate', pb.attr('year', converter=int))
        birth_month = pb.wrap('birthdate', pb.attr('month', converter=int))
        birth_day = pb.wrap('birthdate', pb.attr('day', converter=int))

        @property
        def birthdate(self):
            return date(year=self.birth_year, month=self.birth_month, day=self.birth_day)

        @birthdate.setter
        def birthdate(self, value):
            self.birth_year = value.year
            self.birth_month = value.month
            self.birth_day = value.day

        phone = pb.wrap('contacts', pb.field())
        emails = pb.wrap('contacts', pb.as_list(pb.field(name='email')))

        passport_series = pb.wrap('documents/passport', pb.attr('series'))
        passport_number = pb.wrap('documents/passport', pb.attr('number'))

        occupations = pb.wrap(
            'occupations', pb.lst(pb.nested(Occupation)), ns='data', ns_map={'data': 'http://www.test2.org'}
        )

        citizenship = pb.field(default='RU')

        @phone.validator
        def check(self, attribute, value):
            if not re.match(r'\+\d{11,13}', value):
                raise ValueError("phone number is incorrect")


    with open('user.xml') as file:
        xml = file.read()


Then the deserialized object can be modified and serialized back to xml document or converted to json format:

.. code-block:: python

    try:
        user = pb.from_xml(User, xml, envelope='doc:envelope', ns_map={'doc': 'http://www.test1.org'})
        user.birthdate = user.birthdate.replace(year=1993)

        with open('user.json') as file:
            json.dump(attr.asdict(user), file)

    except (pb.exc.DeserializationError, ValueError) as e:
        print(f"deserialization error: {e}")


``user.json``:

.. code-block:: json

    {
        "age": 26,
        "birth_day": 14,
        "birth_month": 6,
        "birth_year": 1993,
        "citizenship": "RU",
        "emails": ["alex@gmail.com", "alex@mail.ru"],
        "name": "Alexey",
        "occupations": [
            {
                "address": "Moscow",
                "employees": 8854,
                "title": "yandex"
            },
            {
                "address": "Yekaterinburg",
                "employees": 7742,
                "title": "skbkontur"
            }
        ],
        "passport_number": "836815",
        "passport_series": "3127",
        "phone": "+79204563539",
        "surname": "Ivanov"
    }
