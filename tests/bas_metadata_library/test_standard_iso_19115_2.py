import datetime
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


def test_configuration_v2_to_json_file():
    _config = deepcopy(configs_safe_v2["minimal_v2"])
    _config["identification"]["dates"]["revision"] = {
        "date": datetime.datetime(2018, 1, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)
    }
    configuration = MetadataRecordConfigV2(**_config)

    with TemporaryDirectory() as tmp_dir_name:
        config_path = Path(tmp_dir_name).joinpath("config.json")
        configuration.dump(file=config_path)

        with open(config_path, mode="r") as config_file:
            config = json.load(config_file)
            config = json.dumps(config)
            # this should assert the encoded config object is the same as the test file used in the JSON loads method
            # note: this means adding a revision date as we modify the minimal record for test coverage
            config_ = json.dumps(
                {
                    "hierarchy_level": "dataset",
                    "metadata": {
                        "language": "eng",
                        "character_set": "utf-8",
                        "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
                        "date_stamp": "2018-10-18",
                    },
                    "identification": {
                        "title": {"value": "Test Record"},
                        "dates": {"creation": "2018", "revision": "2018-01-01T10:00:00+00:00"},
                        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with required properties only.",
                        "character_set": "utf-8",
                        "language": "eng",
                        "topics": ["environment", "climatologyMeteorologyAtmosphere"],
                        "extent": {
                            "geographic": {
                                "bounding_box": {
                                    "west_longitude": -45.61521,
                                    "east_longitude": -27.04976,
                                    "south_latitude": -68.1511,
                                    "north_latitude": -54.30761,
                                }
                            }
                        },
                    },
                }
            )
            assert config == config_


def test_configuration_v2_to_json_string():
    _config = deepcopy(configs_safe_v2["minimal_v2"])
    _config["identification"]["dates"]["revision"] = {
        "date": datetime.datetime(2018, 1, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)
    }
    configuration = MetadataRecordConfigV2(**_config)
    config = configuration.dumps()
    # this should assert the encoded config object is the same as the test file used in the JSON loads method
    config_ = json.dumps(
        {
            "hierarchy_level": "dataset",
            "metadata": {
                "language": "eng",
                "character_set": "utf-8",
                "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
                "date_stamp": "2018-10-18",
            },
            "identification": {
                "title": {"value": "Test Record"},
                "dates": {"creation": "2018", "revision": "2018-01-01T10:00:00+00:00"},
                "abstract": "Test Record for ISO 19115 metadata standard (no profile) with required properties only.",
                "character_set": "utf-8",
                "language": "eng",
                "topics": ["environment", "climatologyMeteorologyAtmosphere"],
                "extent": {
                    "geographic": {
                        "bounding_box": {
                            "west_longitude": -45.61521,
                            "east_longitude": -27.04976,
                            "south_latitude": -68.1511,
                            "north_latitude": -54.30761,
                        }
                    }
                },
            },
        }
    )
    assert config == config_


def test_configuration_v2_json_round_trip():
    # this should be the same as the test file used in the JSON loads method
    config = {
        "hierarchy_level": "dataset",
        "metadata": {
            "language": "eng",
            "character_set": "utf-8",
            "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
            "date_stamp": "2018-10-18",
        },
        "identification": {
            "title": {"value": "Test Record"},
            "dates": {"creation": "2018"},
            "abstract": "Test Record for ISO 19115 metadata standard (no profile) with required properties only.",
            "character_set": "utf-8",
            "language": "eng",
            "topics": ["environment", "climatologyMeteorologyAtmosphere"],
            "extent": {
                "geographic": {
                    "bounding_box": {
                        "west_longitude": -45.61521,
                        "east_longitude": -27.04976,
                        "south_latitude": -68.1511,
                        "north_latitude": -54.30761,
                    }
                }
            },
        },
    }
    _config = json.dumps(config)
    configuration = MetadataRecordConfigV2()
    configuration.loads(_config)
    config_ = configuration.dumps()
    assert _config == config_


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


@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_parse_existing_record_v2(config_name):
    with open(f"tests/resources/records/iso-19115-2/{config_name}-record.xml") as record_file:
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
