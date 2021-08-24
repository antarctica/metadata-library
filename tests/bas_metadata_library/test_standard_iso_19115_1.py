# noinspection PyUnresolvedReferences
import pytest

from copy import deepcopy
from datetime import date
from typing import List
from unittest.mock import patch
from http import HTTPStatus

from jsonschema import ValidationError
from backports.datetime_fromisoformat import MonkeyPatch

# Workaround for lack of `date(time).fromisoformat()` method in Python 3.6
MonkeyPatch.patch_fromisoformat()

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# This is a testing environment, testing against endpoints that don't themselves allow user input, so the XML returned
# should be safe. In any case the test environment is not exposed and so does not present a risk.
from lxml.etree import ElementTree, XML, fromstring, tostring

from bas_metadata_library.standards.iso_19115_1 import (
    Namespaces,
    MetadataRecordConfigV1,
    MetadataRecordConfigV2,
    MetadataRecord,
)
from tests.bas_metadata_library.standard_iso_19115_1_common import (
    responsible_party,
    maintenance,
    citation,
    online_resource,
)

from tests.resources.configs.iso19115_1_standard import (
    configs_safe_v1,
    configs_safe_v2,
    configs_unsafe_v2,
    configs_v2_all,
)

standard = "iso-19115-1"
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


@pytest.mark.usefixtures("app_client")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_response(client, config_name):
    with patch(
        "bas_metadata_library.standards.iso_19115_common.data_identification_elements.ResourceConstraint."
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
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_complete_record(client, config_name):
    with open(f"tests/resources/records/iso-19115-1/{config_name}-record.xml") as expected_contents_file:
        expected_contents = expected_contents_file.read()

    with patch(
        "bas_metadata_library.standards.iso_19115_common.data_identification_elements.ResourceConstraint."
        "_get_doi_citation"
    ) as doi_citation:
        doi_citation.return_value = (
            "Campbell, S. (2014). <i>Auster Antarctic aircraft</i>. "
            "University of Alberta Libraries. https://doi.org/10.7939/R3QZ22K64"
        )

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

    metadata_records = record.xpath("/gmd:MD_Metadata", namespaces=namespaces.nsmap())
    assert len(metadata_records) == 1


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_file_identifier(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "file_identifier" not in config:
        pytest.skip("record does not contain a file identifier")

    file_identifier = record.xpath(
        f"/gmd:MD_Metadata/gmd:fileIdentifier/gco:CharacterString/text() = '{config['file_identifier']}'",
        namespaces=namespaces.nsmap(),
    )
    assert file_identifier is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_language(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "metadata" not in config or "language" not in config["metadata"]:
        pytest.skip("record does not contain a metadata language")

    language_element = record.xpath(
        f"/gmd:MD_Metadata/gmd:language/gmd:LanguageCode[@codeList = "
        f"'http://www.loc.gov/standards/iso639-2/php/code_list.php' and @codeListValue = "
        f"'{config['metadata']['language']}']/text() = '{config['metadata']['language']}'",
        namespaces=namespaces.nsmap(),
    )
    assert language_element is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_character_set(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "metadata" not in config or "character_set" not in config["metadata"]:
        pytest.skip("record does not contain a metadata character set")

    character_set_element = record.xpath(
        f"/gmd:MD_Metadata/gmd:characterSet/gmd:MD_CharacterSetCode[@codeList = "
        f"'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/"
        f"gmxCodelists.xml#MD_CharacterSetCode' and @codeListValue = '{config['metadata']['character_set']}']/text() = "
        f"'{config['metadata']['character_set']}'",
        namespaces=namespaces.nsmap(),
    )
    assert character_set_element is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_hierarchy_level(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

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
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_hierarchy_level_name(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "hierarchy_level" not in config:
        pytest.skip("record does not contain a hierarchy level name")

    hierarchy_level_names = record.xpath(
        f"/gmd:MD_Metadata/gmd:hierarchyLevelName/gco:CharacterString/text() = '{config['hierarchy_level']}'",
        namespaces=namespaces.nsmap(),
    )
    assert hierarchy_level_names is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_contact(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

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

    responsible_party(element=contact_elements[0], config=config["metadata"]["contacts"][0])


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_datestamp(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "metadata" not in config or "date_stamp" not in config["metadata"]:
        pytest.skip("record does not contain a metadata datestamp")

    datestamps = record.xpath("/gmd:MD_Metadata/gmd:dateStamp/gco:Date/text()", namespaces=namespaces.nsmap())
    assert len(datestamps) == 1
    assert date.fromisoformat(datestamps[0]) == config["metadata"]["date_stamp"]


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_metadata_standard(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

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
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_metadata_standard_version(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

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
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_reference_system_info(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

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
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_identification_citation(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "identification" not in config:
        pytest.skip("record does not contain a identification citation")

    identification_citation_elements = record.xpath(
        "/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation",
        namespaces=namespaces.nsmap(),
    )
    assert len(identification_citation_elements) == 1
    citation(element=identification_citation_elements[0], config=config["identification"])


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_identification_abstract(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "identification" not in config or "abstract" not in config["identification"]:
        pytest.skip("record does not contain a identification abstract")

    identification_abstract_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString/text() = "
        f"'{config['identification']['abstract']}'",
        namespaces=namespaces.nsmap(),
    )
    assert identification_abstract_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_identification_credit(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "identification" not in config or "credit" not in config["identification"]:
        pytest.skip("record does not contain an identification credit")

    identification_credit_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:credit/gco:CharacterString/text() = "
        f"'{config['identification']['credit']}'",
        namespaces=namespaces.nsmap(),
    )
    assert identification_credit_value is True


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
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_identification_points_of_contact(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "identification" not in config or "contacts" not in config["identification"]:
        pytest.skip("record does not contain any identification points of contact")

    for poc in _resolve_points_of_contact_xpaths(
        point_of_contact_type="points-of-contact", config=config["identification"]["contacts"]
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
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_identification_maintenance(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "identification" not in config or "maintenance" not in config["identification"]:
        pytest.skip("record does not contain identification maintenance")

    identification_maintenance_elements = record.xpath(
        "/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/"
        "gmd:MD_MaintenanceInformation",
        namespaces=namespaces.nsmap(),
    )
    assert len(identification_maintenance_elements) == 1
    maintenance(element=identification_maintenance_elements[0], config=config["identification"]["maintenance"])


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
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_identification_descriptive_keywords(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

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


@pytest.mark.usefixtures("app_client")
@pytest.mark.parametrize("config_name", list(configs_v2_all.keys()))
def test_identification_resource_constraints(client, config_name):
    with patch(
        "bas_metadata_library.standards.iso_19115_common.data_identification_elements.ResourceConstraint."
        "_get_doi_citation"
    ) as doi_citation:
        doi_citation.return_value = (
            "Campbell, S. (2014). <i>Auster Antarctic aircraft</i>. "
            "University of Alberta Libraries. https://doi.org/10.7939/R3QZ22K64"
        )
        response = client.get(f"/standards/{standard}/{config_name}")
        record = fromstring(response.data)
        config = configs_v2_all[config_name]

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

            if "statement" not in constraint and "href" not in constraint:
                continue

            statement_element = "gco:CharacterString"
            constraint_value = ""
            if "statement" in constraint:
                constraint_value = constraint["statement"]
            if "href" in constraint:
                statement_element = "gmx:Anchor"
                if "statement" not in constraint:
                    constraint_value = constraint["href"]

            other_constraint_elements = record.xpath(
                f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                f"gmd:MD_LegalConstraints/gmd:otherConstraints/{statement_element}/text() = '{constraint_value}'",
                namespaces=namespaces.nsmap(),
            )
            assert other_constraint_elements is True

            if statement_element == "gmx:Anchor":
                other_constraint_anchor_elements = record.xpath(
                    f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                    f"gmd:MD_LegalConstraints/gmd:otherConstraints/{statement_element}[@xlink:href] = '{constraint_value}'",
                    namespaces=namespaces.nsmap(),
                )
                assert other_constraint_anchor_elements is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_identification_spatial_representation_type(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "identification" not in config or "spatial_representation_type" not in config["identification"]:
        pytest.skip("record does not contain a identification spatial representation type")

    spatial_representation_type_elements = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/"
        f"gmd:MD_SpatialRepresentationTypeCode[@codeList = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/"
        f"ISO_19139_Schemas/resources/codelist/gmxCodelists.xml#MD_SpatialRepresentationTypeCode' and @codeListValue = "
        f"'{config['identification']['spatial_representation_type']}']/text()  = "
        f"'{config['identification']['spatial_representation_type']}'",
        namespaces=namespaces.nsmap(),
    )
    assert spatial_representation_type_elements is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_identification_spatial_resolution(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "identification" not in config or "spatial_resolution" not in config["identification"]:
        pytest.skip("record does not contain a resource spatial resolution")

    if config["identification"]["spatial_resolution"] is not None:
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
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_identification_language(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "identification" not in config or "language" not in config["identification"]:
        pytest.skip("record does not contain a identification language")

    language_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language/gmd:LanguageCode"
        f"[@codeList = 'http://www.loc.gov/standards/iso639-2/php/code_list.php' and @codeListValue = "
        f"'{config['identification']['language']}']/text() = '{config['identification']['language']}'",
        namespaces=namespaces.nsmap(),
    )
    assert language_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_identification_topics(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

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
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_identification_geographic_bounding_box_extent(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if (
        "identification" not in config
        or "extent" not in config["identification"]
        or "geographic" not in config["identification"]["extent"]
        or "bounding_box" not in config["identification"]["extent"]["geographic"]
    ):
        pytest.skip("record does not contain a geographic bounding box extent")

    west_bounding_box_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal/text() = "
        f"'{config['identification']['extent']['geographic']['bounding_box']['west_longitude']}'",
        namespaces=namespaces.nsmap(),
    )
    assert west_bounding_box_value is True

    east_bounding_box_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal/text() = "
        f"'{config['identification']['extent']['geographic']['bounding_box']['east_longitude']}'",
        namespaces=namespaces.nsmap(),
    )
    assert east_bounding_box_value is True

    south_bounding_box_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal/text() = "
        f"'{config['identification']['extent']['geographic']['bounding_box']['south_latitude']}'",
        namespaces=namespaces.nsmap(),
    )
    assert south_bounding_box_value is True

    north_bounding_box_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal/text() = "
        f"'{config['identification']['extent']['geographic']['bounding_box']['north_latitude']}'",
        namespaces=namespaces.nsmap(),
    )
    assert north_bounding_box_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_identification_temporal_extent(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if (
        "identification" not in config
        or "extent" not in config["identification"]
        or "temporal" not in config["identification"]["extent"]
        or "period" not in config["identification"]["extent"]["temporal"]
    ):
        pytest.skip("record does not contain a temporal period extent")

    temporal_period_start_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod[@gml:id = 'boundingExtent']/"
        f"gml:beginPosition/text() = '{config['identification']['extent']['temporal']['period']['start'].isoformat()}'",
        namespaces=namespaces.nsmap(),
    )
    assert temporal_period_start_value is True

    temporal_period_end_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
        f"gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod[@gml:id = 'boundingExtent']/"
        f"gml:endPosition/text() = '{config['identification']['extent']['temporal']['period']['end'].isoformat()}'",
        namespaces=namespaces.nsmap(),
    )
    assert temporal_period_end_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_identification_vertical_extent(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

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
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_identification_supplemental_info(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "identification" not in config or "supplemental_information" not in config["identification"]:
        pytest.skip("record does not contain supplemental information")

    supplemental_info_value = record.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation/"
        f"gco:CharacterString/text() = '{config['identification']['supplemental_information']}'",
        namespaces=namespaces.nsmap(),
    )
    assert supplemental_info_value is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_distribution_formats(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "identification" not in config or "formats" not in config["identification"]:
        pytest.skip("record does not contain any distribution formats")

    for _format in config["identification"]["formats"]:
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
                f"gmd:version/gco:CharacterString/text()",
                namespaces=namespaces.nsmap(),
            )
            assert len(version_values) == 1
            assert version_values[0] == _format["version"]
        if "version" not in _format.keys():
            version_values = record.xpath(
                f"/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/"
                f"gmd:version[@gco:nilReason = 'missing']",
                namespaces=namespaces.nsmap(),
            )
            assert len(version_values) == 1


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_distribution_distributors(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "identification" not in config or "contacts" not in config["identification"]:
        pytest.skip("record does not contain any identification points of contact")

    for poc in _resolve_points_of_contact_xpaths(
        point_of_contact_type="distributors", config=config["identification"]["contacts"]
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
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_distribution_transfer_options(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "identification" not in config or "transfer_options" not in config["identification"]:
        pytest.skip("record does not contain any transfer options")

    for option in config["identification"]["transfer_options"]:
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
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_data_quality_scope(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

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
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_data_quality_lineage(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "identification" not in config or "lineage" not in config["identification"]:
        pytest.skip("record does not contain a lineage")

    lineage_values = record.xpath(
        f"/gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement/"
        f"gco:CharacterString/text() = '{config['identification']['lineage']}'",
        namespaces=namespaces.nsmap(),
    )
    assert lineage_values is True


@pytest.mark.usefixtures("get_record_response")
@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_metadata_maintenance(get_record_response, config_name):
    record = get_record_response(standard=standard, config=config_name)
    config = configs_safe_v2[config_name]

    if "metadata" not in config or "maintenance" not in config["metadata"]:
        pytest.skip("record does not contain metadata maintenance")

    metadata_maintenance_elements = record.xpath(
        "/gmd:MD_Metadata/gmd:metadataMaintenance/gmd:MD_MaintenanceInformation", namespaces=namespaces.nsmap()
    )
    assert len(metadata_maintenance_elements) == 1
    maintenance(element=metadata_maintenance_elements[0], config=config["metadata"]["maintenance"])


def test_edge_case_contact_without_email_address():
    config = deepcopy(configs_safe_v2["minimal_v2"])
    config["metadata"]["contacts"][0]["address"] = {}
    config["metadata"]["contacts"][0]["address"][
        "delivery_point"
    ] = "British Antarctic Survey, High Cross, Madingley Road"
    configuration = MetadataRecordConfigV2(**config)
    record = MetadataRecord(configuration)
    document = fromstring(record.generate_xml_document())
    contact_email_value = document.xpath(
        "/gmd:MD_Metadata/gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/"
        "gmd:CI_Address/gmd:electronicMailAddress/@gco:nilReason = 'unknown'",
        namespaces=namespaces.nsmap(),
    )
    assert contact_email_value is True


def test_edge_case_citation_with_multiple_roles():
    config = deepcopy(configs_safe_v2["minimal_v2"])
    config["reference_system_info"] = {
        "code": {"value": "urn:ogc:def:crs:EPSG::4326"},
        "authority": {"contact": {"individual": {"name": "foo"}, "role": ["publisher", "author"]}},
    }
    configuration = MetadataRecordConfigV2(**config)
    record = MetadataRecord(configuration)
    with pytest.raises(ValueError) as e:
        record.generate_xml_document()

    assert str(e.value) == "Contacts can only have a single role. Citations can only have a single contact."


def test_edge_case_identifier_without_href():
    config = deepcopy(configs_safe_v2["minimal_v2"])
    config["identification"]["identifiers"] = [
        {"identifier": "NE/E007895/1", "title": "award"},
    ]
    configuration = MetadataRecordConfigV2(**config)
    record = MetadataRecord(configuration)
    document = fromstring(record.generate_xml_document())
    identifier_value = document.xpath(
        f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/"
        f"gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text() = "
        f"'{config['identification']['identifiers'][0]['identifier']}'",
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


def test_edge_case_mocked_doi_lookup():
    with patch(
        "bas_metadata_library.standards.iso_19115_common.data_identification_elements.requests.get",
        side_effect=mock_response,
    ):
        config = deepcopy(configs_unsafe_v2["minimal-required-doi-citation_v2"])
        configuration = MetadataRecordConfigV2(**config)
        record = MetadataRecord(configuration)
        document = fromstring(record.generate_xml_document())
        assert document is not None


def test_edge_case_distribution_format_with_version():
    config = deepcopy(configs_safe_v2["minimal_v2"])
    config["identification"]["formats"] = [{"format": "test", "version": "test"}]
    configuration = MetadataRecordConfigV2(**config)
    record = MetadataRecord(configuration)
    document = fromstring(record.generate_xml_document())

    format_version = document.xpath(
        f"/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/"
        f"gmd:version/gco:CharacterString/text() = 'test'",
        namespaces=namespaces.nsmap(),
    )
    assert format_version is True


@pytest.mark.parametrize("config_name", list(configs_safe_v1.keys()))
def test_parse_existing_record_v1(config_name):
    with open(f"tests/resources/records/iso-19115-1/{config_name}-record.xml") as record_file:
        record_data = record_file.read()

    record = MetadataRecord(record=record_data)
    configuration = MetadataRecordConfigV1()
    configuration.convert_from_v2_configuration(record.make_config())
    config = configuration.config
    assert config == configs_safe_v1[config_name]


@pytest.mark.parametrize("config_name", list(configs_safe_v2.keys()))
def test_parse_existing_record_v2(config_name):
    with open(f"tests/resources/records/iso-19115-1/{config_name}-record.xml") as record_file:
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
