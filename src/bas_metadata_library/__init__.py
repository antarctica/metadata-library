import json
import subprocess  # noqa: S404 - see notes in `MetadataRecord.validate` method - nosec
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

from importlib_resources import files as resource_file
from jsonschema import validate
from lxml.etree import (
    Element,
    ElementTree,
    fromstring,
    tostring as element_string,
)  # nosec - see 'lxml` package (bandit)' section in README


class RecordValidationError(Exception):
    """
    Internal error indicating a record has failed schema validation
    """

    pass


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
            json.dump(self.config, file, indent=2)

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

    def generate_xml_document(self) -> bytes:
        """
        Generates an XML document and tree from an XML element defining a record

        The XML document is encoded as a UTF-8 byte string, with pretty-printing and an XML declaration.

        :rtype bytes
        :return: XML document in bytes
        """
        self.record = self.make_element()
        document = ElementTree(self.record)

        return element_string(document, pretty_print=True, xml_declaration=True, encoding="utf-8")

    def validate(self, xsd_path: Path) -> None:
        """
        Validates the contents of a record against a given XSD schema

        The external `xmllint` binary is used to validate records as the `lxml` methods did not easily support relative
        paths for schemas that use imports/includes (which includes the ISO 19115 family).

        Schemas are loaded from an XSD directory within this package using the `importlib.files` method. The current
        record object is written to a temporary directory to easily pass to the `xmllint` binary.

        The `xmllint` binary only returns a 0 exit code if the record validates successfully. Therefore, any other exit
        code can be considered a validation failure, and returned as a `RecordValidationError` exception.

        It is assumed this method will be overridden in concrete implementations of this class. Specifically it's
        assumed the `xsd_path` parameter will be hard coded to a schema suitable for the standard each class implements.

        :type xsd_path: Path
        :param xsd_path: Path relative to `bas_metadata_library.schemas.xsd` to the schema to validate against
        """
        schema_path = resource_file("bas_metadata_library.schemas.xsd").joinpath(xsd_path)

        with TemporaryDirectory() as document_path:
            document_path = Path(document_path).joinpath("record.xml")
            validation_document: MetadataRecord = deepcopy(self)
            with open(document_path, mode="w") as document_file:
                document_data = validation_document.generate_xml_document().decode()
                document_file.write(document_data)

            try:
                # Exempting Bandit/flake8 security issue (using subprocess)
                # Checking for untrusted input is not a concern for this library, rather those implementing
                # this library should ensure it is used in a way that is secure (i.e. it is context dependent).
                #
                # Use `capture_output=True` in future when we can use Python 3.7+
                subprocess.run(  # noqa: S274,S603 - nosec
                    args=["xmllint", "--noout", "--schema", str(schema_path), str(document_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                raise RecordValidationError(f"Record validation failed: {e.stderr.decode()}") from e


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
