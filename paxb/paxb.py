import xml.etree.ElementTree as et

import attr
from . import encoder as default_encoder
from . import exceptions as exc
from . import mappers


def model(maybe_cls=None, name=None, ns=None, ns_map=None, order=None, **kwargs):
    """
    Decorator `@model` maps a class to an XML element. The decorator uses a class
    name as a default element name. The default name can be changed using the decorator
    attribute `name`. The `ns` attribute defines a namespace of the element. By default
    class fields are serialized in in-class definition order. The order can be changed
    using `order` attribute.

    Internally the decorator adds `dunder <https://wiki.python.org/moin/DunderAlias>`_\
    attributes.

    :param maybe_cls: decorated class if it is used as `@model` or `None` if it is used as `@model()`
    :param name: model name. If `None` class name will be used
    :param ns: element namespace. If `None` empty namespace will be used or if the model
               is a nested one - namespace is inherited from the parent model
    :param ns_map: mapping from namespace prefix to full name. If the model is a nested one merged with the parent map
    :param order: class fields serialization order. If `None` in-class definition order is used
    :param kwargs: arguments that will be passed to `attr.ib`
    """

    def decorator(cls):
        cls = attr.attrs(cls, **kwargs)
        cls.__paxb_attrs__ = (name, ns, ns_map, order)

        return cls

    # maybe_cls's type depends on the usage of the decorator.  It's a class
    # if it's used as `@model` but ``None`` if used as `@model()`.
    if maybe_cls is None:
        return decorator
    else:
        return decorator(maybe_cls)


def attribute(name=None, **kwargs):
    """
    Function `attribute` maps a class field to an XML attribute. The field name is used
    as a default attribute name. The default name can be changed using the parameter `name`.

    :param name: attribute name. If `None` field name will be used
    :param kwargs: arguments that will be passed to `attr.ib`
    """

    has_default = 'default' in kwargs or 'factory' in kwargs
    required = not has_default

    attrib = attr.attrib(**kwargs)
    attrib.metadata['paxb.mapper'] = mappers.AttributeXmlMapper(name, required)

    return attrib


def field(name=None, ns=None, ns_map=None, idx=None, **kwargs):
    """
    Function `field` maps a class field to an XML element. The field name is used
    as a default element name. The default name can be changed using parameter `name`.
    The `ns` parameter defines the namespace of the element.

    Internally the decorator adds some metainformation to `attrib.metadata`.

    :param name: element name. If `None` field name will be used
    :param ns: element namespace. If `None` the namespace is inherited from the containing model
    :param ns_map: mapping from namespace prefix to full name. Merged with the parent one
    :param idx: element index in the xml document. If `None` 1 is used
    :param kwargs: arguments that will be passed to `attr.ib`
    """

    has_default = 'default' in kwargs or 'factory' in kwargs
    required = not has_default

    attrib = attr.attrib(**kwargs)
    attrib.metadata['paxb.mapper'] = mappers.FieldXmlMapper(name, ns, ns_map, idx, required)

    return attrib


def nested(cls, name=None, ns=None, ns_map=None, idx=None, **kwargs):
    """
    Function `nested` maps a class to an XML element. `nested` is used when a `@model`
    decorated class contains another one as a field.

    :param cls: nested object class. `cls` must be an instance of `@model` decorated class
    :param name: element name. If `None` decorator name attribute will be used
    :param ns: element namespace. If `None` decorator ns attribute will be used
    :param ns_map: mapping from namespace prefix to full name. Merged with the parent one
    :param idx: element index in the xml document. If `None` 1 is used
    :param kwargs: arguments that will be passed to `attr.ib`
    """

    if not isinstance(cls, type):
        raise TypeError("Passed object must be a class")

    required = 'default' not in kwargs

    attrib = attr.attrib(**kwargs)
    attrib.metadata['paxb.mapper'] = mappers.ModelXmlMapper(cls, name, ns, ns_map, idx, required)

    return attrib


def wrapper(path, wrapped, ns=None, ns_map=None, idx=None):
    """
    Function `wrapper` is used to map a class field to an XML element that is contained by a subelement.

    :param path: full path to the `wrapped` element. Element names are separated by slashes
    :param wrapped: the wrapped element
    :param ns: element namespace. If `None` the namespace is inherited from the containing model
    :param ns_map: mapping from namespace prefix to full name. Merged with the parent one
    :param idx: element index in the xml document. If `None` 1 is used
    """

    wrapped.metadata['paxb.mapper'] = mappers.WrapperXmlMapper(path, wrapped.metadata['paxb.mapper'], ns, ns_map, idx)

    return wrapped


def as_list(wrapped):
    """
    Function `as_list` maps a class list field to an XML element list. Wrapped element
    can be field or nested model.

    :param wrapped: list element type
    """

    wrapped.metadata['paxb.mapper'] = mappers.ListXmlWrapper(wrapped.metadata['paxb.mapper'])

    return wrapped


def from_xml(cls, xml, envelope=None, name=None, ns=None, ns_map=None, required=True):
    """
    Deserializes xml string to object of `cls` class. `cls` must be a `@model` decorated class.

    :param cls: class the deserialized object is instance of
    :param xml: xml string or xml tree to deserialize the object from
    :param envelope: root tag where the serializing object will be looked for
    :param name: name of the serialized object element. If `None` annotation argument will be used
    :param ns: namespace of the serialized object element. If `None` annotation argument will be used
    :param ns_map: mapping from namespace prefix to full name.
    :param required: is the serialized object element required. If element not found and `required` is `True`
           `DeserializationError` will be raised otherwise `None` is returned
    :return: deserialized object
    """

    if isinstance(xml, str):
        root = et.Element(None)
        root.append(et.fromstring(xml))
    else:
        root = xml

    if envelope:
        root = root.find(envelope, ns_map)
        if root is None:
            raise exc.DeserializationError("required element '{}' not found".format(envelope))
        full_path = tuple(envelope.split('/'))
    else:
        full_path = ()

    return mappers.ModelXmlMapper(cls, name, ns, ns_map, required=required).obj(root, full_path=full_path)


def to_xml(obj, envelope=None, name=None, ns=None, ns_map=None, encoder=default_encoder, **kwargs):
    """
    Serializes a paxb class object to an xml string. Object must be an instance of a `@model` decorated class.

    :param obj: object to be serialized
    :param envelope: root tag name the serialized object element will be added inside.
                     If `None` object element will be a root
    :param name: name of the serialized object element. If `None` annotation argument will be used
    :param ns: namespace of the serialized object element. If `None` annotation argument will be used
    :param ns_map: mapping from namespace prefix to full name.
    :param encoder: value encoder. If `None` `paxb.encoder` is used
    :param kwargs: arguments that will be passed to `ElementTree.tostring` method
    :return: serialized object xml string
    """

    if ns_map:
        for alias, uri in ns_map.items():
            et.register_namespace(alias, uri)

    root = et.Element(envelope)
    obj = mappers.ModelXmlMapper(obj.__class__, name, ns, ns_map).xml(obj, root, encoder=encoder)

    if envelope is None:
        root = obj

    if root is not None:
        return et.tostring(root, **kwargs)
    else:
        return None
