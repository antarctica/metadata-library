# noinspection PyUnresolvedReferences
import pytest

from http import HTTPStatus

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# This is a testing environment, testing against endpoints that don't themselves allow user input, so the XML returned
# should be safe. In any case the test environment is not exposed and so does not present a risk.
from jsonschema import ValidationError
from lxml.etree import ElementTree, XML, tostring

from tests.resources.configs.test_metadata_standard import configs_all as configs
from tests.standards.test_standard import Namespaces, MetadataRecordConfig, MetadataRecord

standard = "test-standard"


def test_invalid_configuration():
    config = {"invalid-configuration": "invalid-configuration"}
    with pytest.raises(ValidationError) as e:
        MetadataRecordConfig(**config)
    assert "'resource' is a required property" in str(e.value)


@pytest.mark.usefixtures("app_client")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_response(client, config_name):
    response = client.get(f"/standards/{standard}/{config_name}")
    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "text/xml"


@pytest.mark.usefixtures("app_client")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_complete_record(client, config_name):
    with open(f"tests/resources/records/test-standard-v1/{config_name}-record.xml") as expected_contents_file:
        expected_contents = expected_contents_file.read()

    response = client.get(f"/standards/{standard}/{config_name}")
    assert response.data.decode() == expected_contents


@pytest.mark.usefixtures("app_client")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_xml_declaration(client, config_name):
    response = client.get(f"/standards/{standard}/{config_name}")
    record = ElementTree(XML(response.data))
    assert record.docinfo.xml_version == "1.0"
    assert record.docinfo.encoding == "utf-8"


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_xml_namespaces(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    expected_namespaces = Namespaces().nsmap()
    assert record.nsmap == expected_namespaces


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_root_element(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config:
        pytest.skip("record does not contain a resource")

    resource = record.find(f"Resource")
    assert resource is not None


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_resource_title(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
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
def test_parse_existing_record(config_name):
    with open(f"tests/resources/records/test-standard-v1/{config_name}-record.xml") as record_file:
        record_data = record_file.read()

    record = MetadataRecord(record=record_data)
    configuration = record.make_config()
    config = configuration.config
    assert config == configs[config_name]


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_lossless_conversion(get_record_response, config_name):
    _record = tostring(
        get_record_response(standard=standard, config=config_name),
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
