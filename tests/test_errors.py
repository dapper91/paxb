import paxb as pb
from paxb import exceptions as exc

import pytest


def test_model_deserialization_error():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <envelope>
        <test_model1/>
    </envelope>
    '''

    @pb.model(name='test_model')
    class TestModel:
        element = pb.field()

    with pytest.raises(exc.DeserializationError, match=r"required element '/envelope/test_model\[1\]' not found"):
        pb.from_xml(TestModel, xml, envelope='envelope')

    with pytest.raises(exc.DeserializationError, match=r"required element '/envelope/test_model\[1\]' not found"):
        pb.from_xml(TestModel, xml, envelope='envelope')


def test_field_deserialization_error():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <test_model>
        <element1/>
    </test_model>
    '''

    @pb.model(name='test_model')
    class TestModel:
        element = pb.field()

    with pytest.raises(exc.DeserializationError, match=r"required element '/test_model\[1\]/element\[1\]' not found"):
        pb.from_xml(TestModel, xml)


def test_attribute_deserialization_error():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <test_model attribute1="value1"/>
    '''

    @pb.model(name='test_model')
    class TestModel:
        attribute = pb.attr()

    with pytest.raises(exc.DeserializationError, match=r"required attribute '/test_model\[1\]/attribute' not found"):
        pb.from_xml(TestModel, xml)


def test_wrapper_deserialization_error():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <test_model>
        <wrapper>
            <wrapper>
                <element1>value</element1>
            </wrapper>
        </wrapper>
    </test_model>
    '''

    @pb.model(name='test_model')
    class TestModel:
        element = pb.wrap('wrapper', pb.wrap('wrapper', pb.field()))

    with pytest.raises(
        exc.DeserializationError,
        match=r"required element '/test_model\[1\]/wrapper\[1\]/wrapper\[1\]/element\[1\]' not found"
    ):
        pb.from_xml(TestModel, xml)

    @pb.model(name='test_model')
    class TestModel:
        element = pb.wrap('wrapper1', pb.wrap('wrapper', pb.field()))

    with pytest.raises(
        exc.DeserializationError,
        match=r"required element '/test_model\[1\]/wrapper1\[1\]' not found"
    ):
        pb.from_xml(TestModel, xml)


def test_nested_deserialization_error():
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <test_model>
        <nested_model/>
    </test_model>
    '''

    @pb.model(name='nested_model1')
    class NestedModel:
        pass

    @pb.model(name='test_model')
    class TestModel:
        element = pb.nested(NestedModel)

    with pytest.raises(
        exc.DeserializationError,
        match=r"required element '/test_model\[1\]/nested_model1\[1\]' not found"
    ):
        pb.from_xml(TestModel, xml)
