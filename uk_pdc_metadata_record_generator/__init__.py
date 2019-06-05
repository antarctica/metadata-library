import simplejson as json

from datetime import datetime, date
from pathlib import Path
from typing import Optional, Union

from jsonschema import validate

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# We don't currently allow untrusted/user-provided XML so this is not a risk
from lxml.etree import Element, ElementTree, tostring as element_string  # nosec


class Utils(object):
    @staticmethod
    def get_epsg_code(candidate_code: str) -> Optional[str]:
        if candidate_code.startswith('urn:ogc:def:crs:EPSG'):
            code_parts = candidate_code.split('::')
            return code_parts[-1]

        return None

    @staticmethod
    def format_date_string(date_datetime: Union[date, datetime]) -> str:
        return date_datetime.isoformat()


# Base classes


class Namespaces(object):
    _schema_locations = {}

    def __init__(self):
        self._namespaces = {}

    def nsmap(self) -> dict:
        nsmap = {}
        for prefix, namespace in self._namespaces.items():
            nsmap[prefix] = namespace

        return nsmap

    def schema_locations(self) -> str:
        schema_locations = ''
        for prefix, location in self._schema_locations.items():
            schema_locations = f"{schema_locations} {self._namespaces[prefix]} {location}"

        return schema_locations.lstrip()


class MetadataRecordConfig(object):
    def __init__(self, **kwargs: dict):
        self.config = kwargs
        self.schema = None
        self.schema_path = Path('resources/schemas/metadata-record-schema.json')

        self.load_schema()
        self.validate()

    def config(self) -> dict:
        return self.config

    def load_schema(self):
        with open(self.schema_path) as schema_file:
            self.schema = json.load(schema_file)

    def validate(self):
        _config = json.loads(json.dumps(self.config, default=str))
        return validate(instance=_config, schema=self.schema)


class MetadataRecord(object):
    def __init__(self, configuration: MetadataRecordConfig):
        self.ns = Namespaces()
        self.attributes = configuration.config
        self.record = self.make_element()

    def make_element(self) -> Optional[Element]:
        metadata_record = None
        return metadata_record

    def generate_xml_document(self) -> str:
        document = ElementTree(self.record)

        return element_string(document, pretty_print=True, xml_declaration=True, encoding="utf-8")


class MetadataRecordElement(object):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        self.ns = Namespaces()
        self.record = record
        self.attributes = attributes
        self.parent_element = parent_element
        self.element_attributes = element_attributes

        if self.parent_element is None:
            self.parent_element = self.record
        if self.element_attributes is None:
            self.element_attributes = self.attributes

    def make_element(self):
        pass
