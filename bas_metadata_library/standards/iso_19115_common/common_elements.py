from copy import deepcopy
from datetime import datetime

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# We don't currently allow untrusted/user-provided XML so this is not a risk
from lxml.etree import SubElement, Element  # nosec

from bas_metadata_library import MetadataRecord as _MetadataRecord, MetadataRecord
from bas_metadata_library.standards.iso_19115_common import MetadataRecordElement, CodeListElement
from bas_metadata_library.standards.iso_19115_common.utils import encode_date_string, decode_date_string


class Language(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        xpath: str = None,
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath=f"{xpath}/gmd:LanguageCode",
        )
        self.code_list_values = ["eng"]
        self.code_list = "http://www.loc.gov/standards/iso639-2/php/code_list.php"
        self.element = f"{{{self.ns.gmd}}}language"
        self.element_code = f"{{{self.ns.gmd}}}LanguageCode"
        self.attribute = "language"


class CharacterSet(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        xpath: str = None,
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath=f"{xpath}/gmd:MD_CharacterSetCode",
        )
        self.code_list_values = ["utf-8"]
        self.code_list = (
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/"
            "codelist/gmxCodelists.xml#MD_CharacterSetCode"
        )
        self.element = f"{{{self.ns.gmd}}}characterSet"
        self.element_code = f"{{{self.ns.gmd}}}MD_CharacterSetCode"
        self.attribute = "character_set"


