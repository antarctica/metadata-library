from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from importlib_resources import files as resource_file
from jsonschema.validators import validate
from lxml.etree import Element, fromstring  # nosec - see 'lxml` package (bandit)' section in README

from bas_metadata_library import (
    MetadataRecord as _MetadataRecord,
)
from bas_metadata_library import (
    MetadataRecordConfig as _MetadataRecordConfig,
)
from bas_metadata_library import (
    Namespaces as _Namespaces,
)
from bas_metadata_library.standards.iso_19115_common.root_element import ISOMetadataRecord
from bas_metadata_library.standards.iso_19115_common.utils import (
    decode_config_from_json,
    encode_config_for_json,
)


class Namespaces(_Namespaces):
    """Defines the namespaces for this standard."""

    gmd = "http://www.isotc211.org/2005/gmd"
    gco = "http://www.isotc211.org/2005/gco"
    gml = "http://www.opengis.net/gml/3.2"
    gmx = "http://www.isotc211.org/2005/gmx"
    srv = "http://www.isotc211.org/2005/srv"
    xlink = "http://www.w3.org/1999/xlink"
    xsi = "http://www.w3.org/2001/XMLSchema-instance"

    _schema_locations = {  # noqa: RUF012
        "gmd": "https://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gmd/gmd.xsd",
        "gco": "https://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gco/gco.xsd",
        "gmx": "https://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gmx/gmx.xsd",
        "srv": "https://standards.iso.org/iso/19119/srv/srv.xsd",
    }

    def __init__(self):
        self._namespaces = {
            "gmd": self.gmd,
            "gco": self.gco,
            "gml": self.gml,
            "gmx": self.gmx,
            "srv": self.srv,
            "xlink": self.xlink,
            "xsi": self.xsi,
        }
        super().__init__(namespaces=self._namespaces)


class MetadataRecordConfigV3(_MetadataRecordConfig):
    """Defines version 3 of the JSON Schema used for this metadata standard."""

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)

        self.config = kwargs

        schema_path = resource_file("bas_metadata_library.schemas.dist").joinpath("iso_19115_1_v3.json")
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


class MetadataRecord(_MetadataRecord):
    """
    Defines the root element, and it's sub-elements, for this metadata standard.

    Expects/requires record configurations to use version 3 of the configuration schema for this standard
    """

    def __init__(self, configuration: MetadataRecordConfigV3 = None, record: str | None = None):
        self.ns = Namespaces()
        self.attributes = {}
        self.record = Element(
            f"{{{self.ns.gmd}}}MD_Metadata",
            attrib={f"{{{self.ns.xsi}}}schemaLocation": self.ns.schema_locations()},
            nsmap=self.ns.nsmap(),
        )
        self.xpath = "/gmd:MD_Metadata"

        if configuration is not None:
            configuration.validate()
            self.attributes = configuration.config

        if record is not None:
            self.record = fromstring(record.encode())  # noqa: S320 (see '`lxml` package (security)' README section)

        self.metadata_record = ISOMetadataRecord(record=self.record, attributes=self.attributes, xpath=self.xpath)

    def make_config(self) -> MetadataRecordConfigV3:
        return MetadataRecordConfigV3(**self.metadata_record.make_config())

    def make_element(self) -> Element:
        return self.metadata_record.make_element()

    # noinspection PyMethodOverriding
    def validate(self) -> None:
        super().validate(xsd_path=Path("gmd/gmd.xsd"))
