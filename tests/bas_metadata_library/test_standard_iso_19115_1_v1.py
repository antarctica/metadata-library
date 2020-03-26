# noinspection PyUnresolvedReferences
import pytest

from copy import deepcopy
from datetime import datetime
from typing import List
from unittest.mock import patch
from http import HTTPStatus

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# This is a testing environment, testing against endpoints that don't themselves allow user input, so the XML returned
# should be safe. In any case the test environment is not exposed and so does not present a risk.
from jsonschema import ValidationError
from lxml.etree import ElementTree, XML, fromstring, tostring

from bas_metadata_library.standards.iso_19115_1_v1 import Namespaces, MetadataRecordConfig, MetadataRecord
from tests.bas_metadata_library.standard_iso_19115_1_v1_common import (
    responsible_party,
    maintenance,
    citation,
    online_resource,
)

from tests.resources.configs.iso19115_1_v1_standard import configs_safe as configs, configs_unsafe as unsafe_configs

standard = "iso-19115-1"
namespaces = Namespaces()


def test_invalid_configuration():
    config = {"invalid-configuration": "invalid-configuration"}
    with pytest.raises(ValidationError) as e:
        configuration = MetadataRecordConfig(**config)
        configuration.validate()
    assert "'contacts' is a required property" in str(e.value)


@pytest.mark.usefixtures("app_client")
@pytest.mark.parametrize("config_name", list(list(configs.keys()) + list(unsafe_configs.keys())))
def test_response(client, config_name):
    with patch(
        "bas_metadata_library.standards.iso_19115_common.data_identification_elements.ResourceConstraints."
        "_get_doi_citation"
    ) as doi_citation:
        doi_citation.return_value = (
            "Campbell, S. (2014). <i>Auster Antarctic aircraft</i>. "
            "University of Alberta Libraries. https://doi.org/10.7939/R3QZ22K64"
        )

        response = client.get(f"/standards/{standard}/{config_name}")
        assert response.status_code == HTTPStatus.OK
        assert response.mimetype == "text/xml"


