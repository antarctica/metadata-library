from copy import deepcopy
from http import HTTPStatus
from pathlib import Path

import pytest
from flask.testing import FlaskClient
from jsonschema.exceptions import ValidationError
from lxml.etree import tostring, Element

from bas_metadata_library.standards.iso_19115_2 import (
    MetadataRecord,
    MetadataRecordConfigV4,
    Namespaces,
)
from tests.resources.configs.magic_discovery_profile import configs_v2_all

profile = "magic-discovery"
namespaces = Namespaces()


@pytest.mark.parametrize("config_name", list(configs_v2_all.keys()))
def test_config_schema_validation_valid(config_name: str):
    """Can validate minimal record configs against schema."""
    config = MetadataRecordConfigV4(**configs_v2_all[config_name])
    config.validate()
    assert True is True


def test_config_schema_validation_invalid_profile():
    """
    Cannot validate record configs that don't match schema.

    This is a basic test, to check the schema is loaded and the main, mandatory, parts of the schema work as expected.
    Conditional parts of the schema are tested elsewhere.
    """
    config = deepcopy(MetadataRecordConfigV4(**configs_v2_all["minimal_resource_v2"]))
    del config.config["file_identifier"]
    with pytest.raises(ValidationError) as e:
        config.validate()
    assert "'file_identifier' is a required property" in str(e.value)


@pytest.mark.parametrize("config_name", list(configs_v2_all.keys()))
def test_response(app_client: FlaskClient, config_name: str):
    """Can encode records for schema configs."""
    response = app_client.get(f"/profiles/{profile}/{config_name}")
    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "text/xml"


@pytest.mark.parametrize("config_name", list(configs_v2_all.keys()))
def test_complete_record(app_client: FlaskClient, config_name: str):
    """Check encoded records match known good examples."""
    with Path().resolve().parent.joinpath(f"resources/records/{profile}/{config_name}-record.xml").open() as expected_contents_file:
        expected_contents = expected_contents_file.read()

    response = app_client.get(f"/profiles/{profile}/{config_name}")
    assert response.data.decode() == expected_contents


@pytest.mark.parametrize("config_name", list(configs_v2_all.keys()))
def test_parse_existing_record(config_name: str):
    """Can decode a record to a record config."""
    with Path().resolve().parent.joinpath(f"resources/records/{profile}/{config_name}-record.xml").open() as record_file:
        record_data = record_file.read()

    record = MetadataRecord(record=record_data)
    configuration = record.make_config()
    config = configuration.config
    assert config == configs_v2_all[config_name]


@pytest.mark.parametrize("config_name", list(configs_v2_all.keys()))
def test_lossless_conversion(fx_get_record_response: Element, config_name: str):
    """Can encode then decode a record config without loss of information."""
    _record = tostring(
        fx_get_record_response(kind="profiles", standard_profile=profile, config=config_name),
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8",
    ).decode()
    _config = configs_v2_all[config_name]

    record = MetadataRecord(record=_record)
    config_ = record.make_config().config

    config = MetadataRecordConfigV4(**config_)
    record_ = MetadataRecord(configuration=config).generate_xml_document().decode()
    assert _record == record_
    assert _config == config_

def test_config_schema_cond_supertype():
    """Check conditional schema for additional required properties for resource super-type."""
    config = deepcopy(MetadataRecordConfigV4(**configs_v2_all["minimal_resource_v2"]))
    del config.config["identification"]['other_citation_details']
    with pytest.raises(ValidationError) as e:
        config.validate()
    assert "'other_citation_details' is a required property" in str(e.value)

def test_config_schema_cond_released():
    """Check conditional schema for required released date when publication date set."""
    config = deepcopy(MetadataRecordConfigV4(**configs_v2_all["minimal_container_v2"]))
    del config.config["identification"]['dates']['released']
    with pytest.raises(ValidationError) as e:
        config.validate()
    assert "'released' is a required property" in str(e.value)
