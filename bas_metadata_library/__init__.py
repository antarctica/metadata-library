import json

from typing import Optional

from jsonschema import validate

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# We don't currently allow untrusted/user-provided XML so this is not a risk
from lxml.etree import Element, ElementTree, tostring as element_string  # nosec


# Base classes


class Namespaces(object):
    """
    Gathers all XML namespaces used in a standard

    Provides a way to reference namespaces when constructing elements and declaring namespaces in the root element of
    a XML document.

    This class is intended to be overridden in each metadata standard's module. See existing standards for examples.
    """
    _schema_locations = {}

    def __init__(self):
        self._namespaces = {}

    def nsmap(self) -> dict:
        """
        Indexes namespaces by their prefix

        E.g. {'xlink': 'http://www.w3.org/1999/xlink'}

        :return: dictionary of Namespaces indexed by prefix
        """
        nsmap = {}
        for prefix, namespace in self._namespaces.items():
            nsmap[prefix] = namespace

        return nsmap

    def schema_locations(self) -> str:
        """
        Generates the value for a `xsi:schemaLocation` attribute

        Defines the XML Schema Document (XSD) for each namespace in an XML tree

        E.g. 'xsi:schemaLocation="http://www.w3.org/1999/xlink https://www.w3.org/1999/xlink.xsd"'

        :rtype str
        :return: schema location attribute value
        """
        schema_locations = ''
        for prefix, location in self._schema_locations.items():
            schema_locations = f"{schema_locations} {self._namespaces[prefix]} {location}"

        return schema_locations.lstrip()


class MetadataRecordConfig(object):
    """
    Manages the configuration for a metadata record

    This configuration is used as direct, or computed, values in elements in a metadata record. The configuration is
    first validated against a JSON Schema.
    """
    def __init__(self, **kwargs: dict):
        """
        :type kwargs: dict
        :param kwargs: record configuration
        """
        self.config = kwargs
        self.schema = None

        self.validate()

    def config(self) -> dict:
        """
        Gets the configuration dictionary

        :rtype dict
        :return: configuration dictionary
        """
        return self.config

    def validate(self) -> None:
        """
        Ensures the configuration is valid against the relevant JSON Schema

        Where the configuration is invalid, a relevant exception will be raised.
        """
        if self.schema is not None:
            _config = json.loads(json.dumps(self.config, default=str))
            return validate(instance=_config, schema=self.schema)


class MetadataRecord(object):
    """
    Generates a metadata record using a configuration

    Builds an XML tree as a series of XML elements. Element values and attributes are used directly, or computed, from
    a configuration object.
    """
    def __init__(self, configuration: MetadataRecordConfig):
        """
        :type configuration: MetadataRecordConfig
        :param configuration: Metadata record configuration object
        """
        self.ns = Namespaces()
        self.attributes = configuration.config
        self.record = self.make_element()

    def make_element(self) -> Optional[Element]:
        """
        Builds a metadata record from a root XML element

        Elements are added to this root element defining the contents of the record.

        :return: XML element representing the root of a metadata record
        """
        metadata_record = None
        return metadata_record

    def generate_xml_document(self) -> str:
        """
        Generates an XML document and tree from an XML element defining a record

        The XML document is rendered as a pretty-printed string, with an XML declaration and encoded as UTF-8.

        :rtype str
        :return: XML document string representing a record
        """
        document = ElementTree(self.record)

        return element_string(document, pretty_print=True, xml_declaration=True, encoding="utf-8")


class MetadataRecordElement(object):
    """
    Creates an XML element
    """
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        """
        :type record: MetadataRecord
        :param record: Overall root element of a metadata record
        :type attributes: dict
        :param attributes: all attributes for a metadata record, from a record's configuration
        :type parent_element: Element
        :param parent_element: immediate parent of the current element
        :type element_attributes: dict
        :param element_attributes: attributes for the current element, taken from a record's configuration
        """
        self.ns = Namespaces()
        self.record = record
        self.attributes = attributes
        self.parent_element = parent_element
        self.element_attributes = element_attributes

        if self.parent_element is None:
            self.parent_element = self.record
        if self.element_attributes is None:
            self.element_attributes = self.attributes

    def make_element(self) -> None:
        """
        Builds an XML element
        """
        pass
