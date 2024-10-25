from copy import deepcopy
from http import HTTPStatus
from pathlib import Path

import pytest
from flask.testing import FlaskClient
from jsonschema.exceptions import ValidationError
from lxml.etree import tostring, Element

from bas_metadata_library import RecordValidationError
from bas_metadata_library.standards.iso_19115_2 import (
    MetadataRecord,
    MetadataRecordConfigV4,
    Namespaces,
)
from tests.resources.configs.magic_discovery_profile import configs_v1_all

profile = "magic-discovery"
namespaces = Namespaces()


@pytest.mark.parametrize("config_name", list(configs_v1_all.keys()))
def test_config_schema_validation_valid(config_name: str):
    config = MetadataRecordConfigV4(**configs_v1_all[config_name])
    config.validate()
    assert True is True


def test_config_schema_validation_invalid_profile():
    config = deepcopy(MetadataRecordConfigV4(**configs_v1_all["minimal_product_v1"]))
    with pytest.raises(ValidationError) as e:
        del config.config["file_identifier"]
        config.validate()
    assert "'file_identifier' is a required property" in str(e.value)


@pytest.mark.parametrize("config_name", list(configs_v1_all.keys()))
def test_response(app_client: FlaskClient, config_name: str):
    response = app_client.get(f"/profiles/{profile}/{config_name}")
    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "text/xml"


@pytest.mark.parametrize("config_name", list(configs_v1_all.keys()))
def test_complete_record(app_client: FlaskClient, config_name: str):
    with Path().resolve().parent.joinpath(f"resources/records/{profile}/{config_name}-record.xml").open() as expected_contents_file:
        expected_contents = expected_contents_file.read()

    response = app_client.get(f"/profiles/{profile}/{config_name}")
    assert response.data.decode() == expected_contents


@pytest.mark.parametrize("config_name", list(configs_v1_all.keys()))
def test_parse_existing_record(config_name: str):
    with Path().resolve().parent.joinpath(f"resources/records/{profile}/{config_name}-record.xml").open() as record_file:
        record_data = record_file.read()

    record = MetadataRecord(record=record_data)
    configuration = record.make_config()
    config = configuration.config
    assert config == configs_v1_all[config_name]


@pytest.mark.parametrize("config_name", list(configs_v1_all.keys()))
def test_lossless_conversion(fx_get_record_response: Element, config_name: str):
    _record = tostring(
        fx_get_record_response(kind="profiles", standard_profile=profile, config=config_name),
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8",
    ).decode()
    _config = configs_v1_all[config_name]

    record = MetadataRecord(record=_record)
    config_ = record.make_config().config

    config = MetadataRecordConfigV4(**config_)
    record_ = MetadataRecord(configuration=config).generate_xml_document().decode()
    assert _record == record_
    assert _config == config_