class ResponsibleParty(MetadataRecordElement):
    def __init__(
        self,
        record: _MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        xpath: str = None,
    ):
        super().__init__(record, attributes, parent_element, element_attributes, xpath)

    def make_config(self) -> dict:
        _ = {}

        individual_name = self.record.xpath(
            f"{ self.xpath }/gmd:CI_ResponsibleParty/gmd:individualName/gmx:Anchor/text() | "
            f"{ self.xpath }/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(individual_name) > 0:
            if "individual" not in _.keys():
                _["individual"] = {}
            _["individual"]["name"] = individual_name[0]

        individual_href = self.record.xpath(
            f"{ self.xpath }/gmd:CI_ResponsibleParty/gmd:individualName/gmx:Anchor/@xlink:href",
            namespaces=self.ns.nsmap(),
        )
        if len(individual_href) > 0:
            if "individual" not in _.keys():
                _["individual"] = {}
            _["individual"]["href"] = individual_href[0]

        individual_title = self.record.xpath(
            f"{ self.xpath }/gmd:CI_ResponsibleParty/gmd:individualName/gmx:Anchor/@xlink:title",
            namespaces=self.ns.nsmap(),
        )
        if len(individual_title) > 0:
            _["individual"]["title"] = individual_title[0]

        organisation_name = self.record.xpath(
            f"{ self.xpath }/gmd:CI_ResponsibleParty/gmd:organisationName/gmx:Anchor/text() | "
            f"{ self.xpath }/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(organisation_name) > 0:
            if "organisation" not in _.keys():
                _["organisation"] = {}
            _["organisation"]["name"] = organisation_name[0]

        organisation_href = self.record.xpath(
            f"{ self.xpath }/gmd:CI_ResponsibleParty/gmd:organisationName/gmx:Anchor/@xlink:href",
            namespaces=self.ns.nsmap(),
        )
        if len(organisation_href) > 0:
            if "organisation" not in _.keys():
                _["organisation"] = {}
            _["organisation"]["href"] = organisation_href[0]

        organisation_title = self.record.xpath(
            f"{ self.xpath }/gmd:CI_ResponsibleParty/gmd:organisationName/gmx:Anchor/@xlink:title",
            namespaces=self.ns.nsmap(),
        )
        if len(organisation_title) > 0:
            _["organisation"]["title"] = organisation_title[0]

        position_value = self.record.xpath(
            f"{self.xpath}/gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(position_value) > 0:
            _["position"] = position_value[0]

        phone_value = self.record.xpath(
            f"{self.xpath}/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/"
            f"gmd:CI_Telephone/gmd:voice/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(phone_value) > 0:
            _["phone"] = phone_value[0]

        delivery_point_value = self.record.xpath(
            f"{self.xpath}/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/"
            f"gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(delivery_point_value) > 0:
            if "address" not in _.keys():
                _["address"] = {}
            _["address"]["delivery_point"] = delivery_point_value[0]

        city_value = self.record.xpath(
            f"{self.xpath}/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/"
            f"gmd:CI_Address/gmd:city/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(city_value) > 0:
            if "address" not in _.keys():
                _["address"] = {}
            _["address"]["city"] = city_value[0]

        administrative_area_value = self.record.xpath(
            f"{self.xpath}/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/"
            f"gmd:CI_Address/gmd:administrativeArea/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(administrative_area_value) > 0:
            if "address" not in _.keys():
                _["address"] = {}
            _["address"]["administrative_area"] = administrative_area_value[0]

        postal_code_value = self.record.xpath(
            f"{self.xpath}/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/"
            f"gmd:CI_Address/gmd:postalCode/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(postal_code_value) > 0:
            if "address" not in _.keys():
                _["address"] = {}
            _["address"]["postal_code"] = postal_code_value[0]

        country_value = self.record.xpath(
            f"{self.xpath}/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/"
            f"gmd:CI_Address/gmd:country/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(country_value) > 0:
            if "address" not in _.keys():
                _["address"] = {}
            _["address"]["country"] = country_value[0]

        email_value = self.record.xpath(
            f"{self.xpath}/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/"
            f"gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(email_value) > 0:
            _["email"] = email_value[0]

        online_resource = OnlineResource(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource",
        )
        _online_resource = online_resource.make_config()
        if bool(_online_resource):
            _["online_resource"] = _online_resource

        role = Role(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:CI_ResponsibleParty/gmd:role"
        )
        _role = role.make_config()
        if _role != "":
            _["role"] = [_role]

        return _

    def make_element(self):
        responsible_party_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}CI_ResponsibleParty")

        if "individual" in self.element_attributes and "name" in self.element_attributes["individual"]:
            individual_element = SubElement(responsible_party_element, f"{{{self.ns.gmd}}}individualName")
            if "href" in self.element_attributes["individual"]:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=individual_element,
                    element_attributes=self.element_attributes["individual"],
                    element_value=self.element_attributes["individual"]["name"],
                )
                anchor.make_element()
            else:
                individual_value = SubElement(individual_element, f"{{{self.ns.gco}}}CharacterString")
                individual_value.text = self.element_attributes["individual"]["name"]

        if "organisation" in self.element_attributes and "name" in self.element_attributes["organisation"]:
            organisation_element = SubElement(responsible_party_element, f"{{{self.ns.gmd}}}organisationName")
            if "href" in self.element_attributes["organisation"]:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=organisation_element,
                    element_attributes=self.element_attributes["organisation"],
                    element_value=self.element_attributes["organisation"]["name"],
                )
                anchor.make_element()
            else:
                organisation_name_value = SubElement(organisation_element, f"{{{self.ns.gco}}}CharacterString")
                organisation_name_value.text = self.element_attributes["organisation"]["name"]

        if "position" in self.element_attributes:
            position_name_element = SubElement(responsible_party_element, f"{{{self.ns.gmd}}}positionName")
            position_name_value = SubElement(position_name_element, f"{{{self.ns.gco}}}CharacterString")
            position_name_value.text = self.element_attributes["position"]

        if (
            "phone" in self.element_attributes
            or "address" in self.element_attributes
            or "email" in self.element_attributes
            or "online_resource" in self.element_attributes
        ):
            contact_wrapper = SubElement(responsible_party_element, f"{{{self.ns.gmd}}}contactInfo")
            contact_element = SubElement(contact_wrapper, f"{{{self.ns.gmd}}}CI_Contact")

            if "phone" in self.element_attributes:
                phone_wrapper = SubElement(contact_element, f"{{{self.ns.gmd}}}phone")
                phone_element = SubElement(phone_wrapper, f"{{{self.ns.gmd}}}CI_Telephone")
                phone_voice = SubElement(phone_element, f"{{{self.ns.gmd}}}voice")
                phone_voice_value = SubElement(phone_voice, f"{{{self.ns.gco}}}CharacterString")
                phone_voice_value.text = self.element_attributes["phone"]

            if "address" in self.element_attributes or "email" in self.element_attributes:
                address_wrapper = SubElement(contact_element, f"{{{self.ns.gmd}}}address")
                address_element = SubElement(address_wrapper, f"{{{self.ns.gmd}}}CI_Address")

                if "address" in self.element_attributes:
                    if "delivery_point" in self.element_attributes["address"]:
                        delivery_point_element = SubElement(address_element, f"{{{self.ns.gmd}}}deliveryPoint")
                        delivery_point_value = SubElement(delivery_point_element, f"{{{self.ns.gco}}}CharacterString")
                        delivery_point_value.text = self.element_attributes["address"]["delivery_point"]
                    if "city" in self.element_attributes["address"]:
                        city_element = SubElement(address_element, f"{{{self.ns.gmd}}}city")
                        city_value = SubElement(city_element, f"{{{self.ns.gco}}}CharacterString")
                        city_value.text = self.element_attributes["address"]["city"]
                    if "administrative_area" in self.element_attributes["address"]:
                        administrative_area_element = SubElement(
                            address_element, f"{{{self.ns.gmd}}}administrativeArea"
                        )
                        administrative_area_value = SubElement(
                            administrative_area_element, f"{{{self.ns.gco}}}CharacterString"
                        )
                        administrative_area_value.text = self.element_attributes["address"]["administrative_area"]
                    if "postal_code" in self.element_attributes["address"]:
                        postal_code_element = SubElement(address_element, f"{{{self.ns.gmd}}}postalCode")
                        postal_code_value = SubElement(postal_code_element, f"{{{self.ns.gco}}}CharacterString")
                        postal_code_value.text = self.element_attributes["address"]["postal_code"]
                    if "country" in self.element_attributes["address"]:
                        country_element = SubElement(address_element, f"{{{self.ns.gmd}}}country")
                        country_value = SubElement(country_element, f"{{{self.ns.gco}}}CharacterString")
                        country_value.text = self.element_attributes["address"]["country"]

                if "email" in self.element_attributes:
                    email_element = SubElement(address_element, f"{{{self.ns.gmd}}}electronicMailAddress")
                    email_value = SubElement(email_element, f"{{{self.ns.gco}}}CharacterString")
                    email_value.text = self.element_attributes["email"]
                else:
                    SubElement(
                        address_element,
                        f"{{{self.ns.gmd}}}electronicMailAddress",
                        attrib={f"{{{self.ns.gco}}}nilReason": "unknown"},
                    )

            if "online_resource" in self.element_attributes:
                online_resource_wrapper = SubElement(contact_element, f"{{{self.ns.gmd}}}onlineResource")
                online_resource = OnlineResource(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=online_resource_wrapper,
                    element_attributes=self.element_attributes["online_resource"],
                )
                online_resource.make_element()

        if "role" in self.element_attributes:
            role = Role(
                record=self.record,
                attributes=self.attributes,
                parent_element=responsible_party_element,
                element_attributes=self.element_attributes,
            )
            role.make_element()


class OnlineResource(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        linkage = Linkage(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{ self.xpath }/gmd:CI_OnlineResource/gmd:linkage",
        )
        _linkage = linkage.make_config()
        if "href" in _linkage.keys():
            _["href"] = _linkage["href"]

        name_value = self.record.xpath(
            f"{self.xpath}/gmd:CI_OnlineResource/gmd:name/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(name_value) > 0:
            _["title"] = name_value[0]

        description_value = self.record.xpath(
            f"{self.xpath}/gmd:CI_OnlineResource/gmd:description/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(description_value) > 0:
            _["description"] = description_value[0]

        function = OnlineRole(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:CI_OnlineResource/gmd:function",
        )
        _function = function.make_config()
        if _function != "":
            _["function"] = _function

        return _

    def make_element(self):
        online_resource_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}CI_OnlineResource")

        if "href" in self.element_attributes:
            linkage = Linkage(
                record=self.record,
                attributes=self.attributes,
                parent_element=online_resource_element,
                element_attributes=self.element_attributes,
            )
            linkage.make_element()

        if "title" in self.element_attributes:
            title_wrapper = SubElement(online_resource_element, f"{{{self.ns.gmd}}}name")
            title_element = SubElement(title_wrapper, f"{{{self.ns.gco}}}CharacterString")
            title_element.text = self.element_attributes["title"]

        if "description" in self.element_attributes:
            title_wrapper = SubElement(online_resource_element, f"{{{self.ns.gmd}}}description")
            title_element = SubElement(title_wrapper, f"{{{self.ns.gco}}}CharacterString")
            title_element.text = self.element_attributes["description"]

        if "function" in self.element_attributes:
            function = OnlineRole(
                record=self.record,
                attributes=self.attributes,
                parent_element=online_resource_element,
                element_attributes=self.element_attributes,
            )
            function.make_element()


class Linkage(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        url_value = self.record.xpath(
            f"{self.xpath}/gmd:URL/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(url_value) > 0:
            _["href"] = url_value[0]

        return _

    def make_element(self):
        linkage_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}linkage")
        if "href" in self.element_attributes:
            url_value = SubElement(linkage_element, f"{{{self.ns.gmd}}}URL")
            url_value.text = self.element_attributes["href"]


class Role(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        xpath: str = None,
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath=f"{xpath}/gmd:CI_RoleCode",
        )
        self.code_list_values = [
            "author",
            "custodian",
            "distributor",
            "originator",
            "owner",
            "pointOfContact",
            "principalInvestigator",
            "processor",
            "publisher",
            "resourceProvider",
            "sponsor",
            "user",
            "coAuthor",
            "collaborator",
            "contributor",
            "editor",
            "funder",
            "mediator",
            "rightsHolder",
            "stakeholder",
        ]
        self.code_list = "https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_RoleCode"
        self.element = f"{{{self.ns.gmd}}}role"
        self.element_code = f"{{{self.ns.gmd}}}CI_RoleCode"
        self.attribute = "role"


class OnlineRole(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        xpath: str = None,
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath=f"{xpath}/gmd:CI_OnLineFunctionCode",
        )
        self.code_list_values = ["download", "information", "offlineAccess", "order", "search"]
        self.code_list = (
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/"
            "codelist/gmxCodelists.xml#CI_OnLineFunctionCode"
        )
        self.element = f"{{{self.ns.gmd}}}function"
        self.element_code = f"{{{self.ns.gmd}}}CI_OnLineFunctionCode"
        self.attribute = "function"


class MaintenanceInformation(MetadataRecordElement):
    def __init__(
        self,
        record: _MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        xpath: str = None,
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath=f"{xpath}/gmd:MD_MaintenanceInformation",
        )

    def make_config(self) -> dict:
        _ = {}

        maintenance_frequency = MaintenanceAndUpdateFrequency(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:maintenanceAndUpdateFrequency",
        )
        _maintenance_frequency = maintenance_frequency.make_config()
        if _maintenance_frequency != "":
            _["maintenance_frequency"] = _maintenance_frequency

        progress = MaintenanceProgress(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:maintenanceNote",
        )
        _progress = progress.make_config()
        if _progress != "":
            _["progress"] = _progress

        return _

    def make_element(self):
        maintenance_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}MD_MaintenanceInformation")

        if "maintenance_frequency" in self.element_attributes:
            maintenance_and_update_frequency = MaintenanceAndUpdateFrequency(
                record=self.record,
                attributes=self.attributes,
                parent_element=maintenance_element,
                element_attributes=self.element_attributes,
            )
            maintenance_and_update_frequency.make_element()

        if "progress" in self.element_attributes:
            maintenance_process = MaintenanceProgress(
                record=self.record,
                attributes=self.attributes,
                parent_element=maintenance_element,
                element_attributes=self.element_attributes,
            )
            maintenance_process.make_element()


class MaintenanceAndUpdateFrequency(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        xpath: str = None,
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath=f"{xpath}/gmd:MD_MaintenanceFrequencyCode",
        )
        self.code_list_values = [
            "continual",
            "daily",
            "weekly",
            "fortnightly",
            "monthly",
            "quarterly",
            "biannually",
            "annually",
            "asNeeded",
            "irregular",
            "notPlanned",
            "unknown",
        ]
        self.code_list = (
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/"
            "codelist/gmxCodelists.xml#MD_MaintenanceFrequencyCode"
        )
        self.element = f"{{{self.ns.gmd}}}maintenanceAndUpdateFrequency"
        self.element_code = f"{{{self.ns.gmd}}}MD_MaintenanceFrequencyCode"
        self.attribute = "maintenance_frequency"


class MaintenanceProgress(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        xpath: str = None,
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath=f"{xpath}/gmd:MD_ProgressCode",
        )
        self.code_list_values = [
            "completed",
            "historicalArchive",
            "obsolete",
            "onGoing",
            "planned",
            "required",
            "underDevelopment",
        ]
        self.code_list = (
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/"
            "codelist/gmxCodelists.xml#MD_ProgressCode"
        )
        self.element = f"{{{self.ns.gmd}}}maintenanceNote"
        self.element_code = f"{{{self.ns.gmd}}}MD_ProgressCode"
        self.attribute = "progress"


class Citation(MetadataRecordElement):
    def __init__(
        self,
        record: _MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        xpath: str = None,
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath=f"{xpath}/gmd:CI_Citation",
        )

    def make_config(self) -> dict:
        _ = {}

        title_value = self.record.xpath(
            f"{self.xpath}/gmd:title/gco:CharacterString/text() | {self.xpath}/gmd:title/gmx:Anchor/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(title_value) == 1:
            if "title" not in _.keys():
                _["title"] = {}
            _["title"]["value"] = title_value[0]

        title_href = self.record.xpath(f"{self.xpath}/gmd:title/gmx:Anchor/@xlink:href", namespaces=self.ns.nsmap())
        if len(title_href) == 1:
            if "title" not in _.keys():
                _["title"] = {}
            _["title"]["href"] = title_href[0]

        _dates = {}
        dates_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:date)",
                namespaces=self.ns.nsmap(),
            )
        )
        for date_index in range(1, dates_length + 1):
            date_ = Date(record=self.record, attributes=self.attributes, xpath=f"({self.xpath}/gmd:date)[{date_index}]")
            _date = date_.make_config()
            if bool(_date):
                _date_type = _date["date_type"]
                del _date["date_type"]
                _dates[_date_type] = _date
        if bool(_dates):
            _["dates"] = _dates

        edition_value = self.record.xpath(
            f"{self.xpath}/gmd:edition/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(edition_value) == 1:
            _["edition"] = edition_value[0]

        _identifiers = []
        identifiers_length = int(
            self.record.xpath(
                f"count({self.xpath}/gmd:identifier)",
                namespaces=self.ns.nsmap(),
            )
        )
        for identifier_index in range(1, identifiers_length + 1):
            identifier = Identifier(
                record=self.record,
                attributes=self.attributes,
                xpath=f"({self.xpath}/gmd:identifier)[{identifier_index}]",
            )
            _identifier = identifier.make_config()
            if bool(_identifier):
                _identifiers.append(_identifier)
        if len(_identifiers) > 0:
            _["identifiers"] = _identifiers

        cited_responsible_party = ResponsibleParty(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:citedResponsibleParty"
        )
        _cited_responsible_party = cited_responsible_party.make_config()
        if bool(_cited_responsible_party):
            _["contact"] = _cited_responsible_party

        return _

    def make_element(self):
        citation_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}CI_Citation")

        if "title" in self.element_attributes:
            title_element = SubElement(citation_element, f"{{{self.ns.gmd}}}title")
            if "href" in self.element_attributes["title"]:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=title_element,
                    element_attributes=self.element_attributes["title"],
                    element_value=self.element_attributes["title"]["value"],
                )
                anchor.make_element()
            else:
                title_value = SubElement(title_element, f"{{{self.ns.gco}}}CharacterString")
                title_value.text = self.element_attributes["title"]["value"]

        if "dates" in self.element_attributes:
            for date_type, date_attributes in self.element_attributes["dates"].items():
                _date_attributes = deepcopy(date_attributes)
                _date_attributes["date_type"] = date_type
                citation_date = Date(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=citation_element,
                    element_attributes=_date_attributes,
                )
                citation_date.make_element()

        if "edition" in self.element_attributes:
            edition_element = SubElement(citation_element, f"{{{self.ns.gmd}}}edition")
            edition_value = SubElement(edition_element, f"{{{self.ns.gco}}}CharacterString")
            edition_value.text = str(self.element_attributes["edition"])

        if "identifiers" in self.element_attributes:
            for identifier_attributes in self.element_attributes["identifiers"]:
                identifier = Identifier(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=citation_element,
                    element_attributes=identifier_attributes,
                )
                identifier.make_element()

        if "contact" in self.element_attributes:
            citated_responsible_party_element = SubElement(citation_element, f"{{{self.ns.gmd}}}citedResponsibleParty")

            # Citations can only have a single contact so collapse roles array down to a single value
            _contact_element_attributes = self.element_attributes["contact"]
            if type(self.element_attributes["contact"]["role"]) is list:
                if len(self.element_attributes["contact"]["role"]) > 1:
                    raise ValueError("Contacts can only have a single role. Citations can only have a single contact.")
                _contact_element_attributes = deepcopy(self.element_attributes["contact"])
                _contact_element_attributes["role"] = _contact_element_attributes["role"][0]

            responsible_party = ResponsibleParty(
                record=self.record,
                attributes=self.attributes,
                parent_element=citated_responsible_party_element,
                element_attributes=_contact_element_attributes,
            )
            responsible_party.make_element()


class Date(MetadataRecordElement):
    def __init__(
        self,
        record: _MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        xpath: str = None,
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath=f"{xpath}/gmd:CI_Date",
        )

    def make_config(self) -> dict:
        _ = {}

        date_value = self.record.xpath(
            f"{self.xpath}/gmd:date/gco:Date/text() | {self.xpath}/gmd:date/gco:DateTime/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(date_value) == 1:
            try:
                _ = decode_date_string(date_datetime=date_value[0])
            except ValueError:
                raise RuntimeError("Date/datetime could not be parsed as an ISO date value")

        date_type = DateType(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:dateType")
        _date_type = date_type.make_config()
        _["date_type"] = _date_type

        return _

    def make_element(self):
        date_container_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}date")
        date_container_element = SubElement(date_container_wrapper, f"{{{self.ns.gmd}}}CI_Date")

        date_element = SubElement(date_container_element, f"{{{self.ns.gmd}}}date")

        date_value_element = f"{{{self.ns.gco}}}Date"
        if type(self.element_attributes["date"]) is datetime:
            date_value_element = f"{{{self.ns.gco}}}DateTime"

        _date_precision = None
        if "date_precision" in self.element_attributes.keys():
            _date_precision = self.element_attributes["date_precision"]
        date_value = SubElement(date_element, date_value_element)
        date_value.text = encode_date_string(
            date_datetime=self.element_attributes["date"], date_precision=_date_precision
        )

        date_type = DateType(
            record=self.record,
            attributes=self.attributes,
            parent_element=date_container_element,
            element_attributes=self.element_attributes,
        )
        date_type.make_element()


class DateType(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        xpath: str = None,
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath=f"{xpath}/gmd:CI_DateTypeCode",
        )
        self.code_list_values = [
            "creation",
            "publication",
            "revision",
            "expiry",
            "lastUpdate",
            "lastRevision",
            "nextUpdate",
            "unavailable",
            "inForce",
            "adopted",
            "deprecated",
            "superseded",
            "validityBegins",
            "validityExpires",
            "released",
            "distribution",
        ]
        self.code_list = "https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_DateTypeCode"
        self.element = f"{{{self.ns.gmd}}}dateType"
        self.element_code = f"{{{self.ns.gmd}}}CI_DateTypeCode"
        self.attribute = "date_type"


class Identifier(MetadataRecordElement):
    def __init__(
        self,
        record: _MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        xpath: str = None,
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath=f"{xpath}/gmd:RS_Identifier",
        )
        self.identifier_container = f"{{{self.ns.gmd}}}identifier"

    def make_config(self) -> dict:
        _ = {}

        identifier_value = self.record.xpath(
            f"{self.xpath}/gmd:code/gco:CharacterString/text() | {self.xpath}/gmd:code/gmx:Anchor/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(identifier_value) == 1:
            _["identifier"] = identifier_value[0]

        identifier_href = self.record.xpath(f"{self.xpath}/gmd:code/gmx:Anchor/@xlink:href", namespaces=self.ns.nsmap())
        if len(identifier_href) == 1:
            _["href"] = identifier_href[0]

        identifier_namespace = self.record.xpath(
            f"{self.xpath}/gmd:codeSpace/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(identifier_namespace) == 1:
            _["namespace"] = identifier_namespace[0]

        return _

    def make_element(self):
        identifier_container = SubElement(self.parent_element, self.identifier_container)
        identifier_wrapper = SubElement(identifier_container, f"{{{self.ns.gmd}}}RS_Identifier")
        identifier_element = SubElement(identifier_wrapper, f"{{{self.ns.gmd}}}code")

        if "href" in self.element_attributes:
            anchor = AnchorElement(
                record=self.record,
                attributes=self.attributes,
                parent_element=identifier_element,
                element_attributes=self.element_attributes,
                element_value=self.element_attributes["identifier"],
            )
            anchor.make_element()
        else:
            identifier_value = SubElement(identifier_element, f"{{{self.ns.gco}}}CharacterString")
            identifier_value.text = self.element_attributes["identifier"]

        if "namespace" in self.element_attributes:
            identifier_scheme_element = SubElement(identifier_wrapper, f"{{{self.ns.gmd}}}codeSpace")
            identifier_scheme_value = SubElement(identifier_scheme_element, f"{{{self.ns.gco}}}CharacterString")
            identifier_scheme_value.text = self.element_attributes["namespace"]


class AnchorElement(MetadataRecordElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        element_value: str = None,
    ):
        super().__init__(
            record=record, attributes=attributes, parent_element=parent_element, element_attributes=element_attributes
        )
        self.text = element_value

    def make_element(self):
        attributes = {}

        if "href" in self.element_attributes:
            attributes[f"{{{self.ns.xlink}}}href"] = self.element_attributes["href"]
            attributes[f"{{{self.ns.xlink}}}actuate"] = "onRequest"
        if "title" in self.element_attributes:
            attributes[f"{{{self.ns.xlink}}}title"] = self.element_attributes["title"]

        anchor = SubElement(self.parent_element, f"{{{self.ns.gmx}}}Anchor", attrib=attributes)
        if self.text is not None:
            anchor.text = self.text
