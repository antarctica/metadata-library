import json

from typing import Optional
from pathlib import Path

from jsonschema import validate

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# We don't currently allow untrusted/user-provided XML so this is not a risk
from lxml.etree import Element, ElementTree, tostring as element_string, fromstring  # nosec


# Base classes


class Namespaces(object):
    """
    Gathers all XML namespaces used in a standard

    Provides a way to reference namespaces when constructing elements and declaring namespaces in the root element of
    a XML document.

    This class is intended to be overridden in each metadata standard's module. See existing standards for examples.
    """

    _schema_locations = {}

    def __init__(self, namespaces: dict = None, root_namespace: str = None):
        """
        Root namespace support.

        The root namespace parameter is optional for use in standards that require a default namespace.

        When encoding data, this has the effect of not including a prefix in elements when encoded (e.g. `foo` instead
        of `ns:foo`). When decoding data, this behaviour must be suppressed using the relevant override parameter in
        the `nsmap()` method.

        @type namespaces: dict
        @param namespaces: dictionary of namespaces to add
        @type root_namespace: str
        @param root_namespace: optional namespace to use as unprefixed
        """
        self._namespaces = {}
        self.root_namespace = root_namespace
        if namespaces is not None:
            self._namespaces = {**self._namespaces, **namespaces}

    def nsmap(self, suppress_root_namespace: bool = False) -> dict:
        """
        Create a namespace map.

        Indexes namespaces by their prefix.

        E.g. {'xlink': 'http://www.w3.org/1999/xlink'}

        When a root namespace is set, a default namespace will be set by using the `None` constant for the relevant
        dict key (this is an lxml convention). This will create an invalid namespace map for use in XPath queries, this
        can be overcome using the `suppress_root_namespace` parameter, which will create a 'regular' map.

        :type suppress_root_namespace: bool
        :param suppress_root_namespace: When true, respects a root prefix as a default if set
        :return: dictionary of Namespaces indexed by prefix
        """
        nsmap = {}
        for prefix, namespace in self._namespaces.items():
            if hasattr(self, "root_namespace") and namespace == self.root_namespace and not suppress_root_namespace:
                nsmap[None] = namespace
                continue

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
        schema_locations = ""
        for prefix, location in self._schema_locations.items():
            schema_locations = f"{schema_locations} {self._namespaces[prefix]} {location}"

        return schema_locations.lstrip()


class MetadataRecordConfig(object):
    """
    Represents the configuration for a metadata record

    The record configuration can either be passed directly as a Python object (dict), when instantiating an instance of
    this class, or by using the `load()` or `loads()` methods to load the configuration from a JSON document.

    The structure and values of this configuration are specified by a JSON schema, and which should be used to validate
    configuration instances using the 'validate()' method.
    """

    def __init__(self, **kwargs: dict):
        """
        :type kwargs: dict
        :param kwargs: record configuration
        """
        self.config = kwargs
        self.schema = None

    def validate(self) -> None:
        """
        Ensures the configuration is valid against the relevant JSON Schema

        Where the configuration is invalid, a relevant exception will be raised.
        """
        if self.schema is not None:
            _config = json.loads(json.dumps(self.config, default=str))
            return validate(instance=_config, schema=self.schema)

    def load(self, file: Path) -> None:
        """
        Loads a record configuration from a JSON encoded file

        :type file: Path
        :param file: path to the JSON encoded file to load from
        """
        with open(str(file), mode="r") as file:
            self.config = json.load(fp=file)

    def loads(self, string: str) -> None:
        """
        Loads a record configuration from a JSON encoded string

        :type string: str
        :param string: JSON encoded string to load from
        """
        self.config = json.loads(s=string)

    def dump(self, file: Path) -> None:
        """
        Dumps a record configuration as a JSON encoded file

        The path to the file to read from should be expressed using a Python pathlib.Path object.

        :type file: Path
        :param file: path at which to create a JSON encoded file
        """
        with open(str(file), mode="w") as file:
            json.dump(self.config, file)

    def dumps(self) -> str:
        """
        Dumps a record configuration as a JSON encoded string

        :rtype str
        :returns record configuration as a JSON encoded string
        """
        return json.dumps(self.config, indent=2)


class MetadataRecord(object):
    """
    Generates a metadata record using a configuration, or a configuration using a record

    If a configuration is given, an XML tree of elements is built using the configuration object, typically for output
    as a complete record.

    If a record is given, the XML tree is parsed to reverse engineer a configuration object that describes it.

    These processes are designed to be lossless, meaning if a record is made from a configuration object, that record
    should be able to create exactly the same configuration object again without loosing any information.
    """

    def __init__(self, configuration: MetadataRecordConfig = None, record: str = None):
        """
        :type configuration: MetadataRecordConfig
        :param configuration: Metadata record configuration object
        :type record: str
        :param record: XML document string representing a record
        """
        self.ns = Namespaces()
        self.attributes = {}
        self.record = None

        if configuration is not None:
            configuration.validate()
            self.attributes = configuration.config

        if record is not None:
            self.record = fromstring(record.encode())

    def make_config(self) -> MetadataRecordConfig:
        """
        Builds a metadata configuration object by parsing an existing XML record

        This method is effectively the reverse of make_element() and generate_xml_document().

        :rtype: MetadataRecordConfig
        :return: Metadata record configuration object
        """
        return MetadataRecordConfig(**self.attributes)

    def make_element(self) -> Optional[Element]:
        """
        Builds a metadata record from a root XML element

        Elements are added to this root element defining the contents of the record.

        :rtype: Element
        :return: XML element representing the root of a metadata record
        """
        metadata_record = None
        return metadata_record

    def generate_xml_document(self, xml_declaration: bool = True) -> bytes:
        """
        Generates an XML document and tree from an XML element defining a record

        The XML document is encoded as a UTF-8 byte string, with pretty-printing, and by default, an XML declaration.

        :type xml_declaration: bool
        :param xml_declaration: Whether to include an XML declaration, defaults to True

        :rtype bytes
        :return: XML document in bytes
        """
        self.record = self.make_element()
        document = ElementTree(self.record)

        return element_string(document, pretty_print=True, xml_declaration=xml_declaration, encoding="utf-8")


class MetadataRecordElement(object):
    """
    Creates an XML element
    """

    def __init__(
        self,
        record: Element,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        xpath: str = None,
    ):
        """
        :type record: Element
        :param record: overall root element of a metadata record
        :type attributes: dict
        :param attributes: all attributes for a metadata record, from a record's configuration
        :type parent_element: Element
        :param parent_element: immediate parent of the current element
        :type element_attributes: dict
        :param element_attributes: attributes for the current element, taken from a record's configuration
        :type xpath: str
        :param xpath: Absolute XML XPath selecting the value of the element created
        """
        self.ns = Namespaces()
        self.record = record
        self.attributes = attributes
        self.parent_element = parent_element
        self.element_attributes = element_attributes
        self.xpath = xpath

        if self.parent_element is None:
            self.parent_element = self.record
        if self.element_attributes is None:
            self.element_attributes = self.attributes

    def make_config(self) -> None:
        """
        Parses an XML element to reverse engineer a partial configuration object
        """
        pass

    def make_element(self) -> None:
        """
        Builds an XML element
        """
        pass
