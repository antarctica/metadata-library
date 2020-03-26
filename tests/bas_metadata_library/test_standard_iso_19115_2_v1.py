# noinspection PyUnresolvedReferences
import pytest

from http import HTTPStatus

from jsonschema import ValidationError

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# This is a testing environment, testing against endpoints that don't themselves allow user input, so the XML returned
# should be safe. In any case the test environment is not exposed and so does not present a risk.
from lxml.etree import ElementTree, XML, tostring

from bas_metadata_library.standards.iso_19115_2_v1 import Namespaces, MetadataRecordConfig, MetadataRecord
from bas_metadata_library.standards.iso_19115_2_v1.profiles.inspire_v1_3 import (
    MetadataRecordConfig as InspireMetadataRecordConfig,
)
from bas_metadata_library.standards.iso_19115_2_v1.profiles.uk_pdc_discovery_v1 import (
    MetadataRecordConfig as UKPDCDiscoveryMetadataRecordConfig,
)

from tests.resources.configs.iso19115_2_v1_standard import configs_safe as configs

standard = "iso-19115-2"
namespaces = Namespaces()


@pytest.mark.parametrize(
    "config_class", [MetadataRecordConfig, InspireMetadataRecordConfig, UKPDCDiscoveryMetadataRecordConfig]
)
def test_invalid_configuration(config_class):
    config = {"invalid-configuration": "invalid-configuration"}
    with pytest.raises(ValidationError) as e:
        configuration = config_class(**config)
        configuration.validate()
    assert "'contacts' is a required property" in str(e.value)


@pytest.mark.usefixtures("app_client")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_response(client, config_name):
    response = client.get(f"/standards/{standard}/{config_name}")
    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "text/xml"


@pytest.mark.usefixtures("app_client")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_complete_record(client, config_name):
    with open(f"tests/resources/records/iso-19115-2-v1/{config_name}-record.xml") as expected_contents_file:
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

    metadata_records = record.xpath("/gmi:MI_Metadata", namespaces=namespaces.nsmap())
    assert len(metadata_records) == 1


@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_parse_existing_record(config_name):
    with open(f"tests/resources/records/iso-19115-2-v1/{config_name}-record.xml") as record_file:
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
