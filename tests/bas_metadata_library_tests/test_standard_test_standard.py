import json
from copy import deepcopy
from http import HTTPStatus
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from flask.testing import FlaskClient
from jsonschema import ValidationError
from lxml.etree import XML, ElementTree, tostring, Element

from tests.resources.configs.test_metadata_standard import configs_all as configs
from tests.resources.configs.test_metadata_standard import minimal_record as minimal_config
from tests.standards.test_standard import MetadataRecord, MetadataRecordConfig, Namespaces

standard = "test-standard"


def test_invalid_configuration():
    config = {"invalid-configuration": "invalid-configuration"}
    configuration = MetadataRecordConfig(**config)
    with pytest.raises(ValidationError) as e:
        configuration.validate()
    assert "'resource' is a required property" in str(e.value)


def test_configuration_from_json_file():
    configuration = MetadataRecordConfig()
    configuration.load(file=Path().resolve().parent.joinpath(f"resources/configs/{standard}/minimal.json"))
    configuration.validate()
    assert configuration.config == minimal_config


def test_configuration_from_json_string():
    _config = '{"$schema": "#", "resource": {"title": {"value": "Test Record"}}}'
    configuration = MetadataRecordConfig()
    configuration.loads(string=_config)
    configuration.validate()
    assert configuration.config == minimal_config


def test_configuration_to_json_file():
    config = deepcopy(configs["minimal"])
    configuration = MetadataRecordConfig(**config)

    with TemporaryDirectory() as tmp_dir_name:
        config_path = Path(tmp_dir_name).joinpath("config.json")
        configuration.dump(file=config_path)
        with open(config_path, mode="r") as config_file:
            _config = json.load(config_file)
            assert _config == config


def test_configuration_to_json_string():
    config = deepcopy(configs["minimal"])
    configuration = MetadataRecordConfig(**config)
    _config = configuration.dumps()
    config_ = json.dumps(config, indent=2)
    assert _config == config_


@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_response(app_client: FlaskClient, config_name: str):
    response = app_client.get(f"/standards/{standard}/{config_name}")
    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "text/xml"


@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_complete_record(app_client: FlaskClient, config_name: str):
    with Path().resolve().parent.joinpath(f"resources/records/{standard}/{config_name}-record.xml").open() as expected_contents_file:
        expected_contents = expected_contents_file.read()

    response = app_client.get(f"/standards/{standard}/{config_name}")
    assert response.data.decode() == expected_contents


@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_xml_declaration(app_client: FlaskClient, config_name: str):
    response = app_client.get(f"/standards/{standard}/{config_name}")
    record = ElementTree(XML(response.data))
    assert record.docinfo.xml_version == "1.0"
    assert record.docinfo.encoding == "utf-8"


def test_xml_declaration_enabled():
    config = minimal_config
    configuration = MetadataRecordConfig(**config)
    record = MetadataRecord(configuration=configuration)
    document = record.generate_xml_document()
    assert "<?xml version='1.0' encoding='utf-8'?>" in document.decode()


@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_xml_namespaces(fx_get_record_response: Element, config_name: str):
    record = fx_get_record_response(kind='standards', standard_profile=standard, config=config_name)
    expected_namespaces = Namespaces().nsmap()
    assert record.nsmap == expected_namespaces


@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_root_element(fx_get_record_response: Element, config_name: str):
    record = fx_get_record_response(kind='standards', standard_profile=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config:
        pytest.skip("record does not contain a resource")

    resource = record.find(f"Resource")
    assert resource is not None


@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_resource_title(fx_get_record_response: Element, config_name: str):
    record = fx_get_record_response(kind='standards', standard_profile=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "title" not in config["resource"]:
        pytest.skip("record does not contain a resource title")

    resource_title = record.find(f"Resource/Title")
    assert resource_title is not None

    if "value" in config["resource"]["title"]:
        assert resource_title.text == config["resource"]["title"]["value"]

    if "href" in config["resource"]["title"]:
        assert resource_title.attrib[f"{{{Namespaces().xlink}}}href"] == config["resource"]["title"]["href"]

    if "title" in config["resource"]["title"]:
        assert resource_title.attrib[f"{{{Namespaces().xlink}}}title"] == config["resource"]["title"]["title"]


@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_parse_existing_record(config_name: str):
    with Path().resolve().parent.joinpath(f"resources/records/{standard}/{config_name}-record.xml").open() as record_file:
        record_data = record_file.read()

    record = MetadataRecord(record=record_data)
    configuration = record.make_config()
    config = configuration.config
    assert config == configs[config_name]


@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_lossless_conversion(fx_get_record_response: Element, config_name: str):
    _record = tostring(
        fx_get_record_response(kind='standards', standard_profile=standard, config=config_name),
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8",
    ).decode()
    _config = configs[config_name]

    record = MetadataRecord(record=_record)
    config_ = record.make_config().config

    config = MetadataRecordConfig(**config_)
    record_ = MetadataRecord(configuration=config).generate_xml_document().decode()
    assert _record == record_
    assert _config == config_
