import json

from importlib_resources import path as resource_path

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# We don't currently allow untrusted/user-provided XML so this is not a risk
from lxml.etree import Element, fromstring  # nosec

from bas_metadata_library import MetadataRecordConfig as _MetadataRecordConfig, MetadataRecord as _MetadataRecord
from bas_metadata_library.standards.iso_19115_common import Namespaces
from bas_metadata_library.standards.iso_19115_common.root_element import ISOMetadataRecord


class MetadataRecordConfig(_MetadataRecordConfig):
    """
    Overloaded base MetadataRecordConfig class

    Defines the JSON Schema used for this metadata standard
    """

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)

        self.config = kwargs

        with resource_path(
            "bas_metadata_library.standards_schemas.iso_19115_2_v1", "configuration-schema.json"
        ) as configuration_schema_file_path:
            with open(configuration_schema_file_path) as configuration_schema_file:
                configuration_schema_data = json.load(configuration_schema_file)
        self.schema = configuration_schema_data


class MetadataRecord(_MetadataRecord):
    """
    Overloaded base MetadataRecordConfig class

    Defines the root element, and it's sub-elements, for this metadata standard
    """

    def __init__(self, configuration: MetadataRecordConfig = None, record: str = None):
        self.ns = Namespaces()
        self.attributes = {}
        self.record = Element(
            f"{{{self.ns.gmi}}}MI_Metadata",
            attrib={f"{{{self.ns.xsi}}}schemaLocation": self.ns.schema_locations()},
            nsmap=self.ns.nsmap(),
        )
        self.xpath = "/gmi:MI_Metadata"

        if configuration is not None:
            configuration.validate()
            self.attributes = configuration.config

        if record is not None:
            self.record = fromstring(record.encode())

        self.metadata_record = ISOMetadataRecord(record=self.record, attributes=self.attributes, xpath=self.xpath)

    def make_config(self) -> MetadataRecordConfig:
        return MetadataRecordConfig(**self.metadata_record.make_config())

    def make_element(self) -> Element:
        return self.metadata_record.make_element()
