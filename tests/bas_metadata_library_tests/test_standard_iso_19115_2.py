import json
from copy import deepcopy
from http import HTTPStatus
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from flask.testing import FlaskClient
from jsonschema import ValidationError
from lxml.etree import XML, ElementTree, tostring, Element

from bas_metadata_library import RecordValidationError
from bas_metadata_library.standards.iso_19115_2 import (
    MetadataRecord,
    MetadataRecordConfigV4,
    Namespaces,
)
from tests.resources.configs.iso19115_2_standard import configs_v4_all

standard = "iso-19115-2"
namespaces = Namespaces()


def test_invalid_configuration_v4():
    config = {"invalid-configuration": "invalid-configuration"}
    with pytest.raises(ValidationError) as e:
        configuration = MetadataRecordConfigV4(**config)
        configuration.validate()
    assert "'metadata' is a required property" in str(e.value)


@pytest.mark.parametrize("config_name", list(configs_v4_all.keys()))
def test_configuration_v4_from_json_file(config_name: str):
    configuration = MetadataRecordConfigV4()
    config_path = Path().resolve().parent.joinpath(f"resources/configs/{standard}/{config_name}.json")
    configuration.load(file=config_path)
    configuration.validate()
    assert configuration.config == configs_v4_all[config_name]


@pytest.mark.parametrize("config_name", list(configs_v4_all.keys()))
def test_configuration_v4_to_json_file(config_name: str):
    configuration = MetadataRecordConfigV4(**configs_v4_all[config_name])

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


@pytest.mark.parametrize("config_name", list(configs_v4_all.keys()))
def test_configuration_v4_to_json_string(config_name: str):
    configuration = MetadataRecordConfigV4(**configs_v4_all[config_name])

    config = configuration.dumps()

    with Path().resolve().parent.joinpath(f"resources/configs/{standard}/{config_name}.json").open() as _config_file:
        _config = _config_file.read().rstrip("\n")

    assert config == _config


@pytest.mark.parametrize("config_name", list(configs_v4_all.keys()))
def test_configuration_v4_json_round_trip(config_name: str):
    configuration = MetadataRecordConfigV4(**configs_v4_all[config_name])
    config = configuration.dumps()
    _config = MetadataRecordConfigV4()
    _config.loads(config)
    assert configuration.config == _config.config


@pytest.mark.parametrize("config_name", list(configs_v4_all.keys()))
def test_response(app_client: FlaskClient, config_name: str):
    response = app_client.get(f"/standards/{standard}/{config_name}")
    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "text/xml"


@pytest.mark.parametrize("config_name", list(configs_v4_all.keys()))
def test_complete_record(app_client: FlaskClient, config_name: str):
    with Path().resolve().parent.joinpath(f"resources/records/{standard}/{config_name}-record.xml").open() as expected_contents_file:
        expected_contents = expected_contents_file.read()

    response = app_client.get(f"/standards/{standard}/{config_name}")
    assert response.data.decode() == expected_contents


@pytest.mark.parametrize("config_name", list(configs_v4_all.keys()))
def test_xml_declaration(app_client: FlaskClient, config_name: str):
    response = app_client.get(f"/standards/{standard}/{config_name}")
    record = ElementTree(XML(response.data))
    assert record.docinfo.xml_version == "1.0"
    assert record.docinfo.encoding == "utf-8"


@pytest.mark.parametrize("config_name", list(configs_v4_all.keys()))
def test_xml_namespaces(fx_get_record_response: Element, config_name: str):
    record = fx_get_record_response(kind="standards", standard_profile=standard, config=config_name)
    expected_namespaces = Namespaces().nsmap()
    assert record.nsmap == expected_namespaces


@pytest.mark.parametrize("config_name", list(configs_v4_all.keys()))
def test_root_element(fx_get_record_response: Element, config_name: str):
    record = fx_get_record_response(kind="standards", standard_profile=standard, config=config_name)

    metadata_records = record.xpath("/gmi:MI_Metadata", namespaces=namespaces.nsmap())
    assert len(metadata_records) == 1


@pytest.mark.parametrize("config_name", list(configs_v4_all.keys()))
def test_parse_existing_record_v4(config_name: str):
    with Path().resolve().parent.joinpath(f"resources/records/{standard}/{config_name}-record.xml").open() as record_file:
        record_data = record_file.read()

    record = MetadataRecord(record=record_data)
    configuration = record.make_config()
    config = configuration.config
    assert config == configs_v4_all[config_name]


@pytest.mark.parametrize("config_name", list(configs_v4_all.keys()))
def test_lossless_conversion_v4(fx_get_record_response: Element, config_name: str):
    _record = tostring(
        fx_get_record_response(kind="standards", standard_profile=standard, config=config_name),
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8",
    ).decode()
    _config = configs_v4_all[config_name]

    record = MetadataRecord(record=_record)
    config_ = record.make_config().config

    config = MetadataRecordConfigV4(**config_)
    record_ = MetadataRecord(configuration=config).generate_xml_document().decode()
    assert _record == record_
    assert _config == config_


@pytest.mark.parametrize("config_name", list(configs_v4_all.keys()))
def test_record_schema_validation_valid(config_name: str):
    config = MetadataRecordConfigV4(**configs_v4_all[config_name])
    record = MetadataRecord(configuration=config)
    record.validate()
    assert True is True


def test_record_schema_validation_invalid():
    config = deepcopy(MetadataRecordConfigV4(**configs_v4_all["minimal_v4"]))
    record = MetadataRecord(configuration=config)
    with pytest.raises(RecordValidationError) as e:
        record.attributes["identification"]["spatial_resolution"] = "invalid"
        record.validate()
    assert "Record validation failed:" in str(e.value)
