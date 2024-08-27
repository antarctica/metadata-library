import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from jsonschema import ValidationError
from lxml.etree import tostring

from bas_metadata_library.standards.iso_19115_1 import (
    MetadataRecord,
    MetadataRecordConfigV3,
    Namespaces,
)
from bas_metadata_library.standards.iso_19115_0 import MetadataRecordConfigV4
from tests.resources.configs.iso19115_1_standard import configs_v3_all

standard = "iso-19115-1"
namespaces = Namespaces()


def test_invalid_configuration_v3():
    config = {"invalid-configuration": "invalid-configuration"}
    with pytest.raises(ValidationError) as e:
        configuration = MetadataRecordConfigV3(**config)
        configuration.validate()
    assert "'hierarchy_level' is a required property" in str(e.value)


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_configuration_v3_from_json_file(config_name: str):
    configuration = MetadataRecordConfigV3()
    config_path = Path().resolve().parent.joinpath(f"resources/configs/{standard}/{config_name}.json")
    configuration.load(file=config_path)
    configuration.validate()
    assert configuration.config == configs_v3_all[config_name]


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_configuration_v3_from_json_string(config_name: str):
    with open(Path().resolve().parent.joinpath(f"resources/configs/{standard}/{config_name}.json"), mode="r") as file:
        config_str = file.read()
        configuration = MetadataRecordConfigV3()
        configuration.loads(string=config_str)
        configuration.validate()
        assert configuration.config == configs_v3_all[config_name]


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_configuration_v3_to_json_file(config_name: str):
    configuration = MetadataRecordConfigV3(**configs_v3_all[config_name])

    with TemporaryDirectory() as tmp_dir_name:
        config_path = Path(tmp_dir_name).joinpath("config.json")
        configuration.dump(file=config_path)
        with config_path.open() as config_file:
            config = json.load(config_file)

        with (
            Path().resolve().parent.joinpath(f"resources/configs/{standard}/{config_name}.json").open() as _config_file
        ):
            _config = json.load(_config_file)

        assert config == _config


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_configuration_v3_to_json_string(config_name: str):
    configuration = MetadataRecordConfigV3(**configs_v3_all[config_name])
    config = configuration.dumps()

    with Path().resolve().parent.joinpath(f"resources/configs/{standard}/{config_name}.json").open() as _config_file:
        _config = _config_file.read().rstrip("\n")

    assert config == _config


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_configuration_v3_json_round_trip(config_name: str):
    configuration = MetadataRecordConfigV3(**configs_v3_all[config_name])
    config = configuration.dumps()
    _config = MetadataRecordConfigV3()
    _config.loads(config)
    assert configuration.config == _config.config


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_parse_existing_record_v3(config_name: str):
    with open(
        Path().resolve().parent.joinpath(f"resources/records/{standard}/{config_name}-record.xml"), mode="r"
    ) as record_file:
        record_data = record_file.read()

    record = MetadataRecord(record=record_data)
    configuration_v4 = record.make_config()
    configuration_v3 = configuration_v4.downgrade_to_v3_config()
    config = configuration_v3.config
    assert config == configs_v3_all[config_name]


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_lossless_conversion_v3(get_record_response, config_name: str):
    _record = tostring(
        get_record_response(standard=standard, config=config_name),
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8",
    ).decode()
    _config = configs_v3_all[config_name]

    record = MetadataRecord(record=_record)
    config_v4 = record.make_config()
    config_ = config_v4.downgrade_to_v3_config().config

    config = MetadataRecordConfigV4()
    config.upgrade_from_v3_config(v3_config=MetadataRecordConfigV3(**config_))
    record_ = MetadataRecord(configuration=config).generate_xml_document().decode()
    assert _record == record_
    assert _config == config_
