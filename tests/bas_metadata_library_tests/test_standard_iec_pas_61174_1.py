from copy import deepcopy
from http import HTTPStatus
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import pytest
from flask.testing import FlaskClient
from jsonschema import ValidationError
from lxml.etree import XML, ElementTree, fromstring, tostring, Element

from bas_metadata_library import RecordValidationError
from bas_metadata_library.standards.iec_pas_61174_1_v1 import (
    MetadataRecord,
    MetadataRecordConfigV1,
    Namespaces,
)
from tests.resources.configs.iec_pas_61174_1_standard import configs_v1

standard = "iec-pas-61174-1"
namespaces = Namespaces()


def test_invalid_configuration_v1():
    config = {"invalid-configuration": "invalid-configuration"}
    with pytest.raises(ValidationError) as e:
        configuration = MetadataRecordConfigV1(**config)
        configuration.validate()
    assert "'route_name' is a required property" in str(e.value)


@pytest.mark.parametrize("route_name", ["route name", "route^name", "route:name"])
def test_edge_case_invalid_configuration_v1_route_name(route_name):
    config = deepcopy(configs_v1["minimal_v1"])
    config["route_name"] = route_name
    with pytest.raises(ValidationError) as e:
        configuration = MetadataRecordConfigV1(**config)
        configuration.validate()
    assert f"'{route_name}' does not match" in str(e.value)


def test_edge_case_invalid_configuration_v1_geometry_type():
    config = deepcopy(configs_v1["minimal_v1"])
    config["waypoints"][0]["leg"] = {"geometry_type": "invalid"}
    with pytest.raises(ValidationError) as e:
        configuration = MetadataRecordConfigV1(**config)
        configuration.validate()
    assert "'invalid' is not one of ['Loxodrome', 'Orthodrome']" in str(e.value)


@pytest.mark.parametrize("config_name", list(configs_v1.keys()))
def test_configuration_v1_from_json_file(config_name):
    configuration = MetadataRecordConfigV1()
    configuration.load(file=Path().resolve().parent.joinpath(f"resources/configs/{standard}/{config_name}.json"))
    configuration.validate()
    assert configuration.config == configs_v1[config_name]


@pytest.mark.parametrize("config_name", list(configs_v1.keys()))
def test_configuration_v1_from_json_string(config_name):
    with open(Path().resolve().parent.joinpath(f"resources/configs/{standard}/{config_name}.json"), mode="r") as file:
        config_str = file.read()
        configuration = MetadataRecordConfigV1()
        configuration.loads(string=config_str)
        configuration.validate()
        assert configuration.config == configs_v1[config_name]


@pytest.mark.parametrize("config_name", list(configs_v1.keys()))
def test_response(app_client: FlaskClient, config_name: str):
    response = app_client.get(f"/standards/{standard}/{config_name}")
    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "text/xml"


@pytest.mark.parametrize("config_name", list(configs_v1.keys()))
def test_complete_record(app_client: FlaskClient, config_name: str):
    with open(
        Path().resolve().parent.joinpath(f"resources/records/iec-pas-61174-1/{config_name}-record.xml"), mode="r"
    ) as expected_contents_file:
        expected_contents = expected_contents_file.read()

    response = app_client.get(f"/standards/{standard}/{config_name}")
    assert response.data.decode() == expected_contents


@pytest.mark.parametrize("config_name", list(configs_v1.keys()))
def test_xml_declaration(app_client: FlaskClient, config_name: str):
    response = app_client.get(f"/standards/{standard}/{config_name}")
    record = ElementTree(XML(response.data))
    assert record.docinfo.xml_version == "1.0"
    assert record.docinfo.encoding == "utf-8"


@pytest.mark.parametrize("config_name", list(configs_v1.keys()))
def test_xml_namespaces(fx_get_record_response: Element, config_name: str):
    record = fx_get_record_response(kind="standards", standard_profile=standard, config=config_name)
    expected_namespaces = Namespaces().nsmap()
    assert record.nsmap == expected_namespaces
    # `None` is used as a key as the RTZ namespace is the root namespace
    assert record.nsmap[None] == "http://www.cirm.org/RTZ/1/2"


