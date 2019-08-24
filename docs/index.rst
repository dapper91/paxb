.. paxb documentation master file, created by
   sphinx-quickstart on Wed Aug 14 22:29:04 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

paxb: Python Architecture for XML Binding
=========================================

.. image:: https://travis-ci.org/dapper91/paxb.svg?branch=master
    :target: https://travis-ci.org/dapper91/paxb
    :alt: Build status
.. image:: https://img.shields.io/pypi/l/paxb.svg
    :target: https://pypi.org/project/paxb
    :alt: License
.. image:: https://img.shields.io/pypi/pyversions/paxb.svg
    :target: https://pypi.org/project/paxb
    :alt: Supported Python versions


``paxb`` is a library that provides an API for mapping between XML documents and Python objects.

``paxb`` library implements the following functionality:

- :doc:`Deserialize <paxb/deserialization>` XML documents to Python objects
- Validate deserialized fields
- Access and update Python object fields
- :doc:`Serialize <paxb/serialization>` Python objects to XML documents

``paxb`` provides an efficient way of mapping between an XML document and a Python object. Using paxb
developers can write less boilerplate code emphasizing on application domain logic.

As soon as paxb is based on `attrs <https://www.attrs.org/en/stable/index.html>`_ library ``paxb`` and attrs
API can be :doc:`mixed <paxb/attrs>` together.


Requirements
------------

- `attrs <https://www.attrs.org/en/stable/index.html>`_


The User Guide
--------------

.. toctree::
   :maxdepth: 2

   paxb/installation
   paxb/quickstart
   paxb/binding
   paxb/serialization
   paxb/deserialization
   paxb/namespaces
   paxb/errors
   paxb/attrs


The API Documentation
---------------------

.. toctree::
   :maxdepth: 2

   paxb/api