from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from importlib_resources import files as resource_file
from jsonschema.validators import validate
from lxml.etree import Element, fromstring

from bas_metadata_library import MetadataRecord as _MetadataRecord
from bas_metadata_library import MetadataRecordConfig as _MetadataRecordConfig
from bas_metadata_library.standards.iso_19115_common import Namespaces
from bas_metadata_library.standards.iso_19115_common.root_element import ISOMetadataRecord
from bas_metadata_library.standards.iso_19115_common.utils import (
    decode_config_from_json,
    downgrade_from_v4_config,
    encode_config_for_json,
    upgrade_from_v3_config,
)


class MetadataRecordConfigV3(_MetadataRecordConfig):
    """Defines version 3 of the JSON Schema used for this metadata standard."""

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)

        self.config = kwargs

        schema_path = resource_file("bas_metadata_library.schemas.dist").joinpath("iso_19115_2_v3.json")
        with schema_path.open() as schema_file:
            schema_data = json.load(schema_file)
        self.schema = schema_data

        # Workaround - will be addressed in #149
        self.schema_uri = schema_data["$id"]
        self.config = {"$schema": self.schema_uri, **kwargs}

    def validate(self) -> None:
        if self.schema is None:
            return None

        _config = encode_config_for_json(config=deepcopy(self.config))
        return validate(instance=_config, schema=self.schema)

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
        _config = encode_config_for_json(config=deepcopy(self.config))
        return validate(instance=_config, schema=self.schema)

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

    def upgrade_from_v3_config(self, v3_config: MetadataRecordConfigV3) -> None:
        self.config = upgrade_from_v3_config(v3_config=v3_config.config)

    def downgrade_to_v3_config(self) -> MetadataRecordConfigV3:
        return MetadataRecordConfigV3(**downgrade_from_v4_config(v4_config=self.config))


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
