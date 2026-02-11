import json
from copy import deepcopy
from datetime import date as _date
from datetime import datetime as _datetime

from lxml.etree import Element

from bas_metadata_library.standards.iso_19115_0 import Namespaces
from bas_metadata_library.standards.iso_19115_common.utils import encode_date_string

namespaces = Namespaces()


def assert_responsible_party(element: Element, config: dict):
    if "role" in config:
        roles_element = element.xpath(
            f"./gmd:role/gmd:CI_RoleCode[@codeList = 'https://standards.iso.org/iso/19115/resources/Codelists/cat/"
            f"codelists.xml#CI_RoleCode'][@codeListValue = '{config['role'][0]}']/text() = '{config['role'][0]}'",
            namespaces=namespaces.nsmap(),
        )
        assert roles_element is True

    if "individual" in config:
        individual_elements = element.xpath(
            "./gmd:individualName/gmx:Anchor | ./gmd:individualName/gco:CharacterString",
            namespaces=namespaces.nsmap(),
        )
        assert len(individual_elements) == 1

        if "name" in config["individual"]:
            individual_values = individual_elements[0].xpath("text()", namespaces=namespaces.nsmap())
            assert len(individual_values) == 1
            assert individual_values[0] == config["individual"]["name"]

        if "href" in config["individual"]:
            individual_hrefs = individual_elements[0].xpath("@xlink:href", namespaces=namespaces.nsmap())
            assert len(individual_hrefs) == 1
            assert individual_hrefs[0] == config["individual"]["href"]

        if "title" in config["individual"]:
            individual_titles = individual_elements[0].xpath("@xlink:title", namespaces=namespaces.nsmap())
            assert len(individual_titles) == 1
            assert individual_titles[0] == config["individual"]["title"]

    if "organisation" in config:
        organisation_elements = element.xpath(
            "./gmd:organisationName/gmx:Anchor | ./gmd:organisationName/gco:CharacterString",
            namespaces=namespaces.nsmap(),
        )
        assert len(organisation_elements) == 1

        if "name" in config["organisation"]:
            organisation_values = organisation_elements[0].xpath("text()", namespaces=namespaces.nsmap())
            assert len(organisation_values) == 1
            assert organisation_values[0] == config["organisation"]["name"]

        if "href" in config["organisation"]:
            organisation_hrefs = organisation_elements[0].xpath("@xlink:href", namespaces=namespaces.nsmap())
            assert len(organisation_hrefs) == 1
            assert organisation_hrefs[0] == config["organisation"]["href"]

        if "title" in config["organisation"]:
            organisation_titles = organisation_elements[0].xpath("@xlink:title", namespaces=namespaces.nsmap())
            assert len(organisation_titles) == 1
            assert organisation_titles[0] == config["organisation"]["title"]

    if "position" in config:
        position_value = element.xpath(
            f"./gmd:positionName/gco:CharacterString/text() = " f"'{config['position']}'",
            namespaces=namespaces.nsmap(),
        )
        assert position_value is True

    if "phone" in config:
        phone_value = element.xpath(
            f"./gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString/text() = "
            f"'{config['phone']}'",
            namespaces=namespaces.nsmap(),
        )
        assert phone_value is True

    if "address" in config:
        if "delivery_point" in config["address"]:
            delivery_point_values = element.xpath(
                f"./gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString/"
                f"text() = '{config['address']['delivery_point']}'",
                namespaces=namespaces.nsmap(),
            )
            assert delivery_point_values is True

        if "city" in config["address"]:
            city_values = element.xpath(
                f"./gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString/text() = "
                f"'{config['address']['city']}'",
                namespaces=namespaces.nsmap(),
            )
            assert city_values is True

        if "administrative_area" in config["address"]:
            administrative_area_values = element.xpath(
                f"./gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:administrativeArea/"
                f"gco:CharacterString/text() = '{config['address']['administrative_area']}'",
                namespaces=namespaces.nsmap(),
            )
            assert administrative_area_values is True

        if "postal_code" in config["address"]:
            postal_code_values = element.xpath(
                f"./gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString/"
                f"text() = '{config['address']['postal_code']}'",
                namespaces=namespaces.nsmap(),
            )
            assert postal_code_values is True

        if "country" in config["address"]:
            country_values = element.xpath(
                f"./gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString/text() "
                f"= '{config['address']['country']}'",
                namespaces=namespaces.nsmap(),
            )
            assert country_values is True

    if "email" in config:
        email_value = element.xpath(
            f"./gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/"
            f"gco:CharacterString/text() = '{config['email']}'",
            namespaces=namespaces.nsmap(),
        )
        assert email_value is True

    if "online_resource" in config:
        online_resource_values = element.xpath(
            "./gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource",
            namespaces=namespaces.nsmap(),
        )
        assert len(online_resource_values) == 1
        assert_online_resource(element=online_resource_values[0], config=config["online_resource"])


