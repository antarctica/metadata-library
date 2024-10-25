from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from importlib_resources import files as resource_file
from lxml.etree import Element, fromstring

from bas_metadata_library import MetadataRecord as _MetadataRecord
from bas_metadata_library import MetadataRecordConfig as _MetadataRecordConfig
from bas_metadata_library.standards.iso_19115_common import Namespaces
from bas_metadata_library.standards.iso_19115_common.root_element import ISOMetadataRecord
from bas_metadata_library.standards.iso_19115_common.utils import (
    decode_config_from_json,
    encode_config_for_json,
    validate_config,
)


class MetadataRecordConfigV4(_MetadataRecordConfig):
    """v4 configuration schema for ISO 19115:2003."""

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)

        self.config = kwargs

        schema_path = resource_file("bas_metadata_library.schemas.dist").joinpath("iso_19115_2_v4.json")
        with schema_path.open() as schema_file:
            schema_data = json.load(schema_file)
        self.schema = schema_data

        # Workaround - will be addressed in #149
        self.schema_uri = schema_data["$id"]
        self.config = {"$schema": self.schema_uri, **kwargs}

    def validate(self) -> None:
        validate_config(config=self.config, schema=self.schema)

    def load(self, file: Path) -> None:
        with file.open() as file:
            self.config = decode_config_from_json(config=json.load(fp=file))

    def loads(self, string: str) -> None:
        self.config = decode_config_from_json(config=json.loads(s=string))

    def dump(self, file: Path) -> None:
        with file.open(mode="w") as file:
            json.dump(encode_config_for_json(config=deepcopy(self.config)), file, indent=2)

    def dumps(self) -> str:
        return json.dumps(encode_config_for_json(config=deepcopy(self.config)), indent=2)


class MetadataRecord(_MetadataRecord):
    """
    Defines the root element, and it's sub-elements, for this metadata standard.

    Expects/requires record configurations to use version 3 of the configuration schema for this standard
    """

    def __init__(self, configuration: MetadataRecordConfigV4 = None, record: str | None = None):
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
            self.record = fromstring(record.encode())  # noqa: S320 (see '`lxml` package (security)' README section)

        self.metadata_record = ISOMetadataRecord(record=self.record, attributes=self.attributes, xpath=self.xpath)

    def make_config(self) -> MetadataRecordConfigV4:
        return MetadataRecordConfigV4(**self.metadata_record.make_config())

    def make_element(self) -> Element:
        return self.metadata_record.make_element()

    # noinspection PyMethodOverriding
    def validate(self) -> None:
        super().validate(xsd_path=Path("gmi/gmi.xsd"))
