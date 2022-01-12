import json
from copy import deepcopy
from pathlib import Path

from importlib_resources import files as resource_file
from jsonschema.validators import validate
from lxml.etree import Element, fromstring  # nosec - see 'lxml` package (bandit)' section in README

from bas_metadata_library import (
    MetadataRecord as _MetadataRecord,
    MetadataRecordConfig as _MetadataRecordConfig,
    Namespaces as _Namespaces,
)
from bas_metadata_library.standards.iso_19115_common.root_element import ISOMetadataRecord
from bas_metadata_library.standards.iso_19115_common.utils import (
    decode_config_from_json,
    encode_config_for_json,
)


class Namespaces(_Namespaces):
    """
    Overloaded base Namespaces class

    Defines the namespaces for this standard
    """

    gmd = "http://www.isotc211.org/2005/gmd"
    gco = "http://www.isotc211.org/2005/gco"
    gml = "http://www.opengis.net/gml/3.2"
    gmx = "http://www.isotc211.org/2005/gmx"
    srv = "http://www.isotc211.org/2005/srv"
    xlink = "http://www.w3.org/1999/xlink"
    xsi = "http://www.w3.org/2001/XMLSchema-instance"

    _schema_locations = {
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


class MetadataRecordConfigV2(_MetadataRecordConfig):
    """
    Overloaded base MetadataRecordConfig class

    Defines version 2 of the JSON Schema used for this metadata standard
    """

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)

        self.config = kwargs

        schema_path = resource_file("bas_metadata_library.schemas.dist").joinpath("iso_19115_1_v2.json")
        with open(schema_path, mode="r") as schema_file:
            schema_data = json.load(schema_file)
        self.schema = schema_data

    def validate(self) -> None:
        if self.schema is not None:
            _config = encode_config_for_json(config=deepcopy(self.config))
            return validate(instance=_config, schema=self.schema)

    def load(self, file: Path) -> None:
        with open(str(file), mode="r") as file:
            self.config = decode_config_from_json(config=json.load(fp=file))

    def loads(self, string: str) -> None:
        self.config = decode_config_from_json(config=json.loads(s=string))

    def dump(self, file: Path) -> None:
        with open(str(file), mode="w") as file:
            json.dump(encode_config_for_json(config=deepcopy(self.config)), file)

    def dumps(self) -> str:
        return json.dumps(encode_config_for_json(config=deepcopy(self.config)))


class MetadataRecord(_MetadataRecord):
    """
    Overloaded base MetadataRecordConfig class

    Defines the root element, and it's sub-elements, for this metadata standard

    Expects/requires record configurations to use version 2 of the configuration schema for this standard
    """

    def __init__(self, configuration: MetadataRecordConfigV2 = None, record: str = None):
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
            self.record = fromstring(record.encode())

        self.metadata_record = ISOMetadataRecord(record=self.record, attributes=self.attributes, xpath=self.xpath)

    def make_config(self) -> MetadataRecordConfigV2:
        return MetadataRecordConfigV2(**self.metadata_record.make_config())

    def make_element(self) -> Element:
        return self.metadata_record.make_element()

    # noinspection PyMethodOverriding
    def validate(self) -> None:
        super().validate(xsd_path=Path("gmd/gmd.xsd"))
