.. _namespaces:

Namespaces
==========

Namespace inheritance
---------------------

The default namespace of any element is an empty namespace. Functions :py:func:`paxb.field`, :py:func:`paxb.model`,
:py:func:`paxb.wrapper` and :py:func:`paxb.nested` have a ``ns`` argument which alters the default (empty) namespace
by a passed one. Compare two examples:

.. doctest::

    >>> import paxb as pb
    >>>
    >>> @pb.model
    ... class User:
    ...     name = pb.field()
    ...     surname = pb.field()
    ...
    >>> user = User(name='Alex', surname='Ivanov')
    >>>
    >>> pb.to_xml(user)
    b'<User><name>Alex</name><surname>Ivanov</surname></User>'


.. doctest::

    >>> import paxb as pb
    >>>
    >>> @pb.model(ns='test1')
    ... class User:
    ...     name = pb.field(ns='test2')
    ...     surname = pb.field(ns='test3')
    ...
    >>> user = User(name='Alex', surname='Ivanov')
    >>>
    >>> pb.to_xml(user, ns_map={
    ...     'test1': 'http://test1.org',
    ...     'test2': 'http://test2.org',
    ...     'test3': 'http://test3.org',
    ... })
    b'<test1:User xmlns:test1="http://test1.org" xmlns:test2="http://test2.org" xmlns:test3="http://test3.org"><test2:name>Alex</test2:name><test3:surname>Ivanov</test3:surname></test1:User>'


The ``ns_map`` argument describes a mapping from a namespace prefix to a full name that will be used during
serialization and deserializaion.


The namespace of :py:func:`paxb.field`, :py:func:`paxb.wrapper` and :py:func:`paxb.nested` is inherited
from the containing model if it is not declared explicitly. Look at the example:


.. testcode::

    from xml.dom.minidom import parseString
    import paxb as pb

    @pb.model
    class Passport:                     # implicit namespace, will be inherited from a containing model
        series = pb.field()             # implicit namespace, the same as of Passport model
        number = pb.field(ns='test3')   # explicit namespace 'test3'

    @pb.model(ns='test2')               # namespace 'test2' explicitly set for DrivingLicence and implicitly set for all contained elements
    class DrivingLicence:               # explicit namespace 'test2'
        number = pb.field()             # implicit namespace 'test2'

    @pb.model(ns='test1')               # namespace 'test1' explicitly set for User and implicitly set for all contained elements
    class User:                         # explicit namespace 'test1'
        name = pb.field()               # implicit namespace 'test1'
        surname = pb.field(ns='test2')  # explicit namespace 'test2'

        passport = pb.nested(Passport)                 # default namespace for the contained model Passport will be set to 'test1'
        driving_licence = pb.nested(DrivingLicence)    # default namespace for the contained model DrivingLicence will be set to 'test1'

    passport = Passport(series="5425", number="541125")
    licence = DrivingLicence(number="673457")
    user = User(name='Alex', surname='Ivanov', passport=passport, driving_licence=licence)

    xml = pb.to_xml(user, ns_map={
        'test1': 'http://test1.org',
        'test2': 'http://test2.org',
        'test3': 'http://test3.org',
    }, encoding='unicode')
    print(parseString(xml).toprettyxml(indent=' ' * 4), end='')

`Output`:

.. testoutput::

    <?xml version="1.0" ?>
    <test1:User xmlns:test1="http://test1.org" xmlns:test2="http://test2.org" xmlns:test3="http://test3.org">
        <test1:name>Alex</test1:name>
        <test2:surname>Ivanov</test2:surname>
        <test1:Passport>
            <test1:series>5425</test1:series>
            <test3:number>541125</test3:number>
        </test1:Passport>
        <test2:DrivingLicence>
            <test2:number>673457</test2:number>
        </test2:DrivingLicence>
    </test1:User>
