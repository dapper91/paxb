import xmldiff.main
import paxb as pb


def test_root_serialization():

    @pb.model(name='test_model')
    class TestModel:
        element1 = pb.field()

    obj = TestModel(element1='value1')

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <test_model>
        <element1>value1</element1>
    </test_model>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_attribute_serialization():

    @pb.model
    class TestModel:
        attrib1 = pb.attr()
        attrib2 = pb.attr()

    obj = TestModel(attrib1='value1', attrib2='value2')

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel attrib1="value1" attrib2="value2"/>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_attribute_serialization_with_name():

    @pb.model
    class TestModel:
        attrib1 = pb.attr(name='attribute1')
        attrib2 = pb.attr(name='attribute2')

    obj = TestModel(attrib1="value1", attrib2="value2")

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel attribute1="value1" attribute2="value2"/>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_element_serialization():

    @pb.model
    class TestModel:
        element1 = pb.field()
        element2 = pb.field()

    obj = TestModel(element1="value1", element2="value2")

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <element1>value1</element1>
        <element2>value2</element2>
    </TestModel>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_element_serialization_with_name():

    @pb.model
    class TestModel:
        elem1 = pb.field(name='element1')
        elem2 = pb.field(name='element2')

    obj = TestModel(elem1="value1", elem2="value2")

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <element1>value1</element1>
        <element2>value2</element2>
    </TestModel>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_wrapper_serialization():

    @pb.model
    class TestModel:
        element1 = pb.wrap('wrapper1', pb.wrap('wrapper2', pb.field()))

    obj = TestModel(element1="value1")

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <wrapper1>
            <wrapper2>
                <element1>value1</element1>
            </wrapper2>
        </wrapper1>
    </TestModel>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_wrapper_serialization_with_path():

    @pb.model
    class TestModel:
        element1 = pb.wrap('wrapper1/wrapper2', pb.field())

    obj = TestModel(element1="value1")

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <wrapper1>
            <wrapper2>
                <element1>value1</element1>
            </wrapper2>
        </wrapper1>
    </TestModel>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_inheritance_serialization():

    @pb.model
    class TestBaseModel:
        element1 = pb.field()

    @pb.model
    class TestExtendedModel(TestBaseModel):
        element2 = pb.field()

    @pb.model
    class TestRootModel:
        model1 = pb.nested(TestBaseModel)
        model2 = pb.nested(TestExtendedModel)

    obj = TestRootModel(
        model1=TestBaseModel(element1="value1"),
        model2=TestExtendedModel(element1="value2", element2="value3")
    )

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestRootModel>
        <TestBaseModel>
            <element1>value1</element1>
        </TestBaseModel>
        <TestExtendedModel>
            <element1>value2</element1>
            <element2>value3</element2>
        </TestExtendedModel>
    </TestRootModel>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_nested_serialization():

    @pb.model
    class NestedModel2:
        element = pb.field()

    @pb.model
    class NestedModel1:
        nested = pb.nested(NestedModel2)

    @pb.model
    class TestModel:
        nested = pb.nested(NestedModel1)

    obj = TestModel(nested=NestedModel1(nested=NestedModel2(element="value")))

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <NestedModel1>
            <NestedModel2>
                <element>value</element>
            </NestedModel2>
        </NestedModel1>
    </TestModel>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_element_list_serialization():

    @pb.model
    class TestModel:
        element1 = pb.as_list(pb.field())

    obj = TestModel(element1=["value1", "value2"])

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <element1>value1</element1>
        <element1>value2</element1>
    </TestModel>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_wrapper_list_serialization():

    @pb.model
    class TestModel:
        elements = pb.as_list(pb.wrap('wrapper', pb.field('element')))

    obj = TestModel(elements=["value1", "value2"])

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <wrapper>
            <element>value1</element>
        </wrapper>
        <wrapper>
            <element>value2</element>
        </wrapper>
    </TestModel>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_nested_list_serialization():

    @pb.model
    class NestedModel:
        element = pb.field()

    @pb.model
    class TestModel:
        elements = pb.as_list(pb.nested(NestedModel))

    obj = TestModel(elements=[NestedModel(element="value1"), NestedModel(element="value2")])

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <NestedModel>
            <element>value1</element>
        </NestedModel>
        <NestedModel>
            <element>value2</element>
        </NestedModel>
    </TestModel>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_list_of_list_serialization():
    @pb.model
    class TestModel:
        elements = pb.as_list(pb.wrap('element1', pb.as_list(pb.field('element2'))))

    obj = TestModel(elements=[["value1", "value2"], ["value3", "value4"]])

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <element1>
            <element2>value1</element2>
            <element2>value2</element2>
        </element1>
        <element1>
            <element2>value3</element2>
            <element2>value4</element2>
        </element1>
    </TestModel>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_namespaces_serialization():

    @pb.model(ns='testns1', ns_map={'testns2': 'http://www.test2.org'})
    class TestModel:
        element1 = pb.field(ns='')
        element2 = pb.field()
        element3 = pb.field(ns='testns2')
        element5 = pb.wrap('element4', pb.field(ns=''))
        element6 = pb.wrap('element4', pb.field(ns='testns2'), ns_map={'testns2': 'http://www.test22.org'})

    obj = TestModel(
        element1="value1",
        element2="value2",
        element3="value3",
        element5="value5",
        element6="value6",
    )

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <testns1:TestModel xmlns:testns1="http://www.test1.org"
                       xmlns:testns2="http://www.test2.org">
        <element1>value1</element1>
        <testns1:element2>value2</testns1:element2>
        <testns2:element3>value3</testns2:element3>
        <testns1:element4 xmlns:testns2="http://www.test22.org">
            <element5>value5</element5>
            <testns2:element6>value6</testns2:element6>
        </testns1:element4>
    </testns1:TestModel>
    '''

    actual_xml = pb.to_xml(obj, ns_map={
        'testns1': 'http://www.test1.org',
        'testns2': 'http://www.test2.org',
    })

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_complex_xml_serialization():

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

        phone = pb.wrap('contacts', pb.field())
        emails = pb.wrap('contacts', pb.as_list(pb.field(name='email')))

        passport_series = pb.wrap('documents', pb.wrap('passport', pb.attr('series')))
        passport_number = pb.wrap('documents', pb.wrap('passport', pb.attr('number')))

        occupations = pb.wrap('occupations', pb.lst(pb.nested(Occupation)), ns='data')

        citizenship = pb.field(default='RU')

    occupation1 = Occupation(
        title='yandex',
        address='Moscow',
        employees=8854,
    )
    occupation2 = Occupation(
        title='skbkontur',
        address='Yekaterinburg',
        employees=7742,
    )

    obj = User(
        name='Alexey',
        surname='Ivanov',
        age=26,
        phone='+79204563539',
        emails=['alex@gmail.com', 'alex@mail.ru'],
        passport_series='3127',
        passport_number='836815',
        occupations=[occupation1, occupation2],
        citizenship='RU',
    )

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <doc:envelope xmlns:doc="http://www.test1.org"
                  xmlns:data="http://www.test2.org">
        <doc:user name="Alexey" surname="Ivanov" age="26">

            <doc:contacts>
                <doc:phone>+79204563539</doc:phone>
                <doc:email>alex@gmail.com</doc:email>
                <doc:email>alex@mail.ru</doc:email>
            </doc:contacts>

            <doc:documents>
                <doc:passport series="3127" number="836815"/>
            </doc:documents>

            <data:occupations>
                <data:occupation title="yandex">
                    <data:address>Moscow</data:address>
                    <data:employees>8854</data:employees>
                </data:occupation>
                <data:occupation title="skbkontur">
                    <data:address>Yekaterinburg</data:address>
                    <data:employees>7742</data:employees>
                </data:occupation>
            </data:occupations>

            <doc:citizenship>RU</doc:citizenship>

        </doc:user>
    </doc:envelope>
    '''

    actual_xml = pb.to_xml(obj, envelope='doc:envelope', ns_map={
        'doc': 'http://www.test1.org',
        'data': 'http://www.test2.org',
    })

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_indexes_deserialization():

    @pb.model(name='nested')
    class Nested:
        field = pb.field('element')

    @pb.model(name='root')
    class TestModel:
        field1 = pb.field('element', idx=1)
        field2 = pb.field('element', idx=2)

        field3 = pb.wrap('wrapper', pb.field('element'), idx=1)
        field4 = pb.wrap('wrapper', pb.field('element'), idx=2)

        nested1 = pb.nested(Nested, idx=1)
        nested2 = pb.nested(Nested, idx=2)

    obj = TestModel(
        field1="value1",
        field2="value2",
        field3="value3",
        field4="value4",

        nested1=Nested(field="value5"),
        nested2=Nested(field="value6"),
    )

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <root>
        <element>value1</element>
        <element>value2</element>

        <wrapper>
            <element>value3</element>
        </wrapper>
        <wrapper>
            <element>value4</element>
        </wrapper>

        <nested>
            <element>value5</element>
        </nested>
        <nested>
            <element>value6</element>
        </nested>
    </root>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_empty_model_serialization():

    @pb.model(name='test_model')
    class TestModel:
        element1 = pb.field(default=None)

    obj = TestModel()

    assert pb.to_xml(obj) is None


