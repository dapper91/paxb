from xml.etree import ElementTree as et
import paxb as pb


def test_root_deserialization():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <test_model>
        <element1>value1</element1>
    </test_model>
    '''

    @pb.model(name='test_model')
    class TestModel:
        element1 = pb.field()

    model = pb.from_xml(TestModel, xml)

    assert model.element1 == 'value1'


def test_attribute_deserialization():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel attrib1="value1" attrib2="value2"/>
    '''

    @pb.model
    class TestModel:
        attrib1 = pb.attr()
        attrib2 = pb.attr()

    model = pb.from_xml(TestModel, xml)

    assert model.attrib1 == 'value1'
    assert model.attrib2 == 'value2'


def test_attribute_deserialization_with_name():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel attribute1="value1" attribute2="value2"/>
    '''

    @pb.model
    class TestModel:
        attrib1 = pb.attr(name='attribute1')
        attrib2 = pb.attr(name='attribute2')

    model = pb.from_xml(TestModel, xml)

    assert model.attrib1 == 'value1'
    assert model.attrib2 == 'value2'


def test_element_deserialization():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <element1>value1</element1>
        <element2>value2</element2>
    </TestModel>
    '''

    @pb.model
    class TestModel:
        element1 = pb.field()
        element2 = pb.field()

    model = pb.from_xml(TestModel, xml)

    assert model.element1 == 'value1'
    assert model.element2 == 'value2'


def test_element_deserialization_with_name():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <element1>value1</element1>
        <element2>value2</element2>
    </TestModel>
    '''

    @pb.model
    class TestModel:
        elem1 = pb.field(name='element1')
        elem2 = pb.field(name='element2')

    model = pb.from_xml(TestModel, xml)

    assert model.elem1 == 'value1'
    assert model.elem2 == 'value2'


def test_wrapper_deserialization():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <wrapper1>
            <wrapper2>
                <element1>value1</element1>
            </wrapper2>
        </wrapper1>
    </TestModel>
    '''

    @pb.model
    class TestModel:
        element1 = pb.wrap('wrapper1', pb.wrap('wrapper2', pb.field()))

    model = pb.from_xml(TestModel, xml)

    assert model.element1 == 'value1'


def test_wrapper_deserialization_with_path():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <wrapper1>
            <wrapper2>
                <element1>value1</element1>
            </wrapper2>
        </wrapper1>
    </TestModel>
    '''

    @pb.model
    class TestModel:
        element1 = pb.wrap('wrapper1/wrapper2', pb.field())

    model = pb.from_xml(TestModel, xml)

    assert model.element1 == 'value1'


def test_inheritance_deserialization():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
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

    model = pb.from_xml(TestRootModel, xml)

    assert model.model1.element1 == 'value1'
    assert model.model2.element1 == 'value2'
    assert model.model2.element2 == 'value3'


def test_nested_deserialization():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <NestedModel1>
            <NestedModel2>
                <element>value</element>
            </NestedModel2>
        </NestedModel1>
    </TestModel>
    '''

    @pb.model
    class NestedModel2:
        element = pb.field()

    @pb.model
    class NestedModel1:
        nested = pb.nested(NestedModel2)

    @pb.model
    class TestModel:
        nested = pb.nested(NestedModel1)

    model = pb.from_xml(TestModel, xml)

    assert model.nested.nested.element == 'value'


def test_element_list_deserialization():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <element1>value1</element1>
        <element1>value2</element1>
    </TestModel>
    '''

    @pb.model
    class TestModel:
        element1 = pb.as_list(pb.field())

    model = pb.from_xml(TestModel, xml)

    assert model.element1 == ['value1', 'value2']


def test_wrapper_list_deserialization():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <wrapper>
            <element>value1</element>
        </wrapper>
        <wrapper>
            <element>value2</element>
        </wrapper>
    </TestModel>
    '''

    @pb.model
    class TestModel:
        elements = pb.as_list(pb.wrap('wrapper', pb.field('element')))

    model = pb.from_xml(TestModel, xml)

    assert model.elements == ['value1', 'value2']


