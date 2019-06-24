from pathlib import Path

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# We don't currently allow untrusted/user-provided XML so this is not a risk
from lxml.etree import Element, SubElement  # nosec

from uk_pdc_metadata_record_generator import Namespaces as _Namespaces, MetadataRecordConfig as _MetadataRecordConfig, \
    MetadataRecord as _MetadataRecord, MetadataRecordElement as _MetadataRecordElement


# Base classes


class MetadataRecordElement(_MetadataRecordElement):
    def __init__(
        self,
        record: _MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.ns = Namespaces()


class Namespaces(_Namespaces):
    xlink = 'http://www.w3.org/1999/xlink'
    xsi = 'http://www.w3.org/2001/XMLSchema-instance'

    _schema_locations = {}

    def __init__(self):
        self._namespaces = {
            'xlink': self.xlink,
            'xsi': self.xsi
        }


class MetadataRecordConfig(_MetadataRecordConfig):
    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)

        self.config = kwargs
        self.schema = None
        self.schema_path = Path('tests/resources/schemas/standards/test-standard/test-standard-record-schema.json')

        self.load_schema()
        self.validate()


class MetadataRecord(_MetadataRecord):
    def __init__(self, configuration: MetadataRecordConfig):
        self.ns = Namespaces()
        self.attributes = configuration.config
        self.record = self.make_element()

    def make_element(self) -> Element:
        metadata_record = Element(
            f"MetadataRecord",
            attrib={f"{{{ self.ns.xsi }}}schemaLocation": self.ns.schema_locations()},
            nsmap=self.ns.nsmap()
        )

        resource = ResourceElement(
            record=metadata_record,
            attributes=self.attributes,
            parent_element=metadata_record,
            element_attributes=self.attributes['resource']
        )
        resource.make_element()

        return metadata_record


# Element Classes


class ResourceElement(MetadataRecordElement):
    def make_element(self):
        resource_element = SubElement(self.parent_element, f"Resource")

        title = TitleElement(
            record=self.record,
            attributes=self.attributes,
            parent_element=resource_element,
            element_attributes=self.element_attributes['title']
        )
        title.make_element()


class TitleElement(MetadataRecordElement):
    def make_element(self):
        attributes = {}

        if 'href' in self.element_attributes:
            attributes[f"{{{self.ns.xlink}}}href"] = self.element_attributes['href']
            attributes[f"{{{self.ns.xlink}}}actuate"] = 'onRequest'
        if 'title' in self.element_attributes:
            attributes[f"{{{self.ns.xlink}}}title"] = self.element_attributes['title']

        title = SubElement(self.parent_element, f"Title", attrib=attributes)
        if 'value' in self.element_attributes:
            title.text = self.element_attributes['value']