@pytest.mark.usefixtures("app_client")
@pytest.mark.parametrize("config_name", list(list(configs.keys()) + list(unsafe_configs.keys())))
def test_complete_record(client, config_name):
    with open(f"tests/resources/records/iso-19115-1-v1/{config_name}-record.xml") as expected_contents_file:
        expected_contents = expected_contents_file.read()

    with patch(
        "bas_metadata_library.standards.iso_19115_common.data_identification_elements.ResourceConstraints."
        "_get_doi_citation"
    ) as doi_citation:
        doi_citation.return_value = (
            "Campbell, S. (2014). <i>Auster Antarctic aircraft</i>. "
            "University of Alberta Libraries. https://doi.org/10.7939/R3QZ22K64"
        )

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

    metadata_records = record.xpath("/gmd:MD_Metadata", namespaces=namespaces.nsmap())
    assert len(metadata_records) == 1


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_file_identifier(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "file_identifier" not in config:
        pytest.skip("record does not contain a file identifier")

    file_identifier = record.xpath(
        f"/gmd:MD_Metadata/gmd:fileIdentifier/gco:CharacterString/text() = '{config['file_identifier']}'",
        namespaces=namespaces.nsmap(),
    )
    assert file_identifier is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_language(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "language" not in config:
        pytest.skip("record does not contain a language")

    language_element = record.xpath(
        f"/gmd:MD_Metadata/gmd:language/gmd:LanguageCode[@codeList = "
        f"'http://www.loc.gov/standards/iso639-2/php/code_list.php' and @codeListValue = "
        f"'{config['language']}']/text() = '{config['language']}'",
        namespaces=namespaces.nsmap(),
    )
    assert language_element is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_character_set(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "character_set" not in config:
        pytest.skip("record does not contain a character set")

    character_set_element = record.xpath(
        f"/gmd:MD_Metadata/gmd:characterSet/gmd:MD_CharacterSetCode[@codeList = "
        f"'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/"
        f"gmxCodelists.xml#MD_CharacterSetCode' and @codeListValue = '{config['character_set']}']/text() = "
        f"'{config['character_set']}'",
        namespaces=namespaces.nsmap(),
    )
    assert character_set_element is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_hierarchy_level(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "hierarchy_level" not in config:
        pytest.skip("record does not contain a hierarchy level")

    hierarchy_level_elements = record.xpath(
        f"/gmd:MD_Metadata/gmd:hierarchyLevel/gmd:MD_ScopeCode[@codeList = "
        f"'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/"
        f"gmxCodelists.xml#MD_ScopeCode' and @codeListValue = '{config['hierarchy_level']}']",
        namespaces=namespaces.nsmap(),
    )
    assert len(hierarchy_level_elements) == 1


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_hierarchy_level_name(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "hierarchy_level" not in config:
        pytest.skip("record does not contain a hierarchy level name")

    hierarchy_level_names = record.xpath(
        f"/gmd:MD_Metadata/gmd:hierarchyLevelName/gco:CharacterString/text() = '{config['hierarchy_level']}'",
        namespaces=namespaces.nsmap(),
    )
    assert hierarchy_level_names is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_contact(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "contacts" not in config:
        pytest.skip("record does not contain any contacts")

    contact_elements = record.xpath(
        "/gmd:MD_Metadata/gmd:contact/gmd:CI_ResponsibleParty", namespaces=namespaces.nsmap()
    )
    assert len(contact_elements) == len(config["contacts"])
    if len(config["contacts"]) != 1 or ("roles" in config["contacts"][0] and len(config["contacts"][0]["roles"] != 1)):
        raise NotImplementedError(
            "Testing support for multiple metadata contacts, or a contact with multiple roles, has not yet been added"
        )

    responsible_party(element=contact_elements[0], config=config["contacts"][0])


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_datestamp(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "date_stamp" not in config:
        pytest.skip("record does not contain a datestamp")

    datestamps = record.xpath("/gmd:MD_Metadata/gmd:dateStamp/gco:DateTime/text()", namespaces=namespaces.nsmap())
    assert len(datestamps) == 1
    assert datetime.fromisoformat(datestamps[0]) == config["date_stamp"]


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_metadata_standard(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "metadata_standard" not in config or "name" not in config["metadata_standard"]:
        pytest.skip("record does not contain a metadata standard")

    metadata_standard = record.xpath(
        f"/gmd:MD_Metadata/gmd:metadataStandardName/gco:CharacterString/text() = "
        f"'{config['metadata_standard']['name']}'",
        namespaces=namespaces.nsmap(),
    )
    assert metadata_standard is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_metadata_standard_version(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "metadata_standard" not in config or "version" not in config["metadata_standard"]:
        pytest.skip("record does not contain a metadata standard version")

    metadata_standard_versions = record.xpath(
        f"/gmd:MD_Metadata/gmd:metadataStandardVersion/gco:CharacterString/text() = "
        f"'{config['metadata_standard']['version']}'",
        namespaces=namespaces.nsmap(),
    )
    assert metadata_standard_versions is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_reference_system_info(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "reference_system_info" not in config:
        pytest.skip("record does not contain coordinate reference system information")

    if "authority" in config["reference_system_info"]:
        reference_system_authority_elements = record.xpath(
            "/gmd:MD_Metadata/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/"
            "gmd:RS_Identifier/gmd:authority/gmd:CI_Citation",
            namespaces=namespaces.nsmap(),
        )
        assert len(reference_system_authority_elements) == 1
        citation(element=reference_system_authority_elements[0], config=config["reference_system_info"]["authority"])

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
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_identification_citation(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config:
        pytest.skip("record does not contain a resource citation")

    resource_citation_elements = record.xpath(
        "/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation",
        namespaces=namespaces.nsmap(),
    )
    assert len(resource_citation_elements) == 1
    citation(element=resource_citation_elements[0], config=config["resource"])


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_identification_abstract(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "abstract" not in config["resource"]:
        pytest.skip("record does not contain a resource abstract")

    resource_abstract_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString/text() = "
        f"'{config['resource']['abstract']}'",
        namespaces=namespaces.nsmap(),
    )
    assert resource_abstract_value is True


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
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_identification_points_of_contact(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "contacts" not in config["resource"]:
        pytest.skip("record does not contain any resource points of contact")

    for poc in _resolve_points_of_contact_xpaths(
        point_of_contact_type="points-of-contact", config=config["resource"]["contacts"]
    ):
        # Responsible Party common function expects a single role but config allows multiple so loop through
        # The 'distributor' role is checked for elsewhere in test_distribution_distributors()
        # noinspection PyTypeChecker
        for role in poc["config"]["role"]:
            if role == "distributor":
                continue

            _xpath = poc["xpath"] + f"[gmd:role[gmd:CI_RoleCode[@codeListValue='{role}']]]"
            _config = deepcopy(poc["config"])
            _config["role"] = [role]

            point_of_contact_elements = record.xpath(_xpath, namespaces=namespaces.nsmap())
            assert len(point_of_contact_elements) == 1
            responsible_party(element=point_of_contact_elements[0], config=_config)


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_identification_maintenance(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "maintenance" not in config["resource"]:
        pytest.skip("record does not contain resource maintenance")

    resource_maintenance_elements = record.xpath(
        "/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/"
        "gmd:MD_MaintenanceInformation",
        namespaces=namespaces.nsmap(),
    )
    assert len(resource_maintenance_elements) == 1
    maintenance(element=resource_maintenance_elements[0], config=config["resource"]["maintenance"])


def _resolve_descriptive_keywords_xpaths(config) -> List[dict]:
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
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_identification_descriptive_keywords(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "keywords" not in config["resource"]:
        pytest.skip("record does not contain resource keywords")

    for keyword in _resolve_descriptive_keywords_xpaths(config["resource"]["keywords"]):
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
            citation(element=thesaurus_elements[0], config=keyword["config"]["thesaurus"])


def _resolve_resource_constraints(constraint_type, config):
    if constraint_type == "access" and len(config["resource"]["constraints"]["access"]) >= 1:
        raise NotImplementedError("Testing support for multiple access constraints has not yet been added")
    elif (
        constraint_type == "access"
        and len(config["resource"]["constraints"]["access"]) == 1
        and "restriction_code" not in list(config["resource"]["constraints"]["access"][0].keys())
    ):
        raise NotImplementedError("Testing support for this set of access constraints has not yet been added")
    elif constraint_type == "usage":
        for constraint_config in config:
            if (
                "copyright_licence" not in constraint_config.keys()
                and "required_citation" not in constraint_config.keys()
                and "statement" not in constraint_config.keys()
            ):
                raise NotImplementedError("Testing support for this set of usage constraints has not yet been added")


@pytest.mark.usefixtures("app_client")
@pytest.mark.parametrize("config_name", list(list(configs.keys()) + list(unsafe_configs.keys())))
def test_identification_resource_constraints(client, config_name):
    with patch(
        "bas_metadata_library.standards.iso_19115_common.data_identification_elements.ResourceConstraints."
        "_get_doi_citation"
    ) as doi_citation:
        doi_citation.return_value = (
            "Campbell, S. (2014). <i>Auster Antarctic aircraft</i>. "
            "University of Alberta Libraries. https://doi.org/10.7939/R3QZ22K64"
        )
        response = client.get(f"/standards/{standard}/{config_name}")
        record = fromstring(response.data)
        config = None
        if config_name in configs.keys():
            config = configs[config_name]
        elif config_name in unsafe_configs.keys():
            config = unsafe_configs[config_name]
        if config is None:
            raise RuntimeError(f"Could not load config [{config_name}]")

        if "resource" not in config or "constraints" not in config["resource"]:
            pytest.skip("record does not contain resource constraints")

        if "access" in config["resource"]["constraints"]:
            _resolve_resource_constraints(constraint_type="usage", config=config["resource"]["constraints"]["usage"])

            for access_constraint in config["resource"]["constraints"]["access"]:
                if "restriction_code" in access_constraint.keys():
                    restriction_code_elements = record.xpath(
                        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                        f"gmd:MD_LegalConstraints/gmd:accessConstraints/gmd:MD_RestrictionCode[@codeList = "
                        f"'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/"
                        f"codelist/gmxCodelists.xml#MD_RestrictionCode' and @codeListValue = "
                        f"'{config['resource']['constraints']['access'][0]['restriction_code']}']/text() = "
                        f"'{config['resource']['constraints']['access'][0]['restriction_code']}'",
                        namespaces=namespaces.nsmap(),
                    )
                    assert restriction_code_elements is True

                    if "statement" in config["resource"]["constraints"]["access"][0]:
                        statement_values = record.xpath(
                            f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints"
                            f"/gmd:MD_LegalConstraints[gmd:accessConstraints[gmd:MD_RestrictionCode]]/"
                            f"gmd:otherConstraints/gco:CharacterString/text() = "
                            f"'{config['resource']['constraints']['access'][0]['statement']}'",
                            namespaces=namespaces.nsmap(),
                        )
                        assert statement_values is True

        if "usage" in config["resource"]["constraints"]:
            _resolve_resource_constraints(constraint_type="usage", config=config["resource"]["constraints"]["usage"])

            for usage_constraint in config["resource"]["constraints"]["usage"]:
                if "copyright_licence" in usage_constraint.keys():
                    copyright_licence_value = record.xpath(
                        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                        f"gmd:MD_LegalConstraints[@id='copyright']/gmd:useLimitation/gco:CharacterString/text() | /"
                        f"gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                        f"gmd:MD_LegalConstraints[@id='copyright']/gmd:useLimitation/gmx:Anchor/text()",
                        namespaces=namespaces.nsmap(),
                    )
                    assert len(copyright_licence_value) == 1
                    assert copyright_licence_value[0] == usage_constraint["copyright_licence"]["statement"]

                    if "href" in usage_constraint["copyright_licence"]:
                        copyright_licence_href = record.xpath(
                            f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/"
                            f"gmd:resourceConstraints/gmd:MD_LegalConstraints[@id='copyright']/gmd:useLimitation/"
                            f"gmx:Anchor[@xlink:href = '{usage_constraint['copyright_licence']['href']}']",
                            namespaces=namespaces.nsmap(),
                        )
                        assert len(copyright_licence_href) == 1

                elif (
                    "required_citation" in usage_constraint.keys()
                    and "statement" in usage_constraint["required_citation"]
                ):
                    required_citation_value = record.xpath(
                        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                        f"gmd:MD_LegalConstraints[@id='citation']/gmd:useLimitation/gco:CharacterString/text() = "
                        f"'{usage_constraint['required_citation']['statement']}'",
                        namespaces=namespaces.nsmap(),
                    )
                    assert required_citation_value is True
                elif "required_citation" in usage_constraint.keys() and "doi" in usage_constraint["required_citation"]:
                    required_citation_value = record.xpath(
                        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                        f"gmd:MD_LegalConstraints[@id='citation']/gmd:useLimitation/gco:CharacterString/text() = "
                        f"'Cite this information as \"Campbell, S. (2014). <i>Auster Antarctic aircraft</i>. "
                        f"University of Alberta Libraries. https://doi.org/10.7939/R3QZ22K64\"'",
                        namespaces=namespaces.nsmap(),
                    )
                    assert required_citation_value is True

                elif list(usage_constraint.keys()) == ["statement"]:
                    usage_statement_value = record.xpath(
                        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                        f"gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString/text() = "
                        f"'{usage_constraint['statement']}'",
                        namespaces=namespaces.nsmap(),
                    )
                    assert usage_statement_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_identification_spatial_representation_type(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "spatial_representation_type" not in config["resource"]:
        pytest.skip("record does not contain a resource spatial representation type")

    spatial_representation_type_elements = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/"
        f"gmd:MD_SpatialRepresentationTypeCode[@codeList = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/"
        f"ISO_19139_Schemas/resources/codelist/gmxCodelists.xml#MD_SpatialRepresentationTypeCode' and @codeListValue = "
        f"'{config['resource']['spatial_representation_type']}']/text()  = "
        f"'{config['resource']['spatial_representation_type']}'",
        namespaces=namespaces.nsmap(),
    )
    assert spatial_representation_type_elements is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_identification_spatial_resolution(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "spatial_resolution" not in config["resource"]:
        pytest.skip("record does not contain a resource spatial resolution")

    if config["resource"]["spatial_resolution"] is not None:
        raise NotImplementedError(
            "Testing support for spatial resolutions other than 'inapplicable' has not yet been added"
        )

    spatial_resolution_value = record.xpath(
        "/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution"
        "/gmd:distance/@gco:nilReason = 'inapplicable'",
        namespaces=namespaces.nsmap(),
    )
    assert spatial_resolution_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_identification_language(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "language" not in config["resource"]:
        pytest.skip("record does not contain a resource language")

    language_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language/gmd:LanguageCode"
        f"[@codeList = 'http://www.loc.gov/standards/iso639-2/php/code_list.php' and @codeListValue = "
        f"'{config['resource']['language']}']/text() = '{config['resource']['language']}'",
        namespaces=namespaces.nsmap(),
    )
    assert language_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_identification_topics(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "topics" not in config["resource"]:
        pytest.skip("record does not contain any ISO topics")

    for topic in config["resource"]["topics"]:
        topic_value = record.xpath(
            f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory/"
            f"gmd:MD_TopicCategoryCode/text() = '{topic}'",
            namespaces=namespaces.nsmap(),
        )
        assert topic_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_identification_geographic_bounding_box_extent(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if (
        "resource" not in config
        or "extent" not in config["resource"]
        or "geographic" not in config["resource"]["extent"]
        or "bounding_box" not in config["resource"]["extent"]["geographic"]
    ):
        pytest.skip("record does not contain a geographic bounding box extent")

    west_bounding_box_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal/text() = "
        f"'{config['resource']['extent']['geographic']['bounding_box']['west_longitude']}'",
        namespaces=namespaces.nsmap(),
    )
    assert west_bounding_box_value is True

    east_bounding_box_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal/text() = "
        f"'{config['resource']['extent']['geographic']['bounding_box']['east_longitude']}'",
        namespaces=namespaces.nsmap(),
    )
    assert east_bounding_box_value is True

    south_bounding_box_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal/text() = "
        f"'{config['resource']['extent']['geographic']['bounding_box']['south_latitude']}'",
        namespaces=namespaces.nsmap(),
    )
    assert south_bounding_box_value is True

    north_bounding_box_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal/text() = "
        f"'{config['resource']['extent']['geographic']['bounding_box']['north_latitude']}'",
        namespaces=namespaces.nsmap(),
    )
    assert north_bounding_box_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_identification_temporal_extent(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if (
        "resource" not in config
        or "extent" not in config["resource"]
        or "temporal" not in config["resource"]["extent"]
        or "period" not in config["resource"]["extent"]["temporal"]
    ):
        pytest.skip("record does not contain a temporal period extent")

    temporal_period_start_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod[@gml:id = 'boundingExtent']/"
        f"gml:beginPosition/text() = '{config['resource']['extent']['temporal']['period']['start'].isoformat()}'",
        namespaces=namespaces.nsmap(),
    )
    assert temporal_period_start_value is True

    temporal_period_end_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod[@gml:id = 'boundingExtent']/"
        f"gml:endPosition/text() = '{config['resource']['extent']['temporal']['period']['end'].isoformat()}'",
        namespaces=namespaces.nsmap(),
    )
    assert temporal_period_end_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_identification_vertical_extent(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "extent" not in config["resource"] or "vertical" not in config["resource"]["extent"]:
        pytest.skip("record does not contain a vertical extent")

    vertical_minimum_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:verticalElement/gmd:EX_VerticalExtent/gmd:minimumValue/gco:Real/text() = "
        f"'{config['resource']['extent']['vertical']['minimum']}'",
        namespaces=namespaces.nsmap(),
    )
    assert vertical_minimum_value is True

    vertical_maximum_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:verticalElement/gmd:EX_VerticalExtent/gmd:maximumValue/gco:Real/text() = "
        f"'{config['resource']['extent']['vertical']['maximum']}'",
        namespaces=namespaces.nsmap(),
    )
    assert vertical_maximum_value is True

    vertical_crs_element = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:verticalElement/gmd:EX_VerticalExtent/gmd:verticalCRS/gml:VerticalCRS[@gml:id = "
        f"'{config['resource']['extent']['vertical']['identifier']}'][gml:identifier[text() = "
        f"'{config['resource']['extent']['vertical']['code']}']][gml:name[text() = "
        f"'{config['resource']['extent']['vertical']['name']}']][gml:remarks[text() = "
        f"'{config['resource']['extent']['vertical']['remarks']}']][gml:scope[text() = "
        f"'{config['resource']['extent']['vertical']['scope']}']][gml:domainOfValidity[@xlink:href = "
        f"'{config['resource']['extent']['vertical']['domain_of_validity']['href']}']][gml:verticalCS[@xlink:href = "
        f"'{config['resource']['extent']['vertical']['vertical_cs']['href']}']][gml:verticalDatum[@xlink:href = "
        f"'{config['resource']['extent']['vertical']['vertical_datum']['href']}']]",
        namespaces=namespaces.nsmap(),
    )
    assert len(vertical_crs_element) == 1


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_identification_supplemental_info(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "supplemental" not in config["resource"]:
        pytest.skip("record does not contain supplemental information")

    supplemental_info_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation/"
        f"gco:CharacterString/text() = '{config['resource']['supplemental_information']}'",
        namespaces=namespaces.nsmap(),
    )
    assert supplemental_info_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_distribution_formats(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "formats" not in config["resource"]:
        pytest.skip("record does not contain any distribution formats")

    for _format in config["resource"]["formats"]:
        if "format" in _format.keys():
            format_values = record.xpath(
                f"/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/"
                f"gmd:name/gco:CharacterString/text() | /gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/"
                f"gmd:distributionFormat/gmd:MD_Format/gmd:name/gmx:Anchor/text()",
                namespaces=namespaces.nsmap(),
            )
            assert len(format_values) == 1
            assert format_values[0] == _format["format"]

        if "href" in _format.keys():
            format_href = record.xpath(
                f"/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/"
                f"gmd:name/gmx:Anchor/@xlink:href = '{_format['href']}'",
                namespaces=namespaces.nsmap(),
            )
            assert format_href is True

        if "version" in _format.keys():
            version_values = record.xpath(
                f"/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/"
                f"gmd:version/gmd:version[@gco:nilReason = 'unknown']",
                namespaces=namespaces.nsmap(),
            )
            assert len(version_values) == 1


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_distribution_distributors(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "contacts" not in config["resource"]:
        pytest.skip("record does not contain any resource points of contact")

    for poc in _resolve_points_of_contact_xpaths(
        point_of_contact_type="distributors", config=config["resource"]["contacts"]
    ):
        # Responsible Party common function expects a single role but config allows multiple so loop through
        # Other roles are checked for in test_identification_points_of_contact()
        # noinspection PyTypeChecker
        for role in poc["config"]["role"]:
            if role != "distributor":
                continue

            _xpath = poc["xpath"] + f"[gmd:role[gmd:CI_RoleCode[@codeListValue='{role}']]]"
            _config = deepcopy(poc["config"])
            _config["role"] = [role]

            point_of_contact_elements = record.xpath(_xpath, namespaces=namespaces.nsmap())
            assert len(point_of_contact_elements) == 1
            responsible_party(element=point_of_contact_elements[0], config=_config)


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_distribution_transfer_options(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "transfer_options" not in config["resource"]:
        pytest.skip("record does not contain any transfer options")

    for option in config["resource"]["transfer_options"]:
        if "online_resource" in option.keys():
            option_online_resource_elements = record.xpath(
                f"/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/"
                f"gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource[gmd:linkage[gmd:URL[text() = "
                f"'{option['online_resource']['href']}']]]",
                namespaces=namespaces.nsmap(),
            )
            assert len(option_online_resource_elements) == 1
            online_resource(element=option_online_resource_elements[0], config=option["online_resource"])

        if "size" in option.keys():
            option_size = record.xpath(
                f"/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/"
                f"gmd:MD_DigitalTransferOptions[gmd:unitsOfDistribution[gco:CharacterString[text() = "
                f"'{option['size']['unit']}']]]/gmd:transferSize/gco:Real/text() = '{option['size']['magnitude']}'",
                namespaces=namespaces.nsmap(),
            )
            assert option_size is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_data_quality_scope(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "hierarchy_level" not in config:
        pytest.skip("record does not contain a hierarchy level / scope code")

    scope_code_elements = record.xpath(
        f"/gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:scope/gmd:DQ_Scope/gmd:level/gmd:MD_ScopeCode"
        f"[@codeList = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/"
        f"gmxCodelists.xml#MD_ScopeCode'][@codeListValue = '{config['hierarchy_level']}']/text() = "
        f"'{config['hierarchy_level']}'",
        namespaces=namespaces.nsmap(),
    )
    assert scope_code_elements is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_data_quality_lineage(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "lineage" not in config["resource"]:
        pytest.skip("record does not contain a lineage")

    lineage_values = record.xpath(
        f"/gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement/"
        f"gco:CharacterString/text() = '{config['resource']['lineage']}'",
        namespaces=namespaces.nsmap(),
    )
    assert lineage_values is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_data_quality_measures(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "resource" not in config or "measures" not in config["resource"]:
        pytest.skip("record does not contain any data quality measures")

    for measure in config["resource"]["measures"]:
        if "code" in measure and "code_space" in measure:
            if measure["code"] == "Conformity_001" and measure["code_space"] == "INSPIRE":
                if "pass" in measure:
                    inspire_conformance_result_value = record.xpath(
                        f"/gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_DomainConsistency"
                        f"[gmd:measureIdentification[gmd:RS_Identifier[gmd:code[gco:CharacterString[text() = "
                        f"'{measure['code']}']] and gmd:codeSpace[gco:CharacterString[text() = "
                        f"'{measure['code_space']}']]]]]/gmd:result/gmd:DQ_ConformanceResult/gmd:pass/gco:Boolean/"
                        f"text() = '{str(measure['pass']).lower()}'",
                        namespaces=namespaces.nsmap(),
                    )
                    assert inspire_conformance_result_value is True

                if "explanation" in measure:
                    inspire_conformance_explanation_value = record.xpath(
                        f"/gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_DomainConsistency"
                        f"[gmd:measureIdentification[gmd:RS_Identifier[gmd:code[gco:CharacterString[text() = "
                        f"'{measure['code']}']] and gmd:codeSpace[gco:CharacterString[text() = "
                        f"'{measure['code_space']}']]]]]/gmd:result/gmd:DQ_ConformanceResult/gmd:explanation/"
                        f"gco:CharacterString/text() = '{measure['explanation']}'",
                        namespaces=namespaces.nsmap(),
                    )
                    assert inspire_conformance_explanation_value is True

                if "title" in measure or "dates" in measure:
                    inspire_conformance_citation_element = record.xpath(
                        f"/gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_DomainConsistency"
                        f"[gmd:measureIdentification[gmd:RS_Identifier[gmd:code[gco:CharacterString[text() = "
                        f"'{measure['code']}']] and gmd:codeSpace[gco:CharacterString[text() = "
                        f"'{measure['code_space']}']]]]]/gmd:result/gmd:DQ_ConformanceResult/gmd:specification/"
                        f"gmd:CI_Citation",
                        namespaces=namespaces.nsmap(),
                    )
                    assert len(inspire_conformance_citation_element) == 1
                    citation(element=inspire_conformance_citation_element[0], config=measure)


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_metadata_maintenance(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs[config_name]

    if "maintenance" not in config:
        pytest.skip("record does not contain metadata maintenance")

    metadata_maintenance_elements = record.xpath(
        "/gmd:MD_Metadata/gmd:metadataMaintenance/gmd:MD_MaintenanceInformation", namespaces=namespaces.nsmap()
    )
    assert len(metadata_maintenance_elements) == 1
    maintenance(element=metadata_maintenance_elements[0], config=config["maintenance"])


def test_edgecase_contact_without_email_address():
    config = deepcopy(configs["minimal"])
    config["contacts"][0]["address"] = {}
    config["contacts"][0]["address"]["delivery_point"] = "British Antarctic Survey, High Cross, Madingley Road"
    configuration = MetadataRecordConfig(**config)
    record = MetadataRecord(configuration)
    document = fromstring(record.generate_xml_document())
    contact_email_value = document.xpath(
        "/gmd:MD_Metadata/gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/"
        "gmd:CI_Address/gmd:electronicMailAddress/@gco:nilReason = 'unknown'",
        namespaces=namespaces.nsmap(),
    )
    assert contact_email_value is True


def test_edgecase_citation_with_multiple_roles():
    config = deepcopy(configs["minimal"])
    config["reference_system_info"] = {
        "code": {"value": "urn:ogc:def:crs:EPSG::4326"},
        "authority": {"contact": {"role": ["publisher", "author"]}},
    }
    configuration = MetadataRecordConfig(**config)
    record = MetadataRecord(configuration)
    with pytest.raises(ValueError) as e:
        record.generate_xml_document()

    assert str(e.value) == "Contacts can only have a single role. Citations can only have a single contact."


def test_edgecase_identifier_without_href():
    config = deepcopy(configs["minimal"])
    config["resource"]["identifiers"] = [
        {"identifier": "NE/E007895/1", "title": "award"},
    ]
    configuration = MetadataRecordConfig(**config)
    record = MetadataRecord(configuration)
    document = fromstring(record.generate_xml_document())
    identifier_value = document.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/"
        f"gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text() = "
        f"'{config['resource']['identifiers'][0]['identifier']}'",
        namespaces=namespaces.nsmap(),
    )
    assert identifier_value is True


class MockResponse:
    def raise_for_status(self):
        pass

    # noinspection PyMethodMayBeStatic
    def text(self):
        return (
            "Campbell, S. (2014). <i>Auster Antarctic aircraft</i>. University of Alberta Libraries. "
            "https://doi.org/10.7939/R3QZ22K64"
        )


# noinspection PyUnusedLocal
def mock_response(*args, **kwargs):
    return MockResponse()


def test_edgecase_mocked_doi_lookup():
    with patch(
        "bas_metadata_library.standards.iso_19115_common.data_identification_elements.requests.get",
        side_effect=mock_response,
    ):
        config = deepcopy(unsafe_configs["minimal-required-doi-citation"])
        configuration = MetadataRecordConfig(**config)
        record = MetadataRecord(configuration)
        document = fromstring(record.generate_xml_document())
        assert document is not None


def test_edgecase_distribution_format_with_version():
    config = deepcopy(configs["minimal"])
    config["resource"]["formats"] = [{"format": "test", "version": "test"}]
    configuration = MetadataRecordConfig(**config)
    record = MetadataRecord(configuration)
    document = fromstring(record.generate_xml_document())

    format_version = document.xpath(
        f"/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/"
        f"gmd:version/gco:CharacterString/text() = 'test'",
        namespaces=namespaces.nsmap(),
    )
    assert format_version is True


@pytest.mark.parametrize("config_name", list(configs.keys()))
def test_parse_existing_record(config_name):
    with open(f"tests/resources/records/iso-19115-1-v1/{config_name}-record.xml") as record_file:
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