@pytest.mark.parametrize("config_name", list(configs_v1.keys()))
def test_root_element(fx_get_record_response: Element, config_name: str):
    record = fx_get_record_response(kind="standards", standard_profile=standard, config=config_name)

    metadata_records = record.xpath("/rtz:route", namespaces=namespaces.nsmap(suppress_root_namespace=True))
    assert len(metadata_records) == 1


def test_standard_version():
    config = MetadataRecordConfigV1(**configs_v1["minimal_v1"])
    record = MetadataRecord(configuration=config)
    document = record.generate_xml_document()
    _record = fromstring(document)

    schema_locations = _record.xpath(
        "/rtz:route/@xsi:schemaLocation", namespaces=namespaces.nsmap(suppress_root_namespace=True)
    )
    route_version = _record.xpath("/rtz:route/@version", namespaces=namespaces.nsmap(suppress_root_namespace=True))
    assert f"https://www.cirm.org/rtz/RTZ%20Schema%20version%201_2.xsd" in schema_locations[0]
    assert float(route_version[0]) == 1.2


@pytest.mark.parametrize("config_name", list(configs_v1.keys()))
def test_parse_existing_record_v1(config_name):
    with Path().resolve().parent.joinpath(f"resources/records/iec-pas-61174-1/{config_name}-record.xml").open() as record_file:
        record_data = record_file.read()

    record = MetadataRecord(record=record_data)
    configuration = record.make_config()
    config = configuration.config
    assert config == configs_v1[config_name]


@pytest.mark.parametrize("config_name", list(configs_v1.keys()))
def test_lossless_conversion_v1(fx_get_record_response: Element, config_name: str):
    _record = tostring(
        fx_get_record_response(kind="standards", standard_profile=standard, config=config_name),
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8",
    ).decode()
    _config = configs_v1[config_name]

    record = MetadataRecord(record=_record)
    config_ = record.make_config()
    config_ = config_.config

    config = MetadataRecordConfigV1(**config_)
    record_ = MetadataRecord(configuration=config).generate_xml_document().decode()
    assert _record == record_
    assert _config == config_


@pytest.mark.parametrize("config_name", list(configs_v1.keys()))
def test_record_schema_validation_valid(config_name: str):
    pass
    config = MetadataRecordConfigV1(**configs_v1[config_name])
    record = MetadataRecord(configuration=config)
    record.validate()
    assert True is True


def test_record_schema_validation_invalid():
    config = deepcopy(MetadataRecordConfigV1(**configs_v1["minimal_v1"]))
    record = MetadataRecord(configuration=config)
    with pytest.raises(RecordValidationError) as e:
        record.attributes["waypoints"][0]["leg"] = {"geometry_type": "invalid"}
        record.validate()
    assert "Record validation failed:" in str(e.value)


def test_rtzp_encode():
    config = MetadataRecordConfigV1(**configs_v1["minimal_v1"])
    record = MetadataRecord(configuration=config)

    with TemporaryDirectory() as tmpdirname:
        rtzp_path = Path(tmpdirname).joinpath("route.rtzp")
        record.generate_rtzp_archive(file=rtzp_path)
        assert rtzp_path.exists()

        with ZipFile(str(rtzp_path), "r") as rtzp_file:
            assert rtzp_file.namelist() == [f"{config.config['route_name']}.rtz"]
            assert (
                rtzp_file.read(f"{config.config['route_name']}.rtz")
                == MetadataRecord(configuration=config).generate_xml_document()
            )


def test_rtzp_decode():
    record = MetadataRecord()
    record.load_from_rtzp_archive(
        file=Path().resolve().parent.joinpath(f"resources/records/iec-pas-61174-1/minimal-v1-record.rtzp")
    )
    config = record.make_config().config
    assert config == configs_v1["minimal_v1"]