def assert_online_resource(element: Element, config: dict):
    if "href" in config:
        url_values = element.xpath(
            f"./gmd:linkage/gmd:URL/text() = '{config['href']}'",
            namespaces=namespaces.nsmap(),
        )
        assert url_values is True

    if "title" in config:
        title_values = element.xpath(
            f"./gmd:name/gco:CharacterString/text() = '{config['title']}'",
            namespaces=namespaces.nsmap(),
        )
        assert title_values is True

    if "description" in config:
        description_values = element.xpath(
            f"./gmd:description/gco:CharacterString/text() = '{config['description']}'",
            namespaces=namespaces.nsmap(),
        )
        assert description_values is True

    if "protocol" in config:
        protocol_values = element.xpath(
            f"./gmd:protocol/gco:CharacterString/text() = '{config['protocol']}'",
            namespaces=namespaces.nsmap(),
        )
        assert protocol_values is True

    if "function" in config:
        function_elements = element.xpath(
            f"./gmd:function/gmd:CI_OnLineFunctionCode[@codeList = 'http://standards.iso.org/ittf/"
            f"PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/gmxCodelists.xml#CI_OnLineFunctionCode']"
            f"[@codeListValue = '{config['function']}']/text() = '{config['function']}'",
            namespaces=namespaces.nsmap(),
        )
        assert function_elements is True


def assert_maintenance(element: Element, config: dict):
    if "maintenance_frequency" in config:
        maintenance_frequency_element = element.xpath(
            f"./gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode[@codeList = "
            f"'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/"
            f"gmxCodelists.xml#MD_MaintenanceFrequencyCode'][@codeListValue = '{config['maintenance_frequency']}']/"
            f"text() = '{config['maintenance_frequency']}'",
            namespaces=namespaces.nsmap(),
        )
        assert maintenance_frequency_element is True

    if "progress" in config:
        maintenance_progress_element = element.xpath(
            f"./gmd:maintenanceNote/gmd:MD_ProgressCode[@codeList = 'http://standards.iso.org/ittf/"
            f"PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/gmxCodelists.xml#MD_ProgressCode']"
            f"[@codeListValue = '{config['progress']}']/text() = '{config['progress']}'",
            namespaces=namespaces.nsmap(),
        )
        assert maintenance_progress_element is True


def assert_legal_constraint(element: Element, config: dict, constraints_container: str):
    constraint_element = "gmd:accessConstraints"
    if config["type"] == "usage":
        constraint_element = "gmd:useConstraints"

    restriction_code_elements = element.xpath(
        f"./{constraints_container}/gmd:MD_LegalConstraints/{constraint_element}/gmd:MD_RestrictionCode[@codeList = "
        f"'https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_RestrictionCode' "
        f"and @codeListValue = '{config['restriction_code']}']/text() = '{config['restriction_code']}'",
        namespaces=namespaces.nsmap(),
    )
    assert restriction_code_elements is True

    if "statement" not in config and "href" not in config and "permissions" not in config:
        return

    if "statement" in config and "href" not in config and "permissions" not in config:
        other_constraint_statement = element.xpath(
            f"./{constraints_container}/gmd:MD_LegalConstraints/gmd:otherConstraints/gco:CharacterString/text() = '{config['statement']}'",
            namespaces=namespaces.nsmap(),
        )
        assert other_constraint_statement is True

    if "statement" in config and "href" in config and "permissions" not in config:
        other_constraint_statement = element.xpath(
            f"./{constraints_container}/gmd:MD_LegalConstraints/gmd:otherConstraints/gmx:Anchor/text() = '{config['statement']}'",
            namespaces=namespaces.nsmap(),
        )
        assert other_constraint_statement is True

        other_constraint_href = element.xpath(
            f"./{constraints_container}/gmd:MD_LegalConstraints/gmd:otherConstraints/gmx:Anchor/@xlink:href = '{config['href']}'",
            namespaces=namespaces.nsmap(),
        )
        assert other_constraint_href is True

    if "statement" not in config and "href" in config and "permissions" not in config:
        other_constraint_href = element.xpath(
            f"./{constraints_container}/gmd:MD_LegalConstraints/gmd:otherConstraints/gmx:Anchor/@xlink:href = '{config['href']}'",
            namespaces=namespaces.nsmap(),
        )
        assert other_constraint_href is True

    if "statement" not in config and "href" not in config and "permissions" in config:
        legal_constraint_id_elements = element.xpath(
            f"./{constraints_container}/gmd:MD_LegalConstraints[contains(@id,'permissions')]",
            namespaces=namespaces.nsmap(),
        )
        assert len(legal_constraint_id_elements) >= 1

        _statement = config["permissions"]
        if not isinstance(_statement, str):
            _statement = json.dumps(_statement)

        other_constraint_statement = element.xpath(
            f"./{constraints_container}/gmd:MD_LegalConstraints/gmd:otherConstraints/gco:CharacterString/text() = '{_statement}'",
            namespaces=namespaces.nsmap(),
        )
        assert other_constraint_statement is True