def test_empty_model_serialization_with_list():

    @pb.model(name='test_model')
    class TestModel:
        element1 = pb.lst(pb.field())

    obj = TestModel(element1=[])

    assert pb.to_xml(obj) is None


def test_empty_element_serialization():

    @pb.model(name='test_model')
    class TestModel:
        element1 = pb.field()
        element2 = pb.field(default=None)

    obj = TestModel(element1='value1')

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <test_model>
        <element1>value1</element1>
    </test_model>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_empty_attribute_serialization():

    @pb.model(name='test_model')
    class TestModel:
        attribute1 = pb.attr()
        attribute2 = pb.attr(default=None)

    obj = TestModel(attribute1='value1')

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <test_model attribute1="value1"/>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_empty_list_serialization():

    @pb.model(name='test_model')
    class TestModel:
        element1 = pb.field()
        element2 = pb.lst(pb.field())

    obj = TestModel(element1='value1', element2=[])

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <test_model>
        <element1>value1</element1>
    </test_model>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_empty_nested_serialization():

    @pb.model
    class NestedModel:
        element1 = pb.field()

    @pb.model(name='test_model')
    class TestModel:
        element1 = pb.field()
        element2 = pb.nested(NestedModel, default=None)

    obj = TestModel(element1='value1')

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <test_model>
        <element1>value1</element1>
    </test_model>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_empty_wrapper_serialization():

    @pb.model(name='test_model')
    class TestModel:
        element1 = pb.field()
        element2 = pb.wrap('wrapper1', pb.wrap('wrapper2', pb.field(default=None)))

    obj = TestModel(element1='value1')

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <test_model>
        <element1>value1</element1>
    </test_model>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())


def test_serialization_order():
    @pb.model(order=('element2', 'element1'))
    class TestModel:
        element1 = pb.field()
        element2 = pb.field()
        element3 = pb.field()
        element4 = pb.field()

    obj = TestModel(element1='value1', element2='value2', element3='value3', element4='value4')

    expected_xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <element2>value2</element2>
        <element1>value1</element1>
        <element3>value3</element3>
        <element4>value4</element4>
    </TestModel>
    '''

    actual_xml = pb.to_xml(obj)

    assert not xmldiff.main.diff_texts(actual_xml, expected_xml.encode())
