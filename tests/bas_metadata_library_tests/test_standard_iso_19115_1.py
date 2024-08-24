import datetime
import json
from copy import deepcopy
from datetime import date
from http import HTTPStatus
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from flask.testing import FlaskClient
from jsonschema import ValidationError
from lxml.etree import XML, ElementTree, XMLParser, fromstring, tostring

from bas_metadata_library import RecordValidationError
from bas_metadata_library.standards.iso_19115_1 import (
    MetadataRecord,
    MetadataRecordConfigV3,
    Namespaces,
)
from bas_metadata_library.standards.iso_19115_common.utils import encode_date_string, format_numbers_consistently
from tests.bas_metadata_library_tests.standard_iso_19115_1_common import (
    assert_citation,
    assert_identifier,
    assert_maintenance,
    assert_online_resource,
    assert_responsible_party,
)
from tests.resources.configs.iso19115_1_standard import configs_v3_all

standard = "iso-19115-1"
namespaces = Namespaces()


def test_invalid_configuration_v3():
    config = {"invalid-configuration": "invalid-configuration"}
    with pytest.raises(ValidationError) as e:
        configuration = MetadataRecordConfigV3(**config)
        configuration.validate()
    assert "'hierarchy_level' is a required property" in str(e.value)


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_configuration_v3_from_json_file(config_name: str):
    configuration = MetadataRecordConfigV3()
    config_path = Path().resolve().parent.joinpath(f"resources/configs/{standard}/{config_name}.json")
    configuration.load(file=config_path)
    configuration.validate()
    assert configuration.config == configs_v3_all[config_name]


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_configuration_v3_from_json_string(config_name: str):
    with open(Path().resolve().parent.joinpath(f"resources/configs/{standard}/{config_name}.json"), mode="r") as file:
        config_str = file.read()
        configuration = MetadataRecordConfigV3()
        configuration.loads(string=config_str)
        configuration.validate()
        assert configuration.config == configs_v3_all[config_name]


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_configuration_v3_to_json_file(config_name: str):
    configuration = MetadataRecordConfigV3(**configs_v3_all[config_name])

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


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_configuration_v3_to_json_string(config_name: str):
    configuration = MetadataRecordConfigV3(**configs_v3_all[config_name])
    config = configuration.dumps()

    with Path().resolve().parent.joinpath(f"resources/configs/{standard}/{config_name}.json").open() as _config_file:
        _config = _config_file.read().rstrip("\n")

    assert config == _config


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_configuration_v3_json_round_trip(config_name: str):
    configuration = MetadataRecordConfigV3(**configs_v3_all[config_name])
    config = configuration.dumps()
    _config = MetadataRecordConfigV3()
    _config.loads(config)
    assert configuration.config == _config.config


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_response(app_client: FlaskClient, config_name: str):
    response = app_client.get(f"/standards/{standard}/{config_name}")
    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "text/xml"


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_complete_record(app_client: FlaskClient, config_name: str):
    with open(
        Path().resolve().parent.joinpath(f"resources/records/{standard}/{config_name}-record.xml"), mode="r"
    ) as expected_contents_file:
        expected_contents = expected_contents_file.read()
        response = app_client.get(f"/standards/{standard}/{config_name}")
        assert response.data.decode() == expected_contents


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_xml_declaration(app_client: FlaskClient, config_name: str):
    response = app_client.get(f"/standards/{standard}/{config_name}")
    record = ElementTree(XML(response.data))
    assert record.docinfo.xml_version == "1.0"
    assert record.docinfo.encoding == "utf-8"


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_xml_namespaces(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    expected_namespaces = Namespaces().nsmap()
    assert record.nsmap == expected_namespaces


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_root_element(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)

    metadata_records = record.xpath("/gmd:MD_Metadata", namespaces=namespaces.nsmap())
    assert len(metadata_records) == 1


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_file_identifier(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "file_identifier" not in config:
        pytest.skip("record does not contain a file identifier")

    file_identifier = record.xpath(
        f"/gmd:MD_Metadata/gmd:fileIdentifier/gco:CharacterString/text() = '{config['file_identifier']}'",
        namespaces=namespaces.nsmap(),
    )
    assert file_identifier is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_language(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "metadata" not in config or "language" not in config["metadata"]:
        pytest.skip("record does not contain a metadata language")

    # noinspection HttpUrlsUsage
    language_element = record.xpath(
        f"/gmd:MD_Metadata/gmd:language/gmd:LanguageCode[@codeList = "
        f"'http://www.loc.gov/standards/iso639-2/php/code_list.php' and @codeListValue = "
        f"'{config['metadata']['language']}']/text() = '{config['metadata']['language']}'",
        namespaces=namespaces.nsmap(),
    )
    assert language_element is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_character_set(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "metadata" not in config or "character_set" not in config["metadata"]:
        pytest.skip("record does not contain a metadata character set")

    # noinspection HttpUrlsUsage
    character_set_element = record.xpath(
        f"/gmd:MD_Metadata/gmd:characterSet/gmd:MD_CharacterSetCode[@codeList = "
        f"'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/"
        f"gmxCodelists.xml#MD_CharacterSetCode' and @codeListValue = '{config['metadata']['character_set']}']/text() = "
        f"'{config['metadata']['character_set']}'",
        namespaces=namespaces.nsmap(),
    )
    assert character_set_element is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_hierarchy_level(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "hierarchy_level" not in config:
        pytest.skip("record does not contain a hierarchy level")

    hierarchy_level_elements = record.xpath(
        f"/gmd:MD_Metadata/gmd:hierarchyLevel/gmd:MD_ScopeCode[@codeList = "
        f"'https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_ScopeCode' and "
        f"@codeListValue = '{config['hierarchy_level']}']",
        namespaces=namespaces.nsmap(),
    )
    assert len(hierarchy_level_elements) == 1


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_hierarchy_level_name(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "hierarchy_level" not in config:
        pytest.skip("record does not contain a hierarchy level name")

    hierarchy_level_names = record.xpath(
        f"/gmd:MD_Metadata/gmd:hierarchyLevelName/gco:CharacterString/text() = '{config['hierarchy_level']}'",
        namespaces=namespaces.nsmap(),
    )
    assert hierarchy_level_names is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_contact(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "metadata" not in config or "contacts" not in config["metadata"]:
        pytest.skip("record does not contain any metadata contacts")

    contact_elements = record.xpath(
        "/gmd:MD_Metadata/gmd:contact/gmd:CI_ResponsibleParty", namespaces=namespaces.nsmap()
    )
    assert len(contact_elements) == len(config["metadata"]["contacts"])
    if len(config["metadata"]["contacts"]) != 1 or (
        "roles" in config["metadata"]["contacts"][0] and len(config["metadata"]["contacts"][0]["roles"] != 1)
    ):
        raise NotImplementedError(
            "Testing support for multiple metadata contacts, or a contact with multiple roles, has not yet been added"
        )

    assert_responsible_party(element=contact_elements[0], config=config["metadata"]["contacts"][0])


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_datestamp(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "metadata" not in config or "date_stamp" not in config["metadata"]:
        pytest.skip("record does not contain a metadata datestamp")

    datestamps = record.xpath("/gmd:MD_Metadata/gmd:dateStamp/gco:Date/text()", namespaces=namespaces.nsmap())
    assert len(datestamps) == 1
    assert date.fromisoformat(datestamps[0]) == config["metadata"]["date_stamp"]


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_metadata_standard(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if (
        "metadata" not in config
        or "metadata_standard" not in config["metadata"]
        or "name" not in config["metadata"]["metadata_standard"]
    ):
        pytest.skip("record does not contain a metadata standard")

    metadata_standard = record.xpath(
        f"/gmd:MD_Metadata/gmd:metadataStandardName/gco:CharacterString/text() = "
        f"'{config['metadata']['metadata_standard']['name']}'",
        namespaces=namespaces.nsmap(),
    )
    assert metadata_standard is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_metadata_standard_version(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if (
        "metadata" not in config
        or "metadata_standard" not in config["metadata"]
        or "version" not in config["metadata"]["metadata_standard"]
    ):
        pytest.skip("record does not contain a metadata standard version")

    metadata_standard_versions = record.xpath(
        f"/gmd:MD_Metadata/gmd:metadataStandardVersion/gco:CharacterString/text() = "
        f"'{config['metadata']['metadata_standard']['version']}'",
        namespaces=namespaces.nsmap(),
    )
    assert metadata_standard_versions is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_reference_system_info(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "reference_system_info" not in config:
        pytest.skip("record does not contain coordinate reference system information")

    if "authority" in config["reference_system_info"]:
        reference_system_authority_elements = record.xpath(
            "/gmd:MD_Metadata/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/"
            "gmd:RS_Identifier/gmd:authority/gmd:CI_Citation",
            namespaces=namespaces.nsmap(),
        )
        assert len(reference_system_authority_elements) == 1
        assert_citation(
            element=reference_system_authority_elements[0], config=config["reference_system_info"]["authority"]
        )

    if "code" in config["reference_system_info"]:
        reference_system_code_elements = record.xpath(
            "/gmd:MD_Metadata/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/"
            "gmd:RS_Identifier/gmd:code/gmx:Anchor | /gmd:MD_Metadata/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/"
            "gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString",
            namespaces=namespaces.nsmap(),
        )
        assert len(reference_system_code_elements) == 1

        if "value" in config["reference_system_info"]["code"]:
            reference_system_code_values = reference_system_code_elements[0].xpath(
                f"text() = '{config['reference_system_info']['code']['value']}'", namespaces=namespaces.nsmap()
            )
            assert reference_system_code_values is True

        if "href" in config["reference_system_info"]["code"]:
            reference_system_code_href = reference_system_code_elements[0].xpath(
                f"@xlink:href = '{config['reference_system_info']['code']['href']}'", namespaces=namespaces.nsmap()
            )
            assert reference_system_code_href is True

        if "title" in config["reference_system_info"]["code"]:
            reference_system_code_title = reference_system_code_elements[0].xpath(
                f"@xlink:title = '{config['reference_system_info']['code']['title']}'", namespaces=namespaces.nsmap()
            )
            assert reference_system_code_title is True

    if "version" in config["reference_system_info"]:
        reference_system_version_value = record.xpath(
            f"/gmd:MD_Metadata/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/"
            f"gmd:RS_Identifier/gmd:version/gco:CharacterString/text() = "
            f"'{config['reference_system_info']['version']}'",
            namespaces=namespaces.nsmap(),
        )
        assert reference_system_version_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_citation(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config:
        pytest.skip("record does not contain an identification citation")

    identification_citation_elements = record.xpath(
        "/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation",
        namespaces=namespaces.nsmap(),
    )
    assert len(identification_citation_elements) == 1
    assert_citation(element=identification_citation_elements[0], config=config["identification"])


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_abstract(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config or "abstract" not in config["identification"]:
        pytest.skip("record does not contain an identification abstract")

    identification_abstract_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString/text() = "
        f"'{config['identification']['abstract']}'",
        namespaces=namespaces.nsmap(),
    )
    assert identification_abstract_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_purpose(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config or "purpose" not in config["identification"]:
        pytest.skip("record does not contain an identification purpose")

    identification_purpose_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:purpose/gco:CharacterString/text() = "
        f"'{config['identification']['purpose']}'",
        namespaces=namespaces.nsmap(),
    )
    assert identification_purpose_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_credit(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config or "credit" not in config["identification"]:
        pytest.skip("record does not contain an identification credit")

    identification_credit_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:credit/gco:CharacterString/text() = "
        f"'{config['identification']['credit']}'",
        namespaces=namespaces.nsmap(),
    )
    assert identification_credit_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_status(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config or "status" not in config["identification"]:
        pytest.skip("record does not contain an identification status")

    status_elements = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:status/"
        f"gmd:MD_ProgressCode[@codeList = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/"
        f"ISO_19139_Schemas/resources/codelist/gmxCodelists.xml#MD_ProgressCode' and @codeListValue = "
        f"'{config['identification']['status']}']/text()  = "
        f"'{config['identification']['status']}'",
        namespaces=namespaces.nsmap(),
    )
    assert status_elements is True


# noinspection PyUnboundLocalVariable
def _resolve_points_of_contact_xpaths(point_of_contact_type, config):
    pocs = []
    for poc in config:
        if point_of_contact_type != "points-of-contact" and point_of_contact_type != "distributors":
            raise NotImplementedError("Testing support for this type of point of contact has not yet been added")
        elif point_of_contact_type == "points-of-contact":
            xpath = (
                "/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/"
                "gmd:CI_ResponsibleParty"
            )
        elif point_of_contact_type == "distributors":
            xpath = (
                "/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/"
                "gmd:distributorContact/gmd:CI_ResponsibleParty"
            )

        if "email" in poc:
            xpath = (
                xpath + f"[gmd:contactInfo[gmd:CI_Contact[gmd:address[gmd:CI_Address[gmd:electronicMailAddress"
                f"[gco:CharacterString[text() = '{poc['email']}']]]]]]]"
            )

        if "individual" in poc and "name" in poc["individual"]:
            xpath = (
                xpath + f"[gmd:individualName[gco:CharacterString[text() = '{poc['individual']['name']}'] or "
                f"gmx:Anchor[text() = '{poc['individual']['name']}']]]"
            )

        if "organisation" in poc and "name" in poc["organisation"]:
            xpath = (
                xpath + f"[gmd:organisationName[gco:CharacterString[text() = '{poc['organisation']['name']}'] or "
                f"gmx:Anchor[text() = '{poc['organisation']['name']}']]]"
            )

        pocs.append({"xpath": xpath, "config": poc})

    return pocs


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_points_of_contact(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config or "contacts" not in config["identification"]:
        pytest.skip("record does not contain any identification points of contact")

    for poc in _resolve_points_of_contact_xpaths(
        point_of_contact_type="points-of-contact", config=config["identification"]["contacts"]
    ):
        # Responsible Party common function expects a single role but config allows multiple so loop through
        # The 'distributor' role is checked for elsewhere in test_distributions()
        # noinspection PyTypeChecker
        for role in poc["config"]["role"]:
            if role == "distributor":
                continue

            _xpath = poc["xpath"] + f"[gmd:role[gmd:CI_RoleCode[@codeListValue='{role}']]]"
            _config = deepcopy(poc["config"])
            _config["role"] = [role]

            point_of_contact_elements = record.xpath(_xpath, namespaces=namespaces.nsmap())
            assert len(point_of_contact_elements) == 1
            assert_responsible_party(element=point_of_contact_elements[0], config=_config)


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_maintenance(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config or "maintenance" not in config["identification"]:
        pytest.skip("record does not contain identification maintenance")

    identification_maintenance_elements = record.xpath(
        "/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/"
        "gmd:MD_MaintenanceInformation",
        namespaces=namespaces.nsmap(),
    )
    assert len(identification_maintenance_elements) == 1
    assert_maintenance(element=identification_maintenance_elements[0], config=config["identification"]["maintenance"])


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_graphic_overviews(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config or "graphic_overviews" not in config["identification"]:
        pytest.skip("record does not contain graphic overviews")

    for graphic_overview in config["identification"]["graphic_overviews"]:
        graphic_overview_elements = record.xpath(
            f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:graphicOverview/gmd:MD_BrowseGraphic[@id='{graphic_overview['identifier']}']",
            namespaces=namespaces.nsmap(),
        )
        assert len(graphic_overview_elements) == 1

        href_element = graphic_overview_elements[0].xpath(
            f"./gmd:fileName/gco:CharacterString/text() = '{graphic_overview['href']}'",
            namespaces=namespaces.nsmap(),
        )
        assert href_element is True

        if "description" in graphic_overview:
            description_element = graphic_overview_elements[0].xpath(
                f"./gmd:fileDescription/gco:CharacterString/text() = '{graphic_overview['description']}'",
                namespaces=namespaces.nsmap(),
            )
            assert description_element is True

        if "mime_type" in graphic_overview:
            mime_type_element = graphic_overview_elements[0].xpath(
                f"./gmd:fileType/gco:CharacterString/text() = '{graphic_overview['mime_type']}'",
                namespaces=namespaces.nsmap(),
            )
            assert mime_type_element is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_resource_formats(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config or "resource_formats" not in config["identification"]:
        pytest.skip("record does not contain resource formats")

    for resource_format in config["identification"]["resource_formats"]:
        resource_format_elements = record.xpath(
            f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceFormat/gmd:MD_Format[gmd:name[gco:CharacterString[text()='{resource_format['format']}']]]",
            namespaces=namespaces.nsmap(),
        )
        assert len(resource_format_elements) == 1

        format_name_element = resource_format_elements[0].xpath(
            f"./gmd:name/gco:CharacterString/text() = '{resource_format['format']}'",
            namespaces=namespaces.nsmap(),
        )
        assert format_name_element is True

        if "version" in resource_format:
            version_element = resource_format_elements[0].xpath(
                f"./gmd:version/gco:CharacterString/text() = '{resource_format['version']}'",
                namespaces=namespaces.nsmap(),
            )
            assert version_element is True

        if "amendment_number" in resource_format:
            amendment_number_element = resource_format_elements[0].xpath(
                f"./gmd:amendmentNumber/gco:CharacterString/text() = '{resource_format['amendment_number']}'",
                namespaces=namespaces.nsmap(),
            )
            assert amendment_number_element is True

        if "specification" in resource_format:
            specification_element = resource_format_elements[0].xpath(
                f"./gmd:specification/gco:CharacterString/text() = '{resource_format['specification']}'",
                namespaces=namespaces.nsmap(),
            )
            assert specification_element is True

        if "file_decompression_technique" in resource_format:
            file_decompression_technique_element = resource_format_elements[0].xpath(
                f"./gmd:fileDecompressionTechnique/gco:CharacterString/text() = '{resource_format['file_decompression_technique']}'",
                namespaces=namespaces.nsmap(),
            )
            assert file_decompression_technique_element is True


def _resolve_descriptive_keywords_xpaths(config) -> list[dict]:
    keywords = []
    for keyword in config:
        xpath = (
            "/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords"
        )

        if "thesaurus" in keyword:
            xpath = (
                xpath + f"[gmd:thesaurusName[gmd:CI_Citation[gmd:title[gco:CharacterString[text() = "
                f"'{keyword['thesaurus']['title']['value']}'] or gmx:Anchor[text() = "
                f"'{keyword['thesaurus']['title']['value']}']]]]]"
            )

        if "terms" in keyword and len(keyword["terms"]) > 0:
            if "href" in keyword["terms"][0]:
                xpath = xpath + f"[gmd:keyword[gmx:Anchor[@xlink:href = '{keyword['terms'][0]['href']}']]]"
            if "term" in keyword["terms"][0]:
                xpath = (
                    xpath + f"[gmd:keyword[gco:CharacterString[text() = '{keyword['terms'][0]['term']}'] or "
                    f"gmx:Anchor[text() = '{keyword['terms'][0]['term']}']]]"
                )

        keywords.append({"xpath": xpath, "config": keyword})

    return keywords


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_descriptive_keywords(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config or "keywords" not in config["identification"]:
        pytest.skip("record does not contain identification keywords")

    for keyword in _resolve_descriptive_keywords_xpaths(config["identification"]["keywords"]):
        descriptive_keywords_elements = record.xpath(keyword["xpath"], namespaces=namespaces.nsmap())
        assert len(descriptive_keywords_elements) == 1

        if "terms" in keyword["config"]:
            for keyword_term in keyword["config"]["terms"]:
                if "term" in keyword_term:
                    term_values = descriptive_keywords_elements[0].xpath(
                        f"./gmd:keyword[gco:CharacterString[text() = '{keyword_term['term']}'] or gmx:Anchor[text() = "
                        f"'{keyword_term['term']}']]",
                        namespaces=namespaces.nsmap(),
                    )
                    assert len(term_values) == 1
                if "href" in keyword_term:
                    term_hrefs = descriptive_keywords_elements[0].xpath(
                        f"./gmd:keyword[gmx:Anchor[@xlink:href = '{keyword_term['href']}']]",
                        namespaces=namespaces.nsmap(),
                    )
                    assert len(term_hrefs) == 1

        if "type" in keyword["config"]:
            # noinspection HttpUrlsUsage
            type_value = descriptive_keywords_elements[0].xpath(
                f"./gmd:type/gmd:MD_KeywordTypeCode[@codeList = 'http://standards.iso.org/ittf/"
                f"PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/gmxCodelists.xml#MD_KeywordTypeCode' "
                f"and @codeListValue = '{keyword['config']['type']}']/text() = '{keyword['config']['type']}'",
                namespaces=namespaces.nsmap(),
            )
            assert type_value is True

        if "thesaurus" in keyword["config"]:
            thesaurus_elements = descriptive_keywords_elements[0].xpath(
                "./gmd:thesaurusName/gmd:CI_Citation", namespaces=namespaces.nsmap()
            )
            assert len(thesaurus_elements) == 1
            assert_citation(element=thesaurus_elements[0], config=keyword["config"]["thesaurus"])


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_resource_constraints(app_client: FlaskClient, config_name: str):
    response = app_client.get(f"/standards/{standard}/{config_name}")
    record = fromstring(response.data)
    config = configs_v3_all[config_name]

    if "identification" not in config or "constraints" not in config["identification"]:
        pytest.skip("record does not contain identification resource constraints")

    for constraint in config["identification"]["constraints"]:
        constraint_element = "gmd:accessConstraints"
        if constraint["type"] == "usage":
            constraint_element = "gmd:useConstraints"

        restriction_code_elements = record.xpath(
            f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
            f"gmd:MD_LegalConstraints/{constraint_element}/gmd:MD_RestrictionCode[@codeList = "
            f"'https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_RestrictionCode' "
            f"and @codeListValue = '{constraint['restriction_code']}']/text() = '{constraint['restriction_code']}'",
            namespaces=namespaces.nsmap(),
        )
        assert restriction_code_elements is True

        if "statement" not in constraint and "href" not in constraint and "permissions" not in constraint:
            continue

        if "statement" in constraint and "href" not in constraint and "permissions" not in constraint:
            other_constraint_statement = record.xpath(
                f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                f"gmd:MD_LegalConstraints/gmd:otherConstraints/gco:CharacterString/text() = '{constraint['statement']}'",
                namespaces=namespaces.nsmap(),
            )
            assert other_constraint_statement is True

        if "statement" in constraint and "href" in constraint and "permissions" not in constraint:
            other_constraint_statement = record.xpath(
                f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                f"gmd:MD_LegalConstraints/gmd:otherConstraints/gmx:Anchor/text() = '{constraint['statement']}'",
                namespaces=namespaces.nsmap(),
            )
            assert other_constraint_statement is True

            other_constraint_href = record.xpath(
                f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                f"gmd:MD_LegalConstraints/gmd:otherConstraints/gmx:Anchor/@xlink:href = '{constraint['href']}'",
                namespaces=namespaces.nsmap(),
            )
            assert other_constraint_href is True

        if "statement" not in constraint and "href" in constraint and "permissions" not in constraint:
            other_constraint_href = record.xpath(
                f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                f"gmd:MD_LegalConstraints/gmd:otherConstraints/gmx:Anchor/@xlink:href = '{constraint['href']}'",
                namespaces=namespaces.nsmap(),
            )
            assert other_constraint_href is True

        if "statement" not in constraint and "href" not in constraint and "permissions" in constraint:
            legal_constraint_id_elements = record.xpath(
                f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                f"gmd:MD_LegalConstraints[contains(@id,'permissions')]",
                namespaces=namespaces.nsmap(),
            )
            assert len(legal_constraint_id_elements) >= 1

            _statement = constraint["permissions"]
            if not isinstance(_statement, str):
                _statement = json.dumps(_statement)

            other_constraint_statement = record.xpath(
                f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                f"gmd:MD_LegalConstraints/gmd:otherConstraints/gco:CharacterString/text() = '{_statement}'",
                namespaces=namespaces.nsmap(),
            )
            assert other_constraint_statement is True


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_aggregations(app_client: FlaskClient, config_name: str):
    response = app_client.get(f"/standards/{standard}/{config_name}")
    record = fromstring(response.data)
    config = configs_v3_all[config_name]

    if "identification" not in config or "aggregations" not in config["identification"]:
        pytest.skip("record does not contain identification aggregations")

    base_xpath = f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:aggregationInfo/gmd:MD_AggregateInformation"
    for aggregation in config["identification"]["aggregations"]:
        xpath = (
            base_xpath
            + f"[gmd:aggregateDataSetIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString[text()='{aggregation['identifier']['identifier']}'] "
            f"| gmd:aggregateDataSetIdentifier/gmd:RS_Identifier/gmd:code/gmx:Anchor[text()='{aggregation['identifier']['identifier']}']]"
        )
        association_elements = record.xpath(xpath, namespaces=namespaces.nsmap())
        assert len(association_elements) == 1
        association_element = association_elements[0]

        if "association_type" in aggregation.keys():
            association_type_element = association_element.xpath(
                f"./gmd:associationType/gmd:DS_AssociationTypeCode[@codeList = 'https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#DS_AssociationTypeCode' and @codeListValue = '{aggregation['association_type']}']/text() = '{aggregation['association_type']}'",
                namespaces=namespaces.nsmap(),
            )
            assert association_type_element is True

        if "initiative_type" in aggregation.keys():
            initiative_type_element = association_element.xpath(
                f"./gmd:initiativeType/gmd:DS_InitiativeTypeCode[@codeList = 'https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#DS_InitiativeTypeCode' and @codeListValue = '{aggregation['initiative_type']}']/text() = '{aggregation['initiative_type']}'",
                namespaces=namespaces.nsmap(),
            )
            assert initiative_type_element is True

        if "identifier" in aggregation.keys():
            assert_identifier(
                element=association_element,
                config=aggregation["identifier"],
                identifier_container="gmd:aggregateDataSetIdentifier",
            )


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_spatial_representation_type(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config or "spatial_representation_type" not in config["identification"]:
        pytest.skip("record does not contain an identification spatial representation type")

    # noinspection HttpUrlsUsage
    spatial_representation_type_elements = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/"
        f"gmd:MD_SpatialRepresentationTypeCode[@codeList = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/"
        f"ISO_19139_Schemas/resources/codelist/gmxCodelists.xml#MD_SpatialRepresentationTypeCode' and @codeListValue = "
        f"'{config['identification']['spatial_representation_type']}']/text()  = "
        f"'{config['identification']['spatial_representation_type']}'",
        namespaces=namespaces.nsmap(),
    )
    assert spatial_representation_type_elements is True


def _test_identification_spatial_resolution(record, config):
    if "identification" not in config or "spatial_resolution" not in config["identification"]:
        pytest.skip("record does not contain an identification spatial resolution")

    if config["identification"]["spatial_resolution"] is None:
        spatial_resolution_value = record.xpath(
            "/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/@gco:nilReason = 'inapplicable'",
            namespaces=namespaces.nsmap(),
        )
    elif config["identification"]["spatial_resolution"] is not None:
        spatial_resolution_value = record.xpath(
            f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer/text() = '{config['identification']['spatial_resolution']}'",
            namespaces=namespaces.nsmap(),
        )
    else:
        spatial_resolution_value = False

    assert spatial_resolution_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_spatial_resolution(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]
    _test_identification_spatial_resolution(record=record, config=config)


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_character_set(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config or "character_set" not in config["identification"]:
        pytest.skip("record does not contain an identification character set")

    # noinspection HttpUrlsUsage
    character_string_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:characterSet/gmd:MD_CharacterSetCode/text() = '{config['identification']['character_set']}'",
        namespaces=namespaces.nsmap(),
    )
    assert character_string_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_language(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config or "language" not in config["identification"]:
        pytest.skip("record does not contain an identification language")

    # noinspection HttpUrlsUsage
    language_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language/gmd:LanguageCode"
        f"[@codeList = 'http://www.loc.gov/standards/iso639-2/php/code_list.php' and @codeListValue = "
        f"'{config['identification']['language']}']/text() = '{config['identification']['language']}'",
        namespaces=namespaces.nsmap(),
    )
    assert language_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_topics(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config or "topics" not in config["identification"]:
        pytest.skip("record does not contain any ISO topics")

    for topic in config["identification"]["topics"]:
        topic_value = record.xpath(
            f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory/"
            f"gmd:MD_TopicCategoryCode/text() = '{topic}'",
            namespaces=namespaces.nsmap(),
        )
        assert topic_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_geographic_extent_bounding_box(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if (
        "identification" not in config
        or "extent" not in config["identification"]
        or "geographic" not in config["identification"]["extent"]
        or "bounding_box" not in config["identification"]["extent"]["geographic"]
    ):
        pytest.skip("record does not contain a geographic extent bounding box")

    bounding_box_xpath = (
        "/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        "gmd:geographicElement/gmd:EX_GeographicBoundingBox[@id = 'boundingGeographicExtent']"
    )

    west_bounding_box_value = record.xpath(
        f"{bounding_box_xpath}/gmd:westBoundLongitude/gco:Decimal/text() = "
        f"'{config['identification']['extent']['geographic']['bounding_box']['west_longitude']}'",
        namespaces=namespaces.nsmap(),
    )
    assert west_bounding_box_value is True

    east_bounding_box_value = record.xpath(
        f"{bounding_box_xpath}/gmd:eastBoundLongitude/gco:Decimal/text() = "
        f"'{config['identification']['extent']['geographic']['bounding_box']['east_longitude']}'",
        namespaces=namespaces.nsmap(),
    )
    assert east_bounding_box_value is True

    south_bounding_box_value = record.xpath(
        f"{bounding_box_xpath}/gmd:southBoundLatitude/gco:Decimal/text() = "
        f"'{config['identification']['extent']['geographic']['bounding_box']['south_latitude']}'",
        namespaces=namespaces.nsmap(),
    )
    assert south_bounding_box_value is True

    north_bounding_box_value = record.xpath(
        f"{bounding_box_xpath}/gmd:northBoundLatitude/gco:Decimal/text() = "
        f"'{config['identification']['extent']['geographic']['bounding_box']['north_latitude']}'",
        namespaces=namespaces.nsmap(),
    )
    assert north_bounding_box_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_geographic_extent_identifier(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if (
        "identification" not in config
        or "extent" not in config["identification"]
        or "geographic" not in config["identification"]["extent"]
        or "identifier" not in config["identification"]["extent"]["geographic"]
    ):
        pytest.skip("record does not contain a geographic extent identifier")

    geographic_extent_identifier_elements = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicDescription",
        namespaces=namespaces.nsmap(),
    )
    assert len(geographic_extent_identifier_elements) == 1
    assert_identifier(
        element=geographic_extent_identifier_elements[0],
        config=config["identification"]["extent"]["geographic"]["identifier"],
        identifier_container="gmd:geographicIdentifier",
    )


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_temporal_extent(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if (
        "identification" not in config
        or "extent" not in config["identification"]
        or "temporal" not in config["identification"]["extent"]
        or "period" not in config["identification"]["extent"]["temporal"]
    ):
        pytest.skip("record does not contain a temporal period extent")

    _date_precision = None
    if "date_precision" in config["identification"]["extent"]["temporal"]["period"]["start"]:
        _date_precision = config["identification"]["extent"]["temporal"]["period"]["start"]["date_precision"]
    _start_value = encode_date_string(
        date_datetime=config["identification"]["extent"]["temporal"]["period"]["start"]["date"],
        date_precision=_date_precision,
    )
    temporal_period_start_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod[@gml:id = 'boundingTemporalExtent']/"
        f"gml:beginPosition/text() = '{_start_value}'",
        namespaces=namespaces.nsmap(),
    )
    assert temporal_period_start_value is True

    _date_precision = None
    if "date_precision" in config["identification"]["extent"]["temporal"]["period"]["end"]:
        _date_precision = config["identification"]["extent"]["temporal"]["period"]["end"]["date_precision"]
    _end_value = encode_date_string(
        date_datetime=config["identification"]["extent"]["temporal"]["period"]["end"]["date"],
        date_precision=_date_precision,
    )
    temporal_period_end_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod[@gml:id = 'boundingTemporalExtent']/"
        f"gml:endPosition/text() = '{_end_value}'",
        namespaces=namespaces.nsmap(),
    )
    assert temporal_period_end_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_vertical_extent(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if (
        "identification" not in config
        or "extent" not in config["identification"]
        or "vertical" not in config["identification"]["extent"]
    ):
        pytest.skip("record does not contain a vertical extent")

    vertical_minimum_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:verticalElement/gmd:EX_VerticalExtent/gmd:minimumValue/gco:Real/text() = "
        f"'{config['identification']['extent']['vertical']['minimum']}'",
        namespaces=namespaces.nsmap(),
    )
    assert vertical_minimum_value is True

    vertical_maximum_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:verticalElement/gmd:EX_VerticalExtent/gmd:maximumValue/gco:Real/text() = "
        f"'{config['identification']['extent']['vertical']['maximum']}'",
        namespaces=namespaces.nsmap(),
    )
    assert vertical_maximum_value is True

    vertical_crs_element = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:verticalElement/gmd:EX_VerticalExtent/gmd:verticalCRS/gml:VerticalCRS[@gml:id = "
        f"'{config['identification']['extent']['vertical']['identifier']}'][gml:identifier[text() = "
        f"'{config['identification']['extent']['vertical']['code']}']][gml:name[text() = "
        f"'{config['identification']['extent']['vertical']['name']}']][gml:remarks[text() = "
        f"'{config['identification']['extent']['vertical']['remarks']}']][gml:scope[text() = "
        f"'{config['identification']['extent']['vertical']['scope']}']][gml:domainOfValidity[@xlink:href = "
        f"'{config['identification']['extent']['vertical']['domain_of_validity']['href']}']][gml:verticalCS[@xlink:href = "
        f"'{config['identification']['extent']['vertical']['vertical_cs']['href']}']][gml:verticalDatum[@xlink:href = "
        f"'{config['identification']['extent']['vertical']['vertical_datum']['href']}']]",
        namespaces=namespaces.nsmap(),
    )
    assert len(vertical_crs_element) == 1


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_identification_supplemental_info(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config or "supplemental_information" not in config["identification"]:
        pytest.skip("record does not contain supplemental information")

    supplemental_info_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation/"
        f"gco:CharacterString/text() = '{config['identification']['supplemental_information']}'",
        namespaces=namespaces.nsmap(),
    )
    assert supplemental_info_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_distributions(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]
    xpath_base = "/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor"

    if "distribution" not in config:
        pytest.skip("record does not contain any distributions")

    for distribution_option in config["distribution"]:
        distribution_elements = record.xpath(
            f"{xpath_base}[gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString/text() = '{distribution_option['distributor']['organisation']['name']}'] | "
            f"{xpath_base}[gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:organisationName/gmx:Anchor/text() = '{distribution_option['distributor']['organisation']['name']}' ]",
            namespaces=namespaces.nsmap(),
        )
        assert len(distribution_elements) == 1
        distribution_element = distribution_elements[0]

        # distributor
        # (other roles are checked for in `test_identification_points_of_contact()`)
        distributor_elements = distribution_element.xpath(
            f"{xpath_base}/gmd:distributorContact/gmd:CI_ResponsibleParty[gmd:organisationName/gco:CharacterString/text() = '{distribution_option['distributor']['organisation']['name']}'] | "
            f"{xpath_base}/gmd:distributorContact/gmd:CI_ResponsibleParty[gmd:organisationName/gmx:Anchor/text() = '{distribution_option['distributor']['organisation']['name']}']",
            namespaces=namespaces.nsmap(),
        )
        assert len(distributor_elements) == 1
        assert_responsible_party(element=distributor_elements[0], config=distribution_option["distributor"])

        # format
        if "format" in distribution_option["format"]:
            format_values = distribution_element.xpath(
                f"./gmd:distributorFormat/gmd:MD_Format/gmd:name[gco:CharacterString/text() = '{distribution_option['format']['format']}'] | "
                f"./gmd:distributorFormat/gmd:MD_Format/gmd:name[gmx:Anchor/text() = '{distribution_option['format']['format']}']",
                namespaces=namespaces.nsmap(),
            )
            assert len(format_values) == 1

            if "href" in distribution_option["format"]:
                format_hrefs = distribution_element.xpath(
                    f"./gmd:distributorFormat/gmd:MD_Format/gmd:name/gmx:Anchor/@xlink:href = '{distribution_option['format']['href']}'",
                    namespaces=namespaces.nsmap(),
                )
                assert format_hrefs is True
            if "version" in distribution_option["format"]:
                format_versions = distribution_element.xpath(
                    f"./gmd:distributorFormat/gmd:MD_Format/gmd:version/gco:CharacterString/text() = '{distribution_option['format']['version']}'",
                    namespaces=namespaces.nsmap(),
                )
                assert format_versions is True
            if "version" not in distribution_option["format"]:
                format_version = distribution_element.xpath(
                    f"./gmd:distributorFormat/gmd:MD_Format/gmd:version/@gco:nilReason = 'missing'",
                    namespaces=namespaces.nsmap(),
                )
                assert format_version is True

        # transfer options
        if "online_resource" in distribution_option["transfer_option"]:
            option_online_resource_elements = distribution_element.xpath(
                f"./gmd:distributorTransferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource[gmd:linkage[gmd:URL[text() = '{distribution_option['transfer_option']['online_resource']['href']}']]]",
                namespaces=namespaces.nsmap(),
            )
            assert len(option_online_resource_elements) == 1
            assert_online_resource(
                element=option_online_resource_elements[0],
                config=distribution_option["transfer_option"]["online_resource"],
            )

            if "size" in distribution_option["transfer_option"]:
                _magnitude = format_numbers_consistently(distribution_option["transfer_option"]["size"]["magnitude"])
                option_size = distribution_element.xpath(
                    f"./gmd:distributorTransferOptions/gmd:MD_DigitalTransferOptions[gmd:unitsOfDistribution[gco:CharacterString[text() = '{distribution_option['transfer_option']['size']['unit']}']]]/gmd:transferSize/gco:Real/text() = '{_magnitude}'",
                    namespaces=namespaces.nsmap(),
                )
                assert option_size is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_data_quality_scope(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "hierarchy_level" not in config:
        pytest.skip("record does not contain a hierarchy level / scope code")

    scope_code_elements = record.xpath(
        f"/gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:scope/gmd:DQ_Scope/gmd:level/gmd:MD_ScopeCode"
        f"[@codeList = 'https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_ScopeCode']"
        f"[@codeListValue = '{config['hierarchy_level']}']/text() = '{config['hierarchy_level']}'",
        namespaces=namespaces.nsmap(),
    )
    assert scope_code_elements is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_data_quality_lineage(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "identification" not in config or "lineage" not in config["identification"]:
        pytest.skip("record does not contain a lineage")

    # note: this should be refactored to have a dedicated Statement and Source element when lineage sources are
    # added properly [#73]
    lineage_values = record.xpath(
        f"/gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement/"
        f"gco:CharacterString/text() = '{config['identification']['lineage']['statement']}'",
        namespaces=namespaces.nsmap(),
    )
    assert lineage_values is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_metadata_maintenance(get_record_response, config_name: str):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_v3_all[config_name]

    if "metadata" not in config or "maintenance" not in config["metadata"]:
        pytest.skip("record does not contain metadata maintenance")

    metadata_maintenance_elements = record.xpath(
        "/gmd:MD_Metadata/gmd:metadataMaintenance/gmd:MD_MaintenanceInformation", namespaces=namespaces.nsmap()
    )
    assert len(metadata_maintenance_elements) == 1
    assert_maintenance(element=metadata_maintenance_elements[0], config=config["metadata"]["maintenance"])


def test_edge_case_contact_without_email_address():
    config = deepcopy(configs_v3_all["minimal_v3"])
    config["metadata"]["contacts"][0]["address"] = {}
    config["metadata"]["contacts"][0]["address"]["delivery_point"] = (
        "British Antarctic Survey, High Cross, Madingley Road"
    )
    configuration = MetadataRecordConfigV3(**config)
    record = MetadataRecord(configuration)
    document = fromstring(record.generate_xml_document())
    contact_email_value = document.xpath(
        "/gmd:MD_Metadata/gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/"
        "gmd:CI_Address/gmd:electronicMailAddress/@gco:nilReason = 'unknown'",
        namespaces=namespaces.nsmap(),
    )
    assert contact_email_value is True


def test_edge_case_citation_with_multiple_roles():
    config = deepcopy(configs_v3_all["minimal_v3"])
    config["reference_system_info"] = {
        "code": {"value": "urn:ogc:def:crs:EPSG::4326"},
        "authority": {"contact": {"individual": {"name": "foo"}, "role": ["publisher", "author"]}},
    }
    configuration = MetadataRecordConfigV3(**config)
    record = MetadataRecord(configuration)
    with pytest.raises(ValueError) as e:
        record.generate_xml_document()

    assert str(e.value) == "Contacts can only have a single role. Citations can only have a single contact."


def test_edge_case_identifier_without_href():
    config = deepcopy(configs_v3_all["minimal_v3"])
    config["identification"]["identifiers"] = [
        {"identifier": "NE/E007895/1", "namespace": "award"},
    ]
    configuration = MetadataRecordConfigV3(**config)
    record = MetadataRecord(configuration)
    document = fromstring(record.generate_xml_document())
    identifier_value = document.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/"
        f"gmd:identifier/gmd:RS_Identifier/gmd:code/gco:CharacterString/text() = "
        f"'{config['identification']['identifiers'][0]['identifier']}'",
        namespaces=namespaces.nsmap(),
    )
    assert identifier_value is True


def test_edge_case_datestamp_invalid_date():
    with open(
        Path().resolve().parent.joinpath(f"resources/records/{standard}/minimal_v3-record.xml"), mode="r"
    ) as record_file:
        record_data = record_file.read()
    record_element = XML(record_data.encode(), parser=XMLParser(remove_blank_text=True))
    record_data = tostring(record_element).decode()
    record_data = record_data.replace(
        "<gmd:dateStamp><gco:Date>2018-10-18</gco:Date></gmd:dateStamp>",
        "<gmd:dateStamp><gco:Date>?NotADate?</gco:Date></gmd:dateStamp>",
    )
    record = MetadataRecord(record=record_data)
    with pytest.raises(RuntimeError) as e:
        record.make_config()
    assert e.value.args[0] == "Datestamp could not be parsed as an ISO date value"


def test_edge_case_spatial_resolution_null():
    config = deepcopy(configs_v3_all["complete_v3"])
    config["identification"]["spatial_resolution"] = None
    config_ = MetadataRecordConfigV3(**config)
    record = MetadataRecord(configuration=config_).generate_xml_document()
    record = fromstring(record)

    _test_identification_spatial_resolution(record=record, config=config)


def test_edge_case_date_invalid_date():
    with open(
        Path().resolve().parent.joinpath(f"resources/records/{standard}/minimal_v3-record.xml"), mode="r"
    ) as record_file:
        record_data = record_file.read()
    record_element = XML(record_data.encode(), parser=XMLParser(remove_blank_text=True))
    record_data = tostring(record_element).decode()
    record_data = record_data.replace(
        '<gmd:CI_Date><gmd:date><gco:Date>2018</gco:Date></gmd:date><gmd:dateType><gmd:CI_DateTypeCode codeList="https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_DateTypeCode" codeListValue="creation">creation</gmd:CI_DateTypeCode></gmd:dateType></gmd:CI_Date>',
        '<gmd:CI_Date><gmd:date><gco:Date>?NotADate?</gco:Date></gmd:date><gmd:dateType><gmd:CI_DateTypeCode codeList="https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_DateTypeCode" codeListValue="creation">creation</gmd:CI_DateTypeCode></gmd:dateType></gmd:CI_Date>',
    )
    record = MetadataRecord(record=record_data)
    with pytest.raises(RuntimeError) as e:
        record.make_config()
    assert e.value.args[0] == "Date/datetime could not be parsed as an ISO date value"


def test_edge_case_temporal_extent_begin_invalid_date():
    with open(
        Path().resolve().parent.joinpath(f"resources/records/{standard}/minimal_v3-record.xml"), mode="r"
    ) as record_file:
        record_data = record_file.read()
    record_element = XML(record_data.encode(), parser=XMLParser(remove_blank_text=True))
    record_data = tostring(record_element).decode()
    record_data = record_data.replace(
        "</gmd:EX_Extent>",
        '<gmd:temporalElement><gmd:EX_TemporalExtent><gmd:extent><gml:TimePeriod gml:id="boundingExtent"><gml:beginPosition>?NotADate?</gml:beginPosition><gml:endPosition>2018-03</gml:endPosition></gml:TimePeriod></gmd:extent></gmd:EX_TemporalExtent></gmd:temporalElement></gmd:EX_Extent>',
    )
    record = MetadataRecord(record=record_data)
    with pytest.raises(RuntimeError) as e:
        record.make_config()
    assert e.value.args[0] == "Date/datetime could not be parsed as an ISO date value"


def test_edge_case_temporal_extent_end_invalid_date():
    with open(
        Path().resolve().parent.joinpath(f"resources/records/{standard}/minimal_v3-record.xml"), mode="r"
    ) as record_file:
        record_data = record_file.read()
    record_element = XML(record_data.encode(), parser=XMLParser(remove_blank_text=True))
    record_data = tostring(record_element).decode()
    record_data = record_data.replace(
        "</gmd:EX_Extent>",
        '<gmd:temporalElement><gmd:EX_TemporalExtent><gmd:extent><gml:TimePeriod gml:id="boundingExtent"><gml:beginPosition>2018-03-15T00:00:00</gml:beginPosition><gml:endPosition>?NotADate?</gml:endPosition></gml:TimePeriod></gmd:extent></gmd:EX_TemporalExtent></gmd:temporalElement></gmd:EX_Extent>',
    )
    record = MetadataRecord(record=record_data)
    with pytest.raises(RuntimeError) as e:
        record.make_config()
    assert e.value.args[0] == "Date/datetime could not be parsed as an ISO date value"


def test_edge_case_temporal_extent_begin_missing_date():
    with open(
        Path().resolve().parent.joinpath(f"resources/records/{standard}/minimal_v3-record.xml"), mode="r"
    ) as record_file:
        record_data = record_file.read()
    record_element = XML(record_data.encode(), parser=XMLParser(remove_blank_text=True))
    record_data = tostring(record_element).decode()
    record_data = record_data.replace(
        "</gmd:EX_Extent>",
        '<gmd:temporalElement><gmd:EX_TemporalExtent><gmd:extent><gml:TimePeriod gml:id="boundingExtent"><gml:endPosition>2018-03</gml:endPosition></gml:TimePeriod></gmd:extent></gmd:EX_TemporalExtent></gmd:temporalElement></gmd:EX_Extent>',
    )
    record = MetadataRecord(record=record_data)
    config = record.make_config().config
    assert "end" in config["identification"]["extents"][0]["temporal"]["period"]


_distributor = {
    "organisation": {"name": "UK Polar Data Centre"},
    "phone": "+44 (0)1223 221400",
    "address": {
        "delivery_point": "British Antarctic Survey, High Cross, Madingley Road",
        "city": "Cambridge",
        "administrative_area": "Cambridgeshire",
        "postal_code": "CB3 0ET",
        "country": "United Kingdom",
    },
    "email": "polardatacentre@bas.ac.uk",
    "role": ["distributor"],
}


def test_edge_case_distribution_option_format_no_properties():
    config = deepcopy(configs_v3_all["minimal_v3"])
    config["distribution"] = [
        {
            "distributor": _distributor,
            "format": {"format": "netCDF"},
            "transfer_option": {
                "online_resource": {
                    "href": "https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
                    "title": "Get Data",
                    "description": "Download measurement data",
                    "function": "download",
                }
            },
        }
    ]
    config = MetadataRecordConfigV3(**config)
    record = MetadataRecord(configuration=config).generate_xml_document().decode()
    record_element = XML(record.encode(), parser=XMLParser(remove_blank_text=True))
    record = tostring(record_element).decode()
    record = record.replace(
        '<gmd:MD_Format id="bml-7c0728ad873c8067873930212a8658fa1f010120-fmt"><gmd:name><gco:CharacterString>netCDF</gco:CharacterString></gmd:name><gmd:version gco:nilReason="missing"/></gmd:MD_Format>',
        '<gmd:MD_Format id="bml-7c0728ad873c8067873930212a8658fa1f010120-fmt"></gmd:MD_Format>',
    )
    _record = MetadataRecord(record=record)
    _config = _record.make_config()
    assert _record.make_config().config["distribution"][0] == {
        "distributor": _distributor,
        "transfer_option": {
            "online_resource": {
                "href": "https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
                "title": "Get Data",
                "description": "Download measurement data",
                "function": "download",
            }
        },
    }


def test_edge_case_distribution_option_transfer_options_no_properties():
    config = deepcopy(configs_v3_all["minimal_v3"])
    config["distribution"] = [
        {
            "distributor": _distributor,
            "format": {"format": "netCDF"},
            "transfer_option": {
                "online_resource": {
                    "href": "https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
                    "title": "Get Data",
                    "description": "Download measurement data",
                    "function": "download",
                }
            },
        }
    ]
    config = MetadataRecordConfigV3(**config)
    record = MetadataRecord(configuration=config).generate_xml_document().decode()
    record_element = XML(record.encode(), parser=XMLParser(remove_blank_text=True))
    record = tostring(record_element).decode()
    record = record.replace(
        '<gmd:MD_DigitalTransferOptions id="bml-7c0728ad873c8067873930212a8658fa1f010120-tfo"><gmd:onLine><gmd:CI_OnlineResource><gmd:linkage><gmd:URL>https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=b1a7d1b5-c419-41e7-9178-b1ffd76d5371</gmd:URL></gmd:linkage><gmd:name><gco:CharacterString>Get Data</gco:CharacterString></gmd:name><gmd:description><gco:CharacterString>Download measurement data</gco:CharacterString></gmd:description><gmd:function><gmd:CI_OnLineFunctionCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/gmxCodelists.xml#CI_OnLineFunctionCode" codeListValue="download">download</gmd:CI_OnLineFunctionCode></gmd:function></gmd:CI_OnlineResource></gmd:onLine></gmd:MD_DigitalTransferOptions>',
        '<gmd:MD_DigitalTransferOptions id="bml-7c0728ad873c8067873930212a8658fa1f010120-tfo"></gmd:MD_DigitalTransferOptions>',
    )
    _record = MetadataRecord(record=record)
    _config = _record.make_config()
    assert _record.make_config().config["distribution"][0] == {
        "distributor": _distributor,
        "format": {"format": "netCDF"},
    }


def test_edge_case_distribution_option_no_id():
    config = deepcopy(configs_v3_all["minimal_v3"])
    config["distribution"] = [
        {
            "distributor": _distributor,
            "format": {"format": "netCDF"},
            "transfer_option": {
                "online_resource": {
                    "href": "https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
                    "title": "Get Data",
                    "description": "Download measurement data",
                    "function": "download",
                }
            },
        }
    ]
    config = MetadataRecordConfigV3(**config)
    record = MetadataRecord(configuration=config).generate_xml_document().decode()
    record_element = XML(record.encode(), parser=XMLParser(remove_blank_text=True))
    record = tostring(record_element).decode()
    record = record.replace('<gmd:MD_Format id="bml-7c0728ad873c8067873930212a8658fa1f010120-fmt">', "<gmd:MD_Format>")
    record = record.replace(
        '<gmd:MD_DigitalTransferOptions id="bml-7c0728ad873c8067873930212a8658fa1f010120-tfo">',
        "<gmd:MD_DigitalTransferOptions>",
    )
    _record = MetadataRecord(record=record)
    _config = _record.make_config()
    assert _config.config["distribution"] == [
        {"distributor": _distributor, "format": {"format": "netCDF"}},
        {
            "distributor": _distributor,
            "transfer_option": {
                "online_resource": {
                    "href": "https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
                    "title": "Get Data",
                    "description": "Download measurement data",
                    "function": "download",
                }
            },
        },
    ]


def test_edge_case_distribution_option_more_formats_than_transfer_options():
    config = deepcopy(configs_v3_all["minimal_v3"])
    config["distribution"] = [
        {
            "distributor": _distributor,
            "format": {"format": "blue"},
            "transfer_option": {"online_resource": {"href": "https://example.com/blue"}},
        },
        {
            "distributor": _distributor,
            "format": {"format": "red"},
            "transfer_option": {"online_resource": {"href": "https://example.com/red"}},
        },
    ]
    config = MetadataRecordConfigV3(**config)
    record = MetadataRecord(configuration=config)
    del record.attributes["distribution"][1]["transfer_option"]
    record = record.generate_xml_document().decode()
    _record = MetadataRecord(record=record)
    _config = _record.make_config()
    assert _config.config["distribution"] == [
        {
            "distributor": _distributor,
            "format": {"format": "blue"},
            "transfer_option": {"online_resource": {"href": "https://example.com/blue"}},
        },
        {
            "distributor": _distributor,
            "format": {"format": "red"},
        },
    ]


def test_edge_case_distribution_option_more_transfer_options_than_formats():
    config = deepcopy(configs_v3_all["minimal_v3"])
    config["distribution"] = [
        {
            "distributor": _distributor,
            "format": {"format": "blue"},
            "transfer_option": {"online_resource": {"href": "https://example.com/blue"}},
        },
        {
            "distributor": _distributor,
            "format": {"format": "red"},
            "transfer_option": {"online_resource": {"href": "https://example.com/red"}},
        },
    ]
    config = MetadataRecordConfigV3(**config)
    record = MetadataRecord(configuration=config)
    del record.attributes["distribution"][1]["format"]
    record = record.generate_xml_document().decode()
    _record = MetadataRecord(record=record)
    _config = _record.make_config()
    assert _config.config["distribution"] == [
        {
            "distributor": _distributor,
            "format": {"format": "blue"},
            "transfer_option": {"online_resource": {"href": "https://example.com/blue"}},
        },
        {"distributor": _distributor, "transfer_option": {"online_resource": {"href": "https://example.com/red"}}},
    ]


def test_edge_case_distribution_option_transfer_option_size_no_unit():
    config = deepcopy(configs_v3_all["minimal_v3"])
    config["distribution"] = [
        {
            "distributor": _distributor,
            "format": {"format": "netCDF"},
            "transfer_option": {
                "online_resource": {
                    "href": "https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=b1a7d1b5-c419-41e7-9178-b1ffd76d5371",
                    "title": "Get Data",
                    "description": "Download measurement data",
                    "function": "download",
                },
                "size": {"magnitude": 40.0},
            },
        }
    ]
    config = MetadataRecordConfigV3(**config)
    record = MetadataRecord(configuration=config)
    record = record.generate_xml_document().decode()
    _record = MetadataRecord(record=record)
    _config = _record.make_config()
    assert _config.config["distribution"][0]["transfer_option"]["size"] == {"magnitude": 40}


def test_edge_case_citation_title_anchor_no_value_with_href():
    config = deepcopy(configs_v3_all["complete_v3"])
    config["identification"]["keywords"] = [
        {
            "terms": [
                {"term": "Atmospheric conditions", "href": "https://www.eionet.europa.eu/gemet/en/inspire-theme/ac"}
            ],
            "type": "theme",
            "thesaurus": {
                "title": {
                    "value": "General Multilingual Environmental Thesaurus - INSPIRE themes",
                    "href": "http://www.eionet.europa.eu/gemet/inspire_themes",
                },
                "dates": {"publication": {"date": datetime.date(2018, 8, 16)}},
                "edition": "4.1.2",
                "contact": {
                    "organisation": {
                        "name": "European Environment Information and Observation Network (EIONET), European Environment Agency (EEA)"
                    },
                    "email": "helpdesk@eionet.europa.eu",
                    "online_resource": {
                        "href": "https://www.eionet.europa.eu/gemet/en/themes/",
                        "title": "General Multilingual Environmental Thesaurus (GEMET) themes",
                        "function": "information",
                    },
                    "role": ["publisher"],
                },
            },
        }
    ]
    config = MetadataRecordConfigV3(**config)
    record = MetadataRecord(configuration=config)
    record = record.generate_xml_document().decode()
    record_element = XML(record.encode(), parser=XMLParser(remove_blank_text=True))
    record = tostring(record_element).decode()
    record = record.replace("General Multilingual Environmental Thesaurus - INSPIRE themes", "")
    _record = MetadataRecord(record=record)
    _config = _record.make_config()
    assert _config.config["identification"]["keywords"][0]["thesaurus"]["title"] == {
        "href": "http://www.eionet.europa.eu/gemet/inspire_themes"
    }


@pytest.mark.parametrize("contact_type", ["individual", "organisation"])
def test_edge_case_responsible_party_anchor_no_value_with_href(contact_type):
    config = deepcopy(configs_v3_all["complete_v3"])
    config["metadata"]["contacts"][0][contact_type] = {"name": "*Name to be removed*", "href": "*Test value*"}
    config = MetadataRecordConfigV3(**config)
    record = MetadataRecord(configuration=config)
    record = record.generate_xml_document().decode()
    record_element = XML(record.encode(), parser=XMLParser(remove_blank_text=True))
    record = tostring(record_element).decode()
    record = record.replace("*Name to be removed*", "")
    _record = MetadataRecord(record=record)
    _config = _record.make_config()
    assert _config.config["metadata"]["contacts"][0][contact_type] == {"href": "*Test value*"}


@pytest.mark.parametrize(
    "address_config",
    [
        {
            "city": "Cambridge",
            "administrative_area": "Cambridgeshire",
            "postal_code": "CB3 0ET",
            "country": "United Kingdom",
        },
        {
            "administrative_area": "Cambridgeshire",
            "postal_code": "CB3 0ET",
            "country": "United Kingdom",
        },
        {
            "postal_code": "CB3 0ET",
            "country": "United Kingdom",
        },
        {
            "country": "United Kingdom",
        },
    ],
)
def test_edge_case_responsible_party_incomplete_address(address_config):
    config = deepcopy(configs_v3_all["complete_v3"])
    config["metadata"]["contacts"][0]["address"] = address_config
    config = MetadataRecordConfigV3(**config)
    record = MetadataRecord(configuration=config)
    record = record.generate_xml_document().decode()
    _record = MetadataRecord(record=record)
    _config = _record.make_config()
    assert _config.config["metadata"]["contacts"][0]["address"] == address_config


def test_edge_case_parse_config_year_only_date_no_precision():
    _config = deepcopy(configs_v3_all["minimal_v3"])
    _config["metadata"]["date_stamp"] = "2018-10-18"
    _config["identification"]["dates"]["creation"] = {"date": "2018"}
    _config = json.dumps(_config)
    config = MetadataRecordConfigV3()
    config.loads(string=_config)
    assert config.config["identification"]["dates"]["creation"] == {
        "date": date(2018, 1, 1),
        "date_precision": "year",
    } or {
        "date_precision": "year",
        "date": date(2018, 1, 1),
    }


class MockResponse:
    def raise_for_status(self):
        pass

    # noinspection PyMethodMayBeStatic
    def text(self):
        return (
            "Campbell, S. (2014). <i>Auster Antarctic aircraft</i>. University of Alberta Libraries. "
            "https://doi.org/10.7939/R3QZ22K64"
        )


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_parse_existing_record_v3(config_name: str):
    with open(
        Path().resolve().parent.joinpath(f"resources/records/{standard}/{config_name}-record.xml"), mode="r"
    ) as record_file:
        record_data = record_file.read()

    record = MetadataRecord(record=record_data)
    configuration = record.make_config()
    config = configuration.config
    assert config == configs_v3_all[config_name]


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_lossless_conversion_v3(get_record_response, config_name: str):
    _record = tostring(
        get_record_response(standard=standard, config=config_name),
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8",
    ).decode()
    _config = configs_v3_all[config_name]

    record = MetadataRecord(record=_record)
    config_ = record.make_config().config

    config = MetadataRecordConfigV3(**config_)
    record_ = MetadataRecord(configuration=config).generate_xml_document().decode()
    assert _record == record_
    assert _config == config_


@pytest.mark.parametrize("config_name", list(configs_v3_all.keys()))
def test_record_schema_validation_valid(config_name: str):
    config = MetadataRecordConfigV3(**configs_v3_all[config_name])
    record = MetadataRecord(configuration=config)
    record.validate()
    assert True is True


def test_record_schema_validation_invalid():
    config = deepcopy(MetadataRecordConfigV3(**configs_v3_all["minimal_v3"]))
    record = MetadataRecord(configuration=config)
    with pytest.raises(RecordValidationError) as e:
        record.attributes["identification"]["spatial_resolution"] = "invalid"
        record.validate()
    assert "Record validation failed:" in str(e.value)