def assert_date(element: Element, config: dict):
    if "date" in config:
        if type(config["date"]) is _date:
            date_values = element.xpath("./gmd:date/gco:Date/text()", namespaces=namespaces.nsmap())
            # Hack for year only dates
            if len(date_values[0]) == 4:
                date_values[0] = f"{date_values[0]}-01-01"
            assert len(date_values) == 1
            assert _date.fromisoformat(date_values[0]) == config["date"]
        elif type(config["date"]) is _datetime:
            date_values = element.xpath("./gmd:date/gco:DateTime/text()", namespaces=namespaces.nsmap())
            assert len(date_values) == 1
            assert _datetime.fromisoformat(date_values[0]) == config["date"]

    if "date_type" in config:
        date_type_elements = element.xpath(
            f"./gmd:dateType/gmd:CI_DateTypeCode[@codeList = 'https://standards.iso.org/iso/19115/resources/Codelists/"
            f"cat/codelists.xml#CI_DateTypeCode'][@codeListValue = '{config['date_type']}']/text() = "
            f"'{config['date_type']}'",
            namespaces=namespaces.nsmap(),
        )
        assert date_type_elements is True


def assert_identifier(element: Element, config: dict, identifier_container: str = "gmd:identifier"):
    identifier_elements = element.xpath(
        f"./{identifier_container}/gmd:RS_Identifier/gmd:code/gmx:Anchor[text()='{config['identifier']}'] | "
        f"./{identifier_container}/gmd:RS_Identifier/gmd:code/gco:CharacterString[text()='{config['identifier']}']",
        namespaces=namespaces.nsmap(),
    )
    assert len(identifier_elements) == 1

    if "href" in config:
        identifier_href = identifier_elements[0].xpath(
            f"@xlink:href = '{config['href']}'", namespaces=namespaces.nsmap()
        )
        assert identifier_href is True

    if "namespace" in config:
        identifier_namespace_elements = element.xpath(
            f"./{identifier_container}/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString[text()='{config['namespace']}']",
            namespaces=namespaces.nsmap(),
        )
        assert len(identifier_namespace_elements) == 1


