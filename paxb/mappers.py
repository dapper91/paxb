"""
The module implements mappers and mapping routine functions. Mapper is a class that implements logic
for mapping xml elements to python object fields and vise versa.
"""

import abc
import xml.etree.ElementTree as et

import attr

from . import exceptions as exc
from . import encoder as default_encoder


def get_attrs(cls):
    """
    Returns all paxb attributes of a class decorated with `@model` decorator.

    :param cls: `@model` decorated class
    :return: paxb class attributes
    """

    if not isinstance(cls, type):
        raise TypeError("Passed object must be a class")

    attrs = getattr(cls, '__paxb_attrs__', None)
    if attrs is None:
        raise TypeError("{cls!r} is not a paxb model-decorated class.".format(cls=cls))

    return attrs


def tag_name(ns, name, idx=None):
    tag = '{}:{}'.format(ns, name) if ns else name

    if idx is not None:
        tag += '[{}]'.format(idx)

    return tag


def qname(ns, name):
    return '{{{}}}{}'.format(ns, name) if ns else name


def drop_nones(d):
    """
    Drop none values from the dict
    """
    return {k: v for k, v in d.items() if v is not None}


def first(*args):
    """
    Returns first not None argument.
    """

    for item in args:
        if item is not None:
            return item


def merge_dicts(*dicts):
    """
    Merges dicts in reversed order.

    :param dicts: dicts to be merged
    :return: merged dict
    """

    result = {}
    for d in reversed(dicts):
        if d:
            result.update(d)

    return result


class Mapper(abc.ABC):
    """
    Base mapper class. All mappers are inherited from it.
    """

    @abc.abstractmethod
    def xml(self, obj, root, name=None, ns=None, ns_map=None, idx=None, encoder=default_encoder):
        """
        Serialization method.

        :param obj: object to be serialized
        :param root: root element the object will be added inside
        :param name: element name
        :param ns: element namespace
        :param ns_map: mapping from namespace prefix to full name
        :param idx: element index in the xml tree
        :param encoder: value encoder
        :return: added xml tree node
        """

    @abc.abstractmethod
    def obj(self, xml, name=None, ns=None, ns_map=None, idx=None, full_path=()):
        """
        Deserialization method.

        :param xml: xml tree to deserialize the object from
        :param name: element name
        :param ns: element namespace
        :param ns_map: mapping from namespace prefix to full name
        :param idx: element index in the xml tree
        :param full_path: full path to the current element
        :return: deserialized object
        """


# TODO: implement attribute namespaces
class AttributeXmlMapper(Mapper):
    """
    Attribute to XMl mapper. Implements methods for mapping an xml attribute to a python object and vise versa.
    """

    def __init__(self, name=None, required=True):
        self.name = name
        self.required = required

    def xml(self, obj, root, name=None, ns=None, ns_map=None, _=None, encoder=default_encoder):
        name = first(self.name, name)

        if obj is None:
            if self.required:
                raise exc.SerializationError("required attribute '{}' is not set".format(name))
            else:
                return None

        attrib = encoder.encode(obj)
        root.attrib[name] = attrib

        return attrib

    def obj(self, xml, name=None, ns=None, ns_map=None, _=None, full_path=()):
        name = first(self.name, name)

        attribute = xml.get(name)
        if attribute is None and self.required:
            raise exc.DeserializationError("required attribute '/{}' not found".format('/'.join(full_path + (name, ))))

        return attribute


class FieldXmlMapper(Mapper):
    """
    XML element mapper. Implements methods for mapping an xml element text data to a python object and vise versa.
    """

    def __init__(self, name, ns=None, ns_map=None, idx=None, required=True):
        self.name = name
        self.ns = ns
        self.ns_map = ns_map
        self.idx = idx
        self.required = required

    def xml(self, obj, root, name=None, ns=None, ns_map=None, _=None, encoder=default_encoder):
        name = first(self.name, name)
        ns = first(self.ns, ns)
        ns_map = merge_dicts(self.ns_map, ns_map)

        if obj is None:
            if self.required:
                raise exc.SerializationError("required element '{}' is not set".format(name))
            else:
                return None

        element = et.SubElement(root, qname(ns=ns_map.get(ns), name=name))
        element.text = encoder.encode(obj)

        return element

    def obj(self, xml, name=None, ns=None, ns_map=None, idx=None, full_path=()):
        name = first(self.name, name)
        ns = first(self.ns, ns)
        ns_map = merge_dicts(self.ns_map, ns_map)
        idx = first(idx, self.idx, 1)

        tag = tag_name(ns=ns, name=name, idx=idx)

        xml = xml.find(tag, ns_map)
        if xml is None or xml.text is None:
            if self.required:
                raise exc.DeserializationError("required element '/{}' not found".format('/'.join(full_path + (tag, ))))
            return None

        return xml.text


