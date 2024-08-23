from __future__ import annotations

import json
import subprocess
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from importlib_resources import files as resource_file
from jsonschema import validate
from lxml.etree import (
    Element,
    ElementTree,
    fromstring,
)
from lxml.etree import (
    tostring as element_string,
)


class RecordValidationError(Exception):
    """Internal error indicating a record has failed schema validation."""

    pass


class Namespaces:
    """
    Gathers all XML namespaces used in a standard.

    Provides a way to reference namespaces when constructing elements and declaring namespaces in the root element of
    an XML document.

    This class is intended to be overridden in each metadata standard's module. See existing standards for examples.
    """

    _schema_locations = {}  # noqa: RUF012

    def __init__(self, namespaces: dict | None = None, root_namespace: str | None = None):
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
        dict key (this is a lxml convention). This will create an invalid namespace map for use in XPath queries, this
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
        Generate value for a `xsi:schemaLocation` attribute.

        Defines the XML Schema Document (XSD) for each namespace in an XML tree

        E.g. 'xsi:schemaLocation="http://www.w3.org/1999/xlink https://www.w3.org/1999/xlink.xsd"'
        """
        schema_locations = ""
        for prefix, location in self._schema_locations.items():
            schema_locations = f"{schema_locations} {self._namespaces[prefix]} {location}"

        return schema_locations.lstrip()


class MetadataRecordConfig:
    """
    Represents the configuration for a metadata record.

    The record configuration can either be passed directly as a Python object (dict), when instantiating an instance of
    this class, or by using the `load()` or `loads()` methods to load the configuration from a JSON document.

    The structure and values of this configuration are specified by a JSON schema, and which should be used to validate
    configuration instances using the 'validate()' method. The `schema` property will hold the contents of that JSON
    Schema, the `schema_uri` lists the identity expected/required for that schema.

    It's expected this class will be used a base for standard specific classes, hard-coding the schema that must be
    used for validating a record configuration.
    """

    def __init__(self, **kwargs: dict):
        self.config: dict = kwargs
        self.schema: dict = {}
        self.schema_uri: str = ""

        if "$schema" not in self.config:
            self.config["$schema"] = self.schema_uri

    def validate(self) -> None:
        """
        Ensures the configuration is valid against the relevant JSON Schema.

        The record configuration (a Python dict) is first duplicated to a JSON safe encoding (i.e. Python dates objects
        converted to strings), to allow validation against the JSON Schema.

        Where the configuration is invalid, a relevant exception will be raised.
        """
        if self.schema is not None:
            _config = json.loads(json.dumps(deepcopy(self.config), default=str))
            validate(instance=_config, schema=self.schema)

    def load(self, file: Path) -> None:
        """Loads a record configuration from a JSON encoded file."""
        with file.open(mode="r") as file:
            self.config = json.load(fp=file)

    def loads(self, string: str) -> None:
        """Loads a record configuration from a JSON encoded string."""
        self.config = json.loads(s=string)

    def dump(self, file: Path) -> None:
        """Dumps a record configuration as a JSON encoded file."""
        with file.open(mode="w") as file:
            json.dump(self.config, file, indent=2)

    def dumps(self) -> str:
        """Dumps a record configuration as a JSON encoded string."""
        return json.dumps(self.config, indent=2)


class MetadataRecord:
    """
    Generates a metadata record using a configuration, or a configuration using a record.

    If a configuration is given, an XML tree of elements is built using the configuration object, typically for output
    as a complete record.

    If a record is given, the XML tree is parsed to reverse engineer a configuration object that describes it.

    These processes are designed to be lossless, meaning if a record is made from a configuration object, that record
    should be able to create exactly the same configuration object again without loosing any information.
    """

    def __init__(self, configuration: MetadataRecordConfig = None, record: str | None = None):
        self.ns = Namespaces()
        self.attributes = {}
        self.record = None

        if configuration is not None:
            configuration.validate()
            self.attributes = configuration.config

        if record is not None:
            self.record = fromstring(record.encode())  # noqa: S320 (see '`lxml` package (security)' README section)

    def make_config(self) -> MetadataRecordConfig:
        """
        Builds a metadata configuration object by parsing an existing XML record.

        This method is effectively the reverse of `make_element()` and `generate_xml_document()`.
        """
        return MetadataRecordConfig(**self.attributes)

    def make_element(self) -> Element:
        """
        Builds a metadata record from a root XML element.

        Elements are added to this root element defining the contents of the record.
        """
        return None

    def generate_xml_document(self) -> bytes:
        """
        Generates an XML document and tree from an XML element defining a record.

        The XML document is encoded as a UTF-8 byte string, with pretty-printing and an XML declaration.
        """
        self.record = self.make_element()
        document = ElementTree(self.record)

        return element_string(document, pretty_print=True, xml_declaration=True, encoding="utf-8")

    def validate(self, xsd_path: Path) -> None:
        """
        Validates the contents of a record against a given XSD schema.

        The external `xmllint` binary is used to validate records as the `lxml` methods did not easily support relative
        paths for schemas that use imports/includes (which includes the ISO 19115 family).

        Schemas are loaded from an XSD directory within this package using the `importlib.files` method. The current
        record object is written to a temporary directory to easily pass to the `xmllint` binary.

        The `xmllint` binary only returns a 0 exit code if the record validates successfully. Therefore, any other exit
        code can be considered a validation failure, and returned as a `RecordValidationError` exception.

        It is assumed this method will be overridden in concrete implementations of this class. Specifically it's
        assumed the `xsd_path` parameter will be hard coded to a schema suitable for the standard each class implements.
        """
        schema_path = resource_file("bas_metadata_library.schemas.xsd").joinpath(xsd_path)

        with TemporaryDirectory() as document_path:
            document_path = Path(document_path).joinpath("record.xml")
            validation_document: MetadataRecord = deepcopy(self)
            with document_path.open(mode="w") as document_file:
                document_data = validation_document.generate_xml_document().decode()
                document_file.write(document_data)

            try:
                subprocess.run(
                    args=["xmllint", "--noout", "--schema", str(schema_path), str(document_path)],
                    capture_output=True,
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                msg = f"Record validation failed: {e.stderr.decode()}"
                raise RecordValidationError(msg) from e


class MetadataRecordElement:
    """Create an XML element."""

    def __init__(
        self,
        record: Element,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict | None = None,
        xpath: str | None = None,
    ):
        """
        Initialise.

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
        """Parses an XML element to reverse engineer a partial configuration object."""
        pass

    def make_element(self) -> None:
        """Build an XML element."""
        pass
