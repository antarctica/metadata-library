import json

from tempfile import TemporaryDirectory
from copy import deepcopy
from pathlib import Path
from http import HTTPStatus

import pytest

from jsonschema import ValidationError

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# This is a testing environment, testing against endpoints that don't themselves allow user input, so the XML returned
# should be safe. In any case the test environment is not exposed and so does not present a risk.
from lxml.etree import ElementTree, XML, tostring

from bas_metadata_library import RecordValidationError
from bas_metadata_library.standards.iso_19115_2 import (
    Namespaces,
    MetadataRecordConfigV2,
    MetadataRecord,
)

from tests.resources.configs.iso19115_2_standard import configs_safe_v2, configs_safe_all

standard = "iso-19115-2"
namespaces = Namespaces()


def test_invalid_configuration_v2():
    config = {"invalid-configuration": "invalid-configuration"}
    with pytest.raises(ValidationError) as e:
        configuration = MetadataRecordConfigV2(**config)
        configuration.validate()
    assert "'hierarchy_level' is a required property" in str(e.value)


@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_configuration_v2_from_json_file(config_name):
    configuration = MetadataRecordConfigV2()
    config_path = Path().resolve().parent.joinpath(f"resources/configs/{standard}/{config_name}.json")
    configuration.load(file=config_path)
    configuration.validate()
    assert configuration.config == configs_safe_v2[config_name]


@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_configuration_v2_to_json_file(config_name):
    configuration = MetadataRecordConfigV2(**configs_safe_v2[config_name])

    with TemporaryDirectory() as tmp_dir_name:
        config_path = Path(tmp_dir_name).joinpath("config.json")
        configuration.dump(file=config_path)
        with open(config_path, mode="r") as config_file:
            config = json.load(config_file)

        with open(
            Path().resolve().parent.joinpath(f"resources/configs/{standard}/{config_name}.json"), mode="r"
        ) as _config_file:
            _config = json.load(_config_file)

        assert config == _config


@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_configuration_v2_to_json_string(config_name):
    configuration = MetadataRecordConfigV2(**configs_safe_v2[config_name])

    config = configuration.dumps()

    with open(
        Path().resolve().parent.joinpath(f"resources/configs/{standard}/{config_name}.json"), mode="r"
    ) as _config_file:
        _config = _config_file.read()

    assert config == _config


@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_configuration_v2_json_round_trip(config_name):
    configuration = MetadataRecordConfigV2(**configs_safe_v2[config_name])
    config = configuration.dumps()
    _config = MetadataRecordConfigV2()
    _config.loads(config)
    assert configuration.config == _config.config


@pytest.mark.usefixtures("app_client")
@pytest.mark.parametrize("config_name", list(configs_safe_all.keys()))
def test_response(client, config_name):
    response = client.get(f"/standards/{standard}/{config_name}")
    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "text/xml"


@pytest.mark.usefixtures("app_client")
@pytest.mark.parametrize("config_name", list(configs_safe_all.keys()))
def test_complete_record(client, config_name):
    with open(
        Path().resolve().parent.joinpath(f"resources/records/{standard}/{config_name}-record.xml"), mode="r"
    ) as expected_contents_file:
        expected_contents = expected_contents_file.read()

    response = client.get(f"/standards/{standard}/{config_name}")
    assert response.data.decode() == expected_contents


@pytest.mark.usefixtures("app_client")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_xml_declaration(client, config_name):
    response = client.get(f"/standards/{standard}/{config_name}")
    record = ElementTree(XML(response.data))
    assert record.docinfo.xml_version == "1.0"
    assert record.docinfo.encoding == "utf-8"


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_xml_namespaces(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    expected_namespaces = Namespaces().nsmap()
    assert record.nsmap == expected_namespaces


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_root_element(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)

    metadata_records = record.xpath("/gmi:MI_Metadata", namespaces=namespaces.nsmap())
    assert len(metadata_records) == 1


@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_parse_existing_record_v2(config_name):
    with open(
        Path().resolve().parent.joinpath(f"resources/records/{standard}/{config_name}-record.xml"), mode="r"
    ) as record_file:
        record_data = record_file.read()

    record = MetadataRecord(record=record_data)
    configuration = record.make_config()
    config = configuration.config
    assert config == configs_safe_v2[config_name]


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_lossless_conversion_v2(get_record_response, config_name):
    _record = tostring(
        get_record_response(standard=standard, config=config_name),
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8",
    ).decode()
    _config = configs_safe_v2[config_name]

    record = MetadataRecord(record=_record)
    config_ = record.make_config().config

    config = MetadataRecordConfigV2(**config_)
    record_ = MetadataRecord(configuration=config).generate_xml_document().decode()
    assert _record == record_
    assert _config == config_


@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_record_schema_validation_valid(config_name):
    config = MetadataRecordConfigV2(**configs_safe_v2[config_name])
    record = MetadataRecord(configuration=config)
    record.validate()
    assert True is True


def test_record_schema_validation_invalid():
    config = deepcopy(MetadataRecordConfigV2(**configs_safe_v2["minimal_v2"]))
    record = MetadataRecord(configuration=config)
    with pytest.raises(RecordValidationError) as e:
        record.attributes["identification"]["spatial_resolution"] = "invalid"
        record.validate()
    assert "Record validation failed:" in str(e.value)