class WrapperXmlMapper(Mapper):
    """
    Wrapper mapper.
    """

    def __init__(self, path, wrapped, ns, ns_map, idx=None):
        self.ns = ns
        self.ns_map = ns_map
        self.name, *tail = path.split('/', 1)
        self.idx = idx
        self.required = wrapped.required

        if tail:
            self.wrapped = type(self)(tail[0], wrapped, ns, ns_map)
        else:
            self.wrapped = wrapped

    def xml(self, obj, root, name=None, ns=None, ns_map=None, idx=None, encoder=default_encoder):
        ns = first(self.ns, ns)
        ns_map = merge_dicts(self.ns_map, ns_map)
        idx = first(idx, self.idx, 1)

        existing_elements = root.findall(qname(ns=ns_map.get(ns), name=self.name), ns_map)
        if idx > len(existing_elements) + 1:
            raise exc.SerializationError(
                "element {} at index {} is going to be serialized, but the previous one is omitted".format(name, idx)
            )
        if idx == len(existing_elements) + 1:
            element = et.Element(qname(ns=ns_map.get(ns), name=self.name))
            new_element = True
        else:
            element = existing_elements[idx-1]
            new_element = False

        serialized = self.wrapped.xml(obj, element, name, ns, ns_map, encoder=encoder)
        if serialized is None:
            return None

        if new_element:
            root.append(element)

        return element

    def obj(self, xml, name=None, ns=None, ns_map=None, idx=None, full_path=()):
        ns = first(self.ns, ns)
        ns_map = merge_dicts(self.ns_map, ns_map)
        idx = first(idx, self.idx, 1)

        tag = tag_name(ns=ns, name=self.name, idx=idx)

        xml = xml.find(tag, ns_map)
        if xml is None:
            if self.wrapped.required:
                raise exc.DeserializationError("required element '/{}' not found".format('/'.join(full_path + (tag, ))))
            return None

        return self.wrapped.obj(xml, name, ns, ns_map, full_path=full_path + (tag,))


class ListXmlWrapper(Mapper):
    """
    Element list to XMl mapper. Implements methods for mapping a list of elements to a python list and vise versa.
    """

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.required = wrapped.required

    def xml(self, obj, root, name=None, ns=None, ns_map=None, _=None, encoder=default_encoder):
        name = first(self.wrapped.name, name)
        ns = first(self.wrapped.ns, ns)
        ns_map = merge_dicts(self.wrapped.ns_map, ns_map)

        children = []
        for idx, item in enumerate(obj or []):
            children.append(self.wrapped.xml(item, root, name, ns, ns_map, idx+1, encoder=encoder))

        return children or None

    def obj(self, xml, name=None, ns=None, ns_map=None, _=None, full_path=()):
        name = first(self.wrapped.name, name)
        ns = first(self.wrapped.ns, ns)
        ns_map = merge_dicts(self.wrapped.ns_map, ns_map)

        result = []
        for idx, e in enumerate(xml.iterfind(tag_name(ns=ns, name=name), ns_map)):
            result.append(self.wrapped.obj(xml, name, ns, ns_map, idx+1, full_path=full_path))

        return result


class ModelXmlMapper(Mapper):
    """
    Model to XMl mapper. Implements methods for mapping an xml element to a python object and vise versa.
    """

    def __init__(self, cls, name=None, ns=None, ns_map=None, idx=None, required=True):
        model_name, model_ns, model_ns_map, self.order = get_attrs(cls)
        self.cls = cls
        self.name = first(name, model_name, cls.__name__)
        self.ns = first(ns, model_ns)
        self.ns_map = merge_dicts(ns_map, model_ns_map)
        self.idx = idx
        self.required = required

    def xml(self, obj, root, name=None, ns=None, ns_map=None, _=None, encoder=default_encoder):
        name = first(self.name, name)
        ns = first(self.ns, ns)
        ns_map = merge_dicts(self.ns_map, ns_map)

        if obj is None:
            if self.required:
                raise exc.SerializationError("required element '{}' is not set".format(name))
            else:
                return None

        element = et.Element(qname(ns=ns_map.get(ns), name=name))

        serialized_fields = []
        for field in attr.fields(self.cls):
            mapper = field.metadata.get('paxb.mapper')
            if mapper:
                serialized = mapper.xml(getattr(obj, field.name), element, field.name, ns, ns_map, encoder=encoder)
                if serialized is not None:
                    serialized_fields.append(serialized)

        if not serialized_fields:
            return None
        else:
            root.append(element)
            return element

    def obj(self, xml, name=None, ns=None, ns_map=None, idx=None, full_path=()):
        name = first(self.name, name)
        ns = first(self.ns, ns)
        ns_map = merge_dicts(self.ns_map, ns_map)
        idx = first(idx, self.idx, 1)

        tag = tag_name(ns=ns, name=name, idx=idx)

        xml = xml.find(tag, ns_map)
        if xml is None:
            if self.required:
                raise exc.DeserializationError("required element '/{}' not found".format('/'.join(full_path + (tag, ))))
            return None

        cls_kwargs = {}

        for attr_field in attr.fields(self.cls):
            mapper = attr_field.metadata.get('paxb.mapper')
            if mapper:
                cls_kwargs[attr_field.name] = mapper.obj(xml, attr_field.name, ns, ns_map, full_path=full_path + (tag,))

        cls_kwargs = drop_nones(cls_kwargs)

        return self.cls(**cls_kwargs)
