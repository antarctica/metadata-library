import json
from copy import deepcopy
from pathlib import Path

from importlib_resources import files as resource_file
from jsonschema.validators import validate
from lxml.etree import Element, fromstring  # nosec - see 'lxml` package (bandit)' section in README

from bas_metadata_library import MetadataRecord as _MetadataRecord, MetadataRecordConfig as _MetadataRecordConfig
from bas_metadata_library.standards.iso_19115_common import Namespaces
from bas_metadata_library.standards.iso_19115_common.root_element import ISOMetadataRecord
from bas_metadata_library.standards.iso_19115_common.utils import (
    decode_config_from_json,
    downgrade_to_v2_config as _downgrade_to_v2_config,
    encode_config_for_json,
    upgrade_from_v2_config as _upgrade_from_v2_config,
)


class MetadataRecordConfigV2(_MetadataRecordConfig):
    """
    Overloaded base MetadataRecordConfig class

    Defines version 2 of the JSON Schema used for this metadata standard
    """

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)

        self.config = kwargs

        schema_path = resource_file("bas_metadata_library.schemas.dist").joinpath("iso_19115_2_v2.json")
        with open(schema_path, mode="r") as schema_file:
            schema_data = json.load(schema_file)
        self.schema = schema_data

        if "$schema" in self.config:
            del self.config["$schema"]

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


class MetadataRecordConfigV3(_MetadataRecordConfig):
    """
    Overloaded base MetadataRecordConfig class

    Defines version 3 of the JSON Schema used for this metadata standard
    """

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)

        self.config = kwargs

        schema_path = resource_file("bas_metadata_library.schemas.dist").joinpath("iso_19115_2_v3.json")
        with open(schema_path, mode="r") as schema_file:
            schema_data = json.load(schema_file)
        self.schema = schema_data

        # Workaround - will be addressed in #149
        self.schema_uri = schema_data["$id"]
        self.config = {"$schema": self.schema_uri, **kwargs}

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

    def upgrade_from_v2_config(self, v2_config: MetadataRecordConfigV2) -> None:
        """
        Converts a v2 Metadata Configuration instance into a v2 Metadata Configuration instance.

        :type v2_config MetadataRecordConfigV2
        :param v2_config record configuration as a MetadataRecordConfigV2 instance
        """
        self.config = _upgrade_from_v2_config(
            v2_config=v2_config.config,
            schema_uri="https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v3.json",
        )

    def downgrade_to_v2_config(self) -> MetadataRecordConfigV2:
        """
        Converts a v3 Metadata Configuration instance into a v2 Metadata Configuration instance.

        :rtype MetadataRecordConfigV2
        :returns record configuration as a MetadataRecordConfigV2 instance
        """
        return MetadataRecordConfigV2(**_downgrade_to_v2_config(v3_config=self.config))


class MetadataRecord(_MetadataRecord):
    """
    Overloaded base MetadataRecordConfig class

    Defines the root element, and it's sub-elements, for this metadata standard

    Expects/requires record configurations to use version 3 of the configuration schema for this standard
    """

    def __init__(self, configuration: MetadataRecordConfigV3 = None, record: str = None):
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

    def make_config(self) -> MetadataRecordConfigV3:
        return MetadataRecordConfigV3(**self.metadata_record.make_config())

    def make_element(self) -> Element:
        return self.metadata_record.make_element()

    # noinspection PyMethodOverriding
    def validate(self) -> None:
        super().validate(xsd_path=Path("gmi/gmi.xsd"))
