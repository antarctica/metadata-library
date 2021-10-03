import datetime

import pytest

from copy import deepcopy
from pathlib import Path
from http import HTTPStatus

from jsonschema import ValidationError

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# This is a testing environment, testing against endpoints that don't themselves allow user input, so the XML returned
# should be safe. In any case the test environment is not exposed and so does not present a risk.
from lxml.etree import ElementTree, XML, tostring

from bas_metadata_library.standards.iso_19115_2 import (
    Namespaces,
    MetadataRecordConfigV1,
    MetadataRecordConfigV2,
    MetadataRecord,
)

from tests.resources.configs.iso19115_2_standard import configs_safe_v1, configs_safe_v2, configs_safe_all

standard = "iso-19115-2"
namespaces = Namespaces()


def test_invalid_configuration_v1():
    config = {"invalid-configuration": "invalid-configuration"}
    with pytest.raises(ValidationError) as e:
        configuration = MetadataRecordConfigV1(**config)
        configuration.validate()
    assert "'language' is a required property" in str(e.value)


def test_invalid_configuration_v2():
    config = {"invalid-configuration": "invalid-configuration"}
    with pytest.raises(ValidationError) as e:
        configuration = MetadataRecordConfigV2(**config)
        configuration.validate()
    assert "'hierarchy_level' is a required property" in str(e.value)


def test_configuration_v1_from_json_file():
    configuration = MetadataRecordConfigV1()
    configuration.load(file=Path("tests/resources/configs/iso19115_1_standard_minimal_record_v1.json"))
    configuration.validate()
    _config = deepcopy(configs_safe_v1["minimal_v1"])
    _config["resource"]["dates"].append(
        {"date": datetime.datetime(2018, 1, 1, 10, 0, 0, tzinfo=datetime.timezone.utc), "date_type": "revision"}
    )
    assert configuration.config == _config


def test_configuration_v1_from_json_string():
    with open(str(Path("tests/resources/configs/iso19115_1_standard_minimal_record_v1.json")), mode="r") as file:
        config_str = file.read()
        configuration = MetadataRecordConfigV1()
        configuration.loads(string=config_str)
        configuration.validate()
        _config = deepcopy(configs_safe_v1["minimal_v1"])
        _config["resource"]["dates"].append(
            {"date": datetime.datetime(2018, 1, 1, 10, 0, 0, tzinfo=datetime.timezone.utc), "date_type": "revision"}
        )
        assert configuration.config == _config


def test_configuration_v2_from_json_file():
    configuration = MetadataRecordConfigV2()
    configuration.load(file=Path("tests/resources/configs/iso19115_1_standard_minimal_record_v2.json"))
    configuration.validate()
    _config = deepcopy(configs_safe_v2["minimal_v2"])
    _config["identification"]["dates"]["revision"] = {
        "date": datetime.datetime(2018, 1, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)
    }
    assert configuration.config == _config


def test_configuration_v2_from_json_string():
    with open(str(Path("tests/resources/configs/iso19115_1_standard_minimal_record_v2.json")), mode="r") as file:
        config_str = file.read()
        configuration = MetadataRecordConfigV2()
        configuration.loads(string=config_str)
        configuration.validate()
        _config = deepcopy(configs_safe_v2["minimal_v2"])
        _config["identification"]["dates"]["revision"] = {
            "date": datetime.datetime(2018, 1, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)
        }
        assert configuration.config == _config


@pytest.mark.usefixtures("app_client")
@pytest.mark.parametrize("config_name", list(configs_safe_all.keys()))
def test_response(client, config_name):
    response = client.get(f"/standards/{standard}/{config_name}")
    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "text/xml"


@pytest.mark.usefixtures("app_client")
@pytest.mark.parametrize("config_name", list(configs_safe_all.keys()))
def test_complete_record(client, config_name):
    with open(f"tests/resources/records/iso-19115-2/{config_name}-record.xml") as expected_contents_file:
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


@pytest.mark.parametrize("config_name", list(configs_safe_v1.keys()))
def test_parse_existing_record_v1(config_name):
    with open(f"tests/resources/records/iso-19115-2/{config_name}-record.xml") as record_file:
        record_data = record_file.read()

    record = MetadataRecord(record=record_data)
    configuration = MetadataRecordConfigV1()
    configuration.convert_from_v2_configuration(record.make_config())
    config = configuration.config
    assert config == configs_safe_v1[config_name]


@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_parse_existing_record_v2(config_name):
    with open(f"tests/resources/records/iso-19115-2/{config_name}-record.xml") as record_file:
        record_data = record_file.read()

    record = MetadataRecord(record=record_data)
    configuration = record.make_config()
    config = configuration.config
    assert config == configs_safe_v2[config_name]


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v1.keys()))
def test_lossless_conversion_v1(get_record_response, config_name):
    _record = tostring(
        get_record_response(standard=standard, config=config_name),
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8",
    ).decode()
    _config = configs_safe_v1[config_name]

    record = MetadataRecord(record=_record)
    config_ = MetadataRecordConfigV1()
    config_.convert_from_v2_configuration(record.make_config())
    config_ = config_.config

    config = MetadataRecordConfigV1(**config_)
    config = config.convert_to_v2_configuration()
    record_ = MetadataRecord(configuration=config).generate_xml_document().decode()
    assert _record == record_
    assert _config == config_


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