def assert_citation(element: Element, config: dict):
    if "title" in config and "value" in config["title"]:
        title_elements = element.xpath(
            f"./gmd:title/gco:CharacterString/text() | ./gmd:title/gmx:Anchor/text()", namespaces=namespaces.nsmap()
        )
        assert len(title_elements) == 1
        assert title_elements[0] == config["title"]["value"]

    if "title" in config and "href" in config["title"]:
        title_href = element.xpath(
            f"./gmd:title/gmx:Anchor/@xlink:href = '{config['title']['href']}'", namespaces=namespaces.nsmap()
        )
        assert title_href is True

    if "dates" in config:
        date_elements = element.xpath("./gmd:date/gmd:CI_Date", namespaces=namespaces.nsmap())
        assert len(date_elements) == len(config["dates"])
        for date_type, date_config in config["dates"].items():
            _date_config = deepcopy(date_config)
            _date_config["date_type"] = date_type
            date_elements = element.xpath(
                f"./gmd:date/gmd:CI_Date[gmd:dateType"
                f"[gmd:CI_DateTypeCode[@codeListValue='{_date_config['date_type']}']]]",
                namespaces=namespaces.nsmap(),
            )
            assert len(date_elements) == 1
            assert_date(element=date_elements[0], config=_date_config)

    if "contact" in config:
        contact_elements = element.xpath(
            "./gmd:citedResponsibleParty/gmd:CI_ResponsibleParty", namespaces=namespaces.nsmap()
        )
        assert len(contact_elements) == 1
        assert_responsible_party(element=contact_elements[0], config=config["contact"])

    if "edition" in config:
        edition_value = element.xpath(
            f"./gmd:edition/gco:CharacterString/text() = '{config['edition']}'", namespaces=namespaces.nsmap()
        )
        assert edition_value is True

    if "identifiers" in config:
        for identifier in config["identifiers"]:
            assert_identifier(element=element, config=identifier)

    if 'series' in config:
        series_elements = element.xpath(f"./gmd:series/gmd:CI_Series", namespaces=namespaces.nsmap())
        assert len(series_elements) == 1

        if "title" in config['series']:
            name_element = series_elements[0].xpath(
                f"./gmd:name/gco:CharacterString/text() = '{config['series']['title']['value']}'",
                namespaces=namespaces.nsmap(),
            )
            assert name_element is True

        if "edition" in config['series']:
            identification_element = series_elements[0].xpath(
                f"./gmd:issueIdentification/gco:CharacterString/text() = '{config['series']['edition']}'",
                namespaces=namespaces.nsmap(),
            )
            assert identification_element is True

        if "page" in config['series']:
            page_element = series_elements[0].xpath(
                f"./gmd:page/gco:CharacterString/text() = '{config['series']['page']}'",
                namespaces=namespaces.nsmap(),
            )
            assert page_element is True


def assert_source(element: Element, config: dict) -> None:
    """assert gmd:LI_Source."""
    description_element = element.xpath(
        f"./gmd:description/gco:CharacterString/text() = '{config['description']}'",
        namespaces=namespaces.nsmap(),
    )
    assert description_element is True

    if any(key in ["title", "dates", "edition", "identifiers", "contact"] for key in config):
        source_citation_elements = element.xpath(
            "./gmd:sourceCitation/gmd:CI_Citation", namespaces=namespaces.nsmap()
        )
        assert len(source_citation_elements) == 1
        assert_citation(element=source_citation_elements[0], config=config)

    if 'source_steps' in config:
        for source_step_config in config['source_steps']:
            source_step_elements = element.xpath(
                f"./gmd:sourceStep/gmd:LI_ProcessStep[gmd:description/gco:CharacterString[text() = '{source_step_config['description']}']]",
                namespaces=namespaces.nsmap(),
            )
            assert len(source_step_elements) == 1
            assert_process_step(source_step_elements[0], source_step_config)


def assert_process_step(element: Element, config: dict) -> None:
    """assert gmd:LI_ProcessStep."""
    description_element = element.xpath(
        f"./gmd:description/gco:CharacterString/text() = '{config['description']}'",
        namespaces=namespaces.nsmap(),
    )
    assert description_element is True

    if "rationale" in config:
        rationale_element = element.xpath(
            f"./gmd:rationale/gco:CharacterString/text() = '{config['rationale']}'",
            namespaces=namespaces.nsmap(),
        )
        assert rationale_element is True

    if "date" in config:
        date_element = element.xpath(
            f"./gmd:dateTime/gco:DateTime/text() = '{encode_date_string(config['date'])}'",
            namespaces=namespaces.nsmap(),
        )
        assert date_element is True

    if 'processors' in config:
        for processor_config in config['processors']:
            _property = 'individual' if 'individual' in processor_config else "organisation"
            _element = f"gmd:{_property}Name"
            processor_elements = element.xpath(
                f"./gmd:processor/gmd:CI_ResponsibleParty[{_element}/gco:CharacterString/text() = '{processor_config[_property]['name']}'] | "
                f"./gmd:processor/gmd:CI_ResponsibleParty[{_element}/gmx:Anchor/text() = '{processor_config[_property]['name']}']",
                namespaces=namespaces.nsmap(),
            )
            assert len(processor_elements) == 1
            assert_responsible_party(element=processor_elements[0], config=processor_config)

    if 'sources' in config:
        for source_config in config['sources']:
            sources_elements = element.xpath(
                f"./gmd:source/gmd:LI_Source[gmd:description[gco:CharacterString[text() = '{source_config['description']}']]]",
                namespaces=namespaces.nsmap(),
            )
            assert len(sources_elements) == 1
            assert_source(sources_elements[0], source_config)