def test_nested_list_deserialization():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <NestedModel>
            <element>value1</element>
        </NestedModel>
        <NestedModel>
            <element>value2</element>
        </NestedModel>
    </TestModel>
    '''

    @pb.model
    class NestedModel:
        element = pb.field()

    @pb.model
    class TestModel:
        elements = pb.as_list(pb.nested(NestedModel))

    model = pb.from_xml(TestModel, xml)

    assert len(model.elements) == 2
    assert model.elements[0].element == 'value1'
    assert model.elements[1].element == 'value2'


def test_list_of_list_deserialization():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
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

    @pb.model
    class TestModel:
        elements = pb.as_list(pb.wrap('element1', pb.as_list(pb.field('element2'))))

    model = pb.from_xml(TestModel, xml)

    assert model.elements[0][0] == 'value1'
    assert model.elements[0][1] == 'value2'
    assert model.elements[1][0] == 'value3'
    assert model.elements[1][1] == 'value4'


def test_namespaces_deserialization():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <testns1:TestModel xmlns:testns1="http://www.test1.org"
                   xmlns:testns2="http://www.test2.org"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="http://www.test.com schema.xsd">
        <element1>value1</element1>
        <testns1:element2>value2</testns1:element2>
        <testns2:element3>value3</testns2:element3>
        <testns1:element4 xmlns:testns2="http://www.test22.org">
            <element5>value5</element5>
            <testns2:element6>value6</testns2:element6>
        </testns1:element4>
    </testns1:TestModel>
    '''

    @pb.model(ns='testns1', ns_map={'testns2': 'http://www.test2.org'})
    class TestModel:
        schema = pb.attribute('schemaLocation', ns='xsi')
        element1 = pb.field(ns='')
        element2 = pb.field()
        element3 = pb.field(ns='testns2')
        element5 = pb.wrap('element4', pb.field(ns=''))
        element6 = pb.wrap('element4', pb.field(ns='testns2'), ns_map={'testns2': 'http://www.test22.org'})

    model = pb.from_xml(TestModel, xml, ns_map={
        'testns1': 'http://www.test1.org',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    })

    assert model.schema == 'http://www.test.com schema.xsd'
    assert model.element1 == 'value1'
    assert model.element2 == 'value2'
    assert model.element3 == 'value3'
    assert model.element5 == 'value5'
    assert model.element6 == 'value6'


def test_complex_xml_deserialization():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <envelope xmlns="http://www.test.org"
                  xmlns:doc="http://www.test1.org"
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

            <data:occupations xmlns:data="http://www.test22.org">
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
    </envelope>
    '''

    @pb.model(name='occupation', ns='data', ns_map={'data': 'http://www.test22.org'})
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

        passport_series = pb.wrap('documents/passport', pb.attr('series'))
        passport_number = pb.wrap('documents/passport', pb.attr('number'))

        occupations = pb.wrap(
            'occupations', pb.lst(pb.nested(Occupation)), ns='data', ns_map={'data': 'http://www.test22.org'}
        )

        citizenship = pb.field(default='RU')

    xml = et.fromstring(xml)
    user = pb.from_xml(User, xml)

    assert user.name == 'Alexey'
    assert user.surname == 'Ivanov'
    assert user.age == 26

    assert user.phone == '+79204563539'
    assert user.emails == ['alex@gmail.com', 'alex@mail.ru']

    assert user.passport_series == '3127'
    assert user.passport_number == '836815'

    assert len(user.occupations) == 2

    assert user.occupations[0].title == 'yandex'
    assert user.occupations[0].address == 'Moscow'
    assert user.occupations[0].employees == 8854

    assert user.occupations[1].title == 'skbkontur'
    assert user.occupations[1].address == 'Yekaterinburg'
    assert user.occupations[1].employees == 7742

    assert user.citizenship == 'RU'


def test_indexes_deserialization():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
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

    model = pb.from_xml(TestModel, xml)

    assert model.field1 == 'value1'
    assert model.field2 == 'value2'
    assert model.field3 == 'value3'
    assert model.field4 == 'value4'
    assert model.nested1.field == 'value5'
    assert model.nested2.field == 'value6'


def test_nested_default():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <test_model>
    </test_model>
    '''

    @pb.model(name='nested_model')
    class NestedModel:
        field = pb.field()

    @pb.model(name='test_model')
    class TestModel:
        nested = pb.nested(NestedModel, default=None)

    obj = pb.from_xml(TestModel, xml)
    assert obj.nested is None


def test_field_default():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <test_model>
    </test_model>
    '''

    @pb.model(name='test_model')
    class TestModel:
        field = pb.field(default=None)

    obj = pb.from_xml(TestModel, xml)
    assert obj.field is None


def test_attribute_default():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <test_model>
    </test_model>
    '''

    @pb.model(name='test_model')
    class TestModel:
        attrib = pb.attr(default=None)

    obj = pb.from_xml(TestModel, xml)
    assert obj.attrib is None


def test_private_attributes():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <TestModel>
        <field1>value1</field1>
        <field2>value2</field2>
    </TestModel>
    '''

    @pb.model()
    class TestModel:
        _field1 = pb.field(name='field1')
        __field2 = pb.field(name='field2')

    obj = pb.from_xml(TestModel, xml)

    assert obj._field1 == 'value1'
    assert obj._TestModel__field2 == 'value2'


def test_dict_deserialization():

    @pb.model
    class Nested:
        fields = pb.as_list(pb.field())

    @pb.model
    class TestModel:
        field = pb.field()
        nested = pb.as_list(pb.nested(Nested))

    data = {
        'field': 'value1',
        'nested': [
            {
                'fields': ['value21', 'value22'],
            },
            {
                'fields': ['value31', 'value32'],
            },
        ]
    }

    obj = TestModel(**data)

    assert obj.field == 'value1'
    assert obj.nested == [Nested(fields=['value21', 'value22']), Nested(fields=['value31', 'value32'])]
