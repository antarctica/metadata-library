from __future__ import annotations

import json
from pathlib import Path

from lxml.etree import Element, SubElement, fromstring

from bas_metadata_library import (
    MetadataRecord as _MetadataRecord,
)
from bas_metadata_library import (
    MetadataRecordConfig as _MetadataRecordConfig,
)
from bas_metadata_library import (
    MetadataRecordElement as _MetadataRecordElement,
)
from bas_metadata_library import (
    Namespaces as _Namespaces,
)

# Base classes


class MetadataRecordElement(_MetadataRecordElement):
    def __init__(
        self, record: _MetadataRecord, attributes: dict, parent_element: Element = None, element_attributes: dict | None = None
    ):
        super().__init__(
            record=record, attributes=attributes, parent_element=parent_element, element_attributes=element_attributes
        )
        self.ns = Namespaces()


class Namespaces(_Namespaces):
    xlink = "http://www.w3.org/1999/xlink"
    xsi = "http://www.w3.org/2001/XMLSchema-instance"

    _schema_locations = {}  # noqa: RUF012

    def __init__(self):
        self._namespaces = {"xlink": self.xlink, "xsi": self.xsi}


class MetadataRecordConfig(_MetadataRecordConfig):
    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)

        self.config = kwargs

        # Workaround for #179
        schema_path = Path().resolve().joinpath("tests/schemas/test_standard_v1.json")
        if not schema_path.exists():
            schema_path = Path().resolve().parent.joinpath("schemas/test_standard_v1.json")

        with schema_path.open() as schema_file:
            schema_data = json.load(schema_file)
        self.schema = schema_data

        # Workaround - will be addressed in #149
        self.schema_uri = schema_data["$id"]
        self.config = {"$schema": self.schema_uri, **kwargs}


class MetadataRecord(_MetadataRecord):
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
        resource = ResourceElement(record=self.record, attributes=self.attributes)
        _resource = resource.make_config()
        self.attributes["resource"] = _resource

        return MetadataRecordConfig(**self.attributes)

    def make_element(self) -> Element:
        metadata_record = Element(
            "MetadataRecord",
            attrib={f"{{{ self.ns.xsi }}}schemaLocation": self.ns.schema_locations()},
            nsmap=self.ns.nsmap(),
        )

        resource = ResourceElement(
            record=metadata_record,
            attributes=self.attributes,
            parent_element=metadata_record,
            element_attributes=self.attributes["resource"],
        )
        resource.make_element()

        return metadata_record


# Element Classes


class ResourceElement(MetadataRecordElement):
    def make_config(self) -> dict:
        title = TitleElement(
            record=self.record,
            attributes=self.attributes,
        )
        _title = title.make_config()

        return {"title": _title}

    def make_element(self):
        resource_element = SubElement(self.parent_element, "Resource")

        title = TitleElement(
            record=self.record,
            attributes=self.attributes,
            parent_element=resource_element,
            element_attributes=self.element_attributes["title"],
        )
        title.make_element()


class TitleElement(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}
        base_xpath = "/MetadataRecord/Resource/Title"

        value = self.record.xpath(f"{base_xpath}/text()", namespaces=self.ns.nsmap())
        if len(value) == 1:
            _["value"] = value[0]

        href = self.record.xpath(f"{base_xpath}/@xlink:href", namespaces=self.ns.nsmap())
        if len(href) == 1:
            _["href"] = href[0]

        title = self.record.xpath(f"{base_xpath}/@xlink:title", namespaces=self.ns.nsmap())
        if len(title) == 1:
            _["title"] = title[0]

        return _

    def make_element(self):
        attributes = {}

        if "href" in self.element_attributes:
            attributes[f"{{{self.ns.xlink}}}href"] = self.element_attributes["href"]
            attributes[f"{{{self.ns.xlink}}}actuate"] = "onRequest"
        if "title" in self.element_attributes:
            attributes[f"{{{self.ns.xlink}}}title"] = self.element_attributes["title"]

        title = SubElement(self.parent_element, "Title", attrib=attributes)
        if "value" in self.element_attributes:
            title.text = self.element_attributes["value"]
