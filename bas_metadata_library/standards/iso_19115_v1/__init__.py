import json
from itertools import groupby

import requests

from copy import deepcopy
from datetime import datetime, date
from typing import Union, Optional, List
from importlib.resources import path as resource_path

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# We don't currently allow untrusted/user-provided XML so this is not a risk
from lxml.etree import Element, SubElement, fromstring  # nosec

from bas_metadata_library import (
    Namespaces as _Namespaces,
    MetadataRecordConfig as _MetadataRecordConfig,
    MetadataRecord as _MetadataRecord,
    MetadataRecordElement as _MetadataRecordElement,
)


# Utility classes


class Utils(object):
    """
    Utility methods
    """

    @staticmethod
    def format_date_string(date_datetime: Union[date, datetime]) -> str:
        """
        Formats a python date or datetime as an ISO 8601 date or datetime string representation

        E.g. Return 'date(2012, 4, 18)' as '2012-04-18' or 'datetime(2012, 4, 18, 22, 48, 56)' as '2012-4-18T22:48:56'.

        :type date_datetime: date/datetime
        :param date_datetime: python date/datetime

        :rtype str
        :return: ISO 8601 formatted date/datetime
        """
        return date_datetime.isoformat()

    @staticmethod
    def contacts_have_role(contacts: list, role: str) -> bool:
        """
        Checks if at least one contact has a given role

        E.g. in all the contacts in a resource, do any have the 'distributor' role?

        :type contacts: list
        :param contacts: list of contacts (point of contacts)
        :type role: str
        :param role: role to check for

        :rtype bool
        :return True if at least one contact has the given role, otherwise False
        """
        for contact in contacts:
            if role in contact["role"]:
                return True

        return False

    @staticmethod
    def contacts_condense_roles(contacts: List[dict]):
        """
        Groups separate contacts with multiple roles into a single contact with multiple roles

        I.e. if two contacts are identical but with different, singular, roles, this method will return a single contact
        with multiple roles.

        E.g. a set of contacts: {'name': 'foo', role: ['a']}, {'name': 'foo', role: ['b']}, {'name': 'bar', role: ['a']}
                   with become: {'name': 'foo', role: ['a', 'b']}, {'name': 'bar', role: ['a']}

        :type contacts: list
        :param contacts: list of contacts to be grouped/reduced

        :rtype list
        :return list of contacts with merged roles
        """
        _merged_contacts = []

        _contacts_without_roles = []
        for contact in contacts:
            _contact = deepcopy(contact)
            del _contact["role"]
            _contacts_without_roles.append(
                {"key": json.dumps(_contact), "key_data": _contact, "role_data": contact["role"][0]}
            )

        for key, contact in groupby(_contacts_without_roles, key=lambda x: x["key"]):
            contact = list(contact)
            _merged_contact = contact[0]["key_data"]
            _merged_contact["role"] = []
            for _contact in contact:
                _merged_contact["role"].append(_contact["role_data"])
            _merged_contacts.append(_merged_contact)

        return _merged_contacts


# Base classes


class Namespaces(_Namespaces):
    """
    Overloaded base Namespaces class

    Defines the namespaces for this standard
    """

    gmd = "http://www.isotc211.org/2005/gmd"
    gco = "http://www.isotc211.org/2005/gco"
    gml = "http://www.opengis.net/gml/3.2"
    gmx = "http://www.isotc211.org/2005/gmx"
    srv = "http://www.isotc211.org/2005/srv"
    xlink = "http://www.w3.org/1999/xlink"
    xsi = "http://www.w3.org/2001/XMLSchema-instance"

    _schema_locations = {
        "gmd": "https://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gmd/gmd.xsd",
        "gco": "https://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gco/gco.xsd",
        "gmx": "https://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gmx/gmx.xsd",
        "srv": "https://standards.iso.org/iso/19119/srv/srv.xsd",
    }

    def __init__(self):
        self._namespaces = {
            "gmd": self.gmd,
            "gco": self.gco,
            "gml": self.gml,
            "gmx": self.gmx,
            "srv": self.srv,
            "xlink": self.xlink,
            "xsi": self.xsi,
        }


class MetadataRecordConfig(_MetadataRecordConfig):
    """
    Overloaded base MetadataRecordConfig class

    Defines the JSON Schema used for this metadata standard
    """

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)

        self.config = kwargs

        with resource_path(
            "bas_metadata_library.standards_schemas.iso_19115_v1", "configuration-schema.json"
        ) as configuration_schema_file_path:
            with open(configuration_schema_file_path) as configuration_schema_file:
                configuration_schema_data = json.load(configuration_schema_file)
        self.schema = configuration_schema_data


class MetadataRecord(_MetadataRecord):
    """
    Overloaded base MetadataRecordConfig class

    Defines the root element, and it's sub-elements, for this metadata standard
    """

    def __init__(self, configuration: MetadataRecordConfig = None, record: str = None):
        self.ns = Namespaces()
        self.attributes = {}
        self.record = None

        if configuration is not None:
            configuration.validate()
            self.attributes = configuration.config

        if record is not None:
            self.record = fromstring(record.encode())

    def make_config(self) -> MetadataRecordConfig:
        file_identifier = FileIdentifier(record=self.record, attributes=self.attributes)
        _file_identifier = file_identifier.make_config()
        if _file_identifier != "":
            # noinspection PyTypeChecker
            self.attributes["file_identifier"] = _file_identifier

        language = Language(record=self.record, attributes=self.attributes, xpath="/gmd:MD_Metadata/gmd:language")
        _language = language.make_config()
        if _language != "":
            # noinspection PyTypeChecker
            self.attributes["language"] = _language

        character_set = CharacterSet(
            record=self.record, attributes=self.attributes, xpath="/gmd:MD_Metadata/gmd:characterSet"
        )
        _character_set = character_set.make_config()
        if _character_set != "":
            # noinspection PyTypeChecker
            self.attributes["character_set"] = _character_set

        hierarchy_level = HierarchyLevel(record=self.record, attributes=self.attributes)
        _hierarchy_level = hierarchy_level.make_config()
        if _hierarchy_level != "":
            # noinspection PyTypeChecker
            self.attributes["hierarchy_level"] = _hierarchy_level

        _contacts = []
        contacts_length = int(self.record.xpath(f"count(/gmd:MD_Metadata/gmd:contact)", namespaces=self.ns.nsmap(),))
        for contact_index in range(1, contacts_length + 1):
            contact = Contact(
                record=self.record, attributes=self.attributes, xpath=f"/gmd:MD_Metadata/gmd:contact[{contact_index}]"
            )
            _contact = contact.make_config()
            if bool(_contact):
                _contacts.append(_contact)
        if len(_contacts) > 0:
            # noinspection PyTypeChecker
            self.attributes["contacts"] = _contacts

        date_stamp = DateStamp(record=self.record, attributes=self.attributes)
        _date_stamp = date_stamp.make_config()
        if _date_stamp is not None:
            # noinspection PyTypeChecker
            self.attributes["date_stamp"] = _date_stamp

        metadata_standard = MetadataStandard(record=self.record, attributes=self.attributes)
        _metadata_standard = metadata_standard.make_config()
        if bool(_metadata_standard):
            self.attributes["metadata_standard"] = _metadata_standard

        reference_system_identifier = ReferenceSystemInfo(record=self.record, attributes=self.attributes)
        _reference_system_identifier = reference_system_identifier.make_config()
        if bool(_reference_system_identifier):
            # noinspection PyTypeChecker
            self.attributes["reference_system_info"] = _reference_system_identifier

        _resource = {}

        data_identification = DataIdentification(record=self.record, attributes=self.attributes)
        _data_identification = data_identification.make_config()
        if bool(_data_identification):
            _resource = {**_resource, **_data_identification}

        data_distribution = DataDistribution(record=self.record, attributes=self.attributes)
        _data_distribution = data_distribution.make_config()
        if bool(_data_distribution):
            # detach distributors and merge into main contacts list
            if "distributors" in _data_distribution.keys():
                if "contacts" not in _resource.keys():  # pragma: no cover
                    _resource["contacts"] = []
                _resource["contacts"] = _resource["contacts"] + _data_distribution["distributors"]
                del _data_distribution["distributors"]
            _resource = {**_resource, **_data_distribution}

        data_quality = DataQuality(record=self.record, attributes=self.attributes)
        _data_quality = data_quality.make_config()
        if bool(_data_quality):
            _resource = {**_resource, **_data_quality}

        metadata_maintenance = MetadataMaintenance(record=self.record, attributes=self.attributes)
        _metadata_maintenance = metadata_maintenance.make_config()
        if bool(_metadata_maintenance):
            # noinspection PyTypeChecker
            self.attributes["maintenance"] = _metadata_maintenance

        if "contacts" in _resource.keys():
            _resource["contacts"] = Utils.contacts_condense_roles(contacts=_resource["contacts"])
        if bool(_resource):
            self.attributes["resource"] = _resource
        return MetadataRecordConfig(**self.attributes)

    def make_element(self) -> Element:
        metadata_record = Element(
            f"{{{self.ns.gmd}}}MD_Metadata",
            attrib={f"{{{ self.ns.xsi }}}schemaLocation": self.ns.schema_locations()},
            nsmap=self.ns.nsmap(),
        )

        identifier = FileIdentifier(record=metadata_record, attributes=self.attributes, parent_element=metadata_record)
        identifier.make_element()

        if "language" in self.attributes:
            language = Language(record=metadata_record, attributes=self.attributes)
            language.make_element()

        if "character_set" in self.attributes:
            character_set = CharacterSet(record=metadata_record, attributes=self.attributes)
            character_set.make_element()

        if "hierarchy_level" in self.attributes:
            hierarchy_level = HierarchyLevel(record=metadata_record, attributes=self.attributes)
            hierarchy_level.make_element()

        for contact_attributes in self.attributes["contacts"]:
            for role in contact_attributes["role"]:
                _contact = contact_attributes.copy()
                _contact["role"] = role

                contact = Contact(
                    record=metadata_record,
                    attributes=self.attributes,
                    parent_element=metadata_record,
                    element_attributes=_contact,
                )
                contact.make_element()

        date_stamp = DateStamp(record=metadata_record, attributes=self.attributes)
        date_stamp.make_element()

        if "metadata_standard" in self.attributes:
            metadata_standard = MetadataStandard(
                record=metadata_record,
                attributes=self.attributes,
                parent_element=metadata_record,
                element_attributes=self.attributes["metadata_standard"],
            )
            metadata_standard.make_element()

        if "reference_system_info" in self.attributes:
            reference_system_info = ReferenceSystemInfo(
                record=metadata_record,
                attributes=self.attributes,
                parent_element=metadata_record,
                element_attributes=self.attributes["reference_system_info"],
            )
            reference_system_info.make_element()

        data_identification = DataIdentification(record=metadata_record, attributes=self.attributes)
        data_identification.make_element()

        if (
            "formats" in self.attributes["resource"]
            or "transfer_options" in self.attributes["resource"]
            or (
                "contacts" in self.attributes["resource"]
                and Utils.contacts_have_role(contacts=self.attributes["resource"]["contacts"], role="distributor")
            )
        ):
            data_distribution = DataDistribution(record=metadata_record, attributes=self.attributes)
            data_distribution.make_element()

        if "measures" in self.attributes["resource"] or "lineage" in self.attributes["resource"]:
            data_quality = DataQuality(record=metadata_record, attributes=self.attributes)
            data_quality.make_element()

        if "maintenance" in self.attributes:
            metadata_maintenance = MetadataMaintenance(
                record=metadata_record,
                attributes=self.attributes,
                parent_element=metadata_record,
                element_attributes=self.attributes["maintenance"],
            )
            metadata_maintenance.make_element()

        return metadata_record


class MetadataRecordElement(_MetadataRecordElement):
    """
    Overloaded base MetadataRecordElement class

    Sets the type hint of the record attribute to the MetadataRecord class for this metadata standard
    """

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
            xpath=xpath,
        )
        self.ns = Namespaces()


class CodeListElement(MetadataRecordElement):
    """
    Derived MetadataRecordElement class defining an ISO code list element
    """

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
            xpath=xpath,
        )
        self.code_list_values = []
        self.code_list = None
        self.element = None
        self.element_code = None
        self.attribute = None

    def make_config(self) -> str:
        _ = ""

        value = self.record.xpath(
            f"{self.xpath}[@codeList = '{self.code_list}']/@codeListValue", namespaces=self.ns.nsmap(),
        )
        if len(value) == 1:
            _ = value[0]

        return _

    def make_element(self):
        code_list_element = SubElement(self.parent_element, self.element)
        if (
            self.attribute in self.element_attributes
            and self.element_attributes[self.attribute] in self.code_list_values
        ):
            code_list_value = SubElement(
                code_list_element,
                self.element_code,
                attrib={"codeList": self.code_list, "codeListValue": self.element_attributes[self.attribute]},
            )
            code_list_value.text = self.element_attributes[self.attribute]


# Element Classes


class FileIdentifier(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        value = self.record.xpath(
            "/gmd:MD_Metadata/gmd:fileIdentifier/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(value) == 1:
            _ = value[0]

        return _

    def make_element(self):
        if "file_identifier" in self.attributes:
            file_identifier_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}fileIdentifier")
            file_identifier_value = SubElement(file_identifier_element, f"{{{self.ns.gco}}}CharacterString")
            file_identifier_value.text = self.attributes["file_identifier"]


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
        self.code_list_values = ["utf8"]
        self.code_list = (
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/"
            "codelist/gmxCodelists.xml#MD_CharacterSetCode"
        )
        self.element = f"{{{self.ns.gmd}}}characterSet"
        self.element_code = f"{{{self.ns.gmd}}}MD_CharacterSetCode"
        self.attribute = "character_set"


class ScopeCode(CodeListElement):
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
            xpath=f"{xpath}/gmd:MD_ScopeCode",
        )
        self.code_list_values = [
            "attribute",
            "attributeType",
            "collectionHardware",
            "collectionSession",
            "dataset",
            "series",
            "nonGeographicDataset",
            "dimensionGroup",
            "feature",
            "featureType",
            "propertyType",
            "fieldSession",
            "software",
            "service",
            "model",
            "tile",
        ]
        self.code_list = (
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/"
            "codelist/gmxCodelists.xml#MD_ScopeCode"
        )
        self.element = f"{{{self.ns.gmd}}}level"
        self.element_code = f"{{{self.ns.gmd}}}MD_ScopeCode"
        self.attribute = "hierarchy_level"


class HierarchyLevel(ScopeCode):
    def __init__(
        self, record: MetadataRecord, attributes: dict, parent_element: Element = None, element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes,
            xpath="/gmd:MD_Metadata/gmd:hierarchyLevel",
        )
        self.element = f"{{{self.ns.gmd}}}hierarchyLevel"

    def make_element(self):
        super().make_element()
        hierarchy_level_name_element = SubElement(self.record, f"{{{self.ns.gmd}}}hierarchyLevelName")
        if self.attribute in self.attributes and self.attributes[self.attribute] in self.code_list_values:
            hierarchy_level_name_value = SubElement(hierarchy_level_name_element, f"{{{self.ns.gco}}}CharacterString")
            hierarchy_level_name_value.text = self.attributes[self.attribute]


class Contact(MetadataRecordElement):
    def make_config(self) -> dict:
        responsible_party = ResponsibleParty(record=self.record, attributes=self.attributes, xpath=self.xpath)
        _responsible_party = responsible_party.make_config()
        if not bool(_responsible_party):  # pragma: no cover
            return {}

        return _responsible_party

    def make_element(self):
        contact_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}contact")

        responsible_party = ResponsibleParty(
            record=self.record,
            attributes=self.attributes,
            parent_element=contact_element,
            element_attributes=self.element_attributes,
        )
        responsible_party.make_element()


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
            if "individual" not in _.keys():  # pragma: no cover
                _["individual"] = {}
            _["individual"]["href"] = individual_href[0]

        individual_title = self.record.xpath(
            f"{ self.xpath }/gmd:CI_ResponsibleParty/gmd:individualName/gmx:Anchor/@xlink:title",
            namespaces=self.ns.nsmap(),
        )
        if len(individual_title) > 0:
            if "individual" not in _.keys():  # pragma: no cover
                _["individual"] = {}
            _["individual"]["title"] = individual_title[0]

        organisation_name = self.record.xpath(
            f"{ self.xpath }/gmd:CI_ResponsibleParty/gmd:organisationName/gmx:Anchor/text() | "
            f"{ self.xpath }/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(organisation_name) > 0:
            if "organisation" not in _.keys():  # pragma: no cover
                _["organisation"] = {}
            _["organisation"]["name"] = organisation_name[0]

        organisation_href = self.record.xpath(
            f"{ self.xpath }/gmd:CI_ResponsibleParty/gmd:organisationName/gmx:Anchor/@xlink:href",
            namespaces=self.ns.nsmap(),
        )
        if len(organisation_href) > 0:
            if "organisation" not in _.keys():  # pragma: no cover
                _["organisation"] = {}
            _["organisation"]["href"] = organisation_href[0]

        organisation_title = self.record.xpath(
            f"{ self.xpath }/gmd:CI_ResponsibleParty/gmd:organisationName/gmx:Anchor/@xlink:title",
            namespaces=self.ns.nsmap(),
        )
        if len(organisation_title) > 0:
            if "organisation" not in _.keys():  # pragma: no cover
                _["organisation"] = {}
            _["organisation"]["title"] = organisation_title[0]

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
            if "address" not in _.keys():  # pragma: no cover
                _["address"] = {}
            _["address"]["city"] = city_value[0]

        administrative_area_value = self.record.xpath(
            f"{self.xpath}/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/"
            f"gmd:CI_Address/gmd:administrativeArea/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(administrative_area_value) > 0:
            if "address" not in _.keys():  # pragma: no cover
                _["address"] = {}
            _["address"]["administrative_area"] = administrative_area_value[0]

        postal_code_value = self.record.xpath(
            f"{self.xpath}/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/"
            f"gmd:CI_Address/gmd:postalCode/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(postal_code_value) > 0:
            if "address" not in _.keys():  # pragma: no cover
                _["address"] = {}
            _["address"]["postal_code"] = postal_code_value[0]

        country_value = self.record.xpath(
            f"{self.xpath}/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/"
            f"gmd:CI_Address/gmd:country/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(country_value) > 0:
            if "address" not in _.keys():  # pragma: no cover
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
        if list(_online_resource.keys()) == ["function"] and _online_resource["function"] == "":  # pragma: no cover
            _online_resource = {}
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
            record=self.record, attributes=self.attributes, xpath=f"{ self.xpath }/gmd:CI_OnlineResource/gmd:linkage",
        )
        _linkage = linkage.make_config()
        if "href" in _linkage.keys():
            _["href"] = _linkage["href"]

        name_value = self.record.xpath(
            f"{self.xpath}/gmd:CI_OnlineResource/gmd:name/gco:CharacterString/text()", namespaces=self.ns.nsmap(),
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
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:CI_OnlineResource/gmd:function",
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

        url_value = self.record.xpath(f"{self.xpath}/gmd:URL/text()", namespaces=self.ns.nsmap(),)
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


class DateStamp(MetadataRecordElement):
    def make_config(self) -> Optional[datetime]:
        _ = None

        value = self.record.xpath("/gmd:MD_Metadata/gmd:dateStamp/gco:DateTime/text()", namespaces=self.ns.nsmap())
        if len(value) == 1:
            try:
                _ = datetime.fromisoformat(value[0])
            except ValueError:  # pragma: no cover
                raise RuntimeError("Datestamp could not be parsed as an ISO datetime value")

        return _

    def make_element(self):
        date_stamp_element = SubElement(self.record, f"{{{self.ns.gmd}}}dateStamp")
        date_stamp_value = SubElement(date_stamp_element, f"{{{self.ns.gco}}}DateTime")
        date_stamp_value.text = Utils.format_date_string(self.attributes["date_stamp"])


class MetadataMaintenance(MetadataRecordElement):
    def make_config(self) -> dict:
        maintenance_information = MaintenanceInformation(
            record=self.record, attributes=self.attributes, xpath=f"/gmd:MD_Metadata/gmd:metadataMaintenance"
        )
        return maintenance_information.make_config()

    def make_element(self):
        if "maintenance" in self.attributes:
            metadata_maintenance_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}metadataMaintenance")

            maintenance_information = MaintenanceInformation(
                record=self.record,
                attributes=self.attributes,
                parent_element=metadata_maintenance_element,
                element_attributes=self.attributes["maintenance"],
            )
            maintenance_information.make_element()


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
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:maintenanceAndUpdateFrequency",
        )
        _maintenance_frequency = maintenance_frequency.make_config()
        if _maintenance_frequency != "":
            _["maintenance_frequency"] = _maintenance_frequency

        progress = MaintenanceProgress(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:maintenanceNote",
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


class MetadataStandard(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        standard_name = self.record.xpath(
            "/gmd:MD_Metadata/gmd:metadataStandardName/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(standard_name) == 1:
            _["name"] = standard_name[0]

        standard_version = self.record.xpath(
            "/gmd:MD_Metadata/gmd:metadataStandardVersion/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(standard_version) == 1:
            _["version"] = standard_version[0]

        return _

    def make_element(self):
        if "name" in self.element_attributes:
            metadata_standard_name_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}metadataStandardName")
            metadata_standard_name_value = SubElement(
                metadata_standard_name_element, f"{{{self.ns.gco}}}CharacterString"
            )
            metadata_standard_name_value.text = self.element_attributes["name"]

        if "version" in self.element_attributes:
            metadata_standard_version_element = SubElement(
                self.parent_element, f"{{{self.ns.gmd}}}metadataStandardVersion"
            )
            metadata_standard_version_value = SubElement(
                metadata_standard_version_element, f"{{{self.ns.gco}}}CharacterString"
            )
            metadata_standard_version_value.text = self.element_attributes["version"]


class ReferenceSystemInfo(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        authority = Citation(
            record=self.record,
            attributes=self.attributes,
            xpath=f"/gmd:MD_Metadata/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/"
            f"gmd:RS_Identifier/gmd:authority",
        )
        _authority = authority.make_config()
        if bool(_authority):
            _["authority"] = _authority

        code_value = self.record.xpath(
            "/gmd:MD_Metadata/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/"
            "gmd:RS_Identifier/gmd:code/gco:CharacterString/text() | /gmd:MD_Metadata/gmd:referenceSystemInfo/"
            "gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gmx:Anchor/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(code_value) == 1:
            if "code" not in _.keys():
                _["code"] = {}
            _["code"]["value"] = code_value[0]

        code_href = self.record.xpath(
            "/gmd:MD_Metadata/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/"
            "gmd:RS_Identifier/gmd:code/gmx:Anchor/@xlink:href",
            namespaces=self.ns.nsmap(),
        )
        if len(code_href) == 1:
            if "code" not in _.keys():  # pragma: no cover
                _["code"] = {}
            _["code"]["href"] = code_href[0]

        version_value = self.record.xpath(
            "/gmd:MD_Metadata/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/"
            "gmd:RS_Identifier/gmd:version/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(version_value) == 1:
            _["version"] = version_value[0]

        return _

    def make_element(self):
        reference_system_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}referenceSystemInfo")
        reference_system_element = SubElement(reference_system_wrapper, f"{{{self.ns.gmd}}}MD_ReferenceSystem")
        reference_system_identifier_wrapper = SubElement(
            reference_system_element, f"{{{self.ns.gmd}}}referenceSystemIdentifier"
        )
        reference_system_identifier_element = SubElement(
            reference_system_identifier_wrapper, f"{{{self.ns.gmd}}}RS_Identifier"
        )

        if "authority" in self.element_attributes:
            reference_system_identifier_authority_element = SubElement(
                reference_system_identifier_element, f"{{{self.ns.gmd}}}authority"
            )
            citation = Citation(
                record=self.record,
                attributes=self.attributes,
                parent_element=reference_system_identifier_authority_element,
                element_attributes=self.element_attributes["authority"],
            )
            citation.make_element()

        if "code" in self.element_attributes:
            reference_system_identifier_code_element = SubElement(
                reference_system_identifier_element, f"{{{self.ns.gmd}}}code"
            )
            if "href" in self.element_attributes["code"]:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=reference_system_identifier_code_element,
                    element_attributes=self.element_attributes["code"],
                    element_value=self.element_attributes["code"]["value"],
                )
                anchor.make_element()
            else:
                reference_system_identifier_code_value = SubElement(
                    reference_system_identifier_code_element, f"{{{self.ns.gco}}}CharacterString"
                )
                reference_system_identifier_code_value.text = self.element_attributes["code"]["value"]

        if "version" in self.element_attributes:
            reference_system_identifier_version_element = SubElement(
                reference_system_identifier_element, f"{{{self.ns.gmd}}}version"
            )
            reference_system_identifier_version_value = SubElement(
                reference_system_identifier_version_element, f"{{{self.ns.gco}}}CharacterString"
            )
            reference_system_identifier_version_value.text = self.element_attributes["version"]


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
            if "title" not in _.keys():  # pragma: no cover
                _["title"] = {}
            _["title"]["href"] = title_href[0]

        _dates = []
        dates_length = int(self.record.xpath(f"count({self.xpath}/gmd:date)", namespaces=self.ns.nsmap(),))
        for date_index in range(1, dates_length + 1):
            date_ = Date(record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:date[{date_index}]")
            _date = date_.make_config()
            if bool(_date):
                _dates.append(_date)
        if len(_dates) > 0:
            _["dates"] = _dates

        edition_value = self.record.xpath(
            f"{self.xpath}/gmd:edition/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(edition_value) == 1:
            _["edition"] = edition_value[0]

        _identifiers = []
        identifiers_length = int(self.record.xpath(f"count({self.xpath}/gmd:identifier)", namespaces=self.ns.nsmap(),))
        for identifier_index in range(1, identifiers_length + 1):
            identifier = Identifier(
                record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:identifier[{identifier_index}]"
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
            for date_attributes in self.element_attributes["dates"]:
                citation_date = Date(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=citation_element,
                    element_attributes=date_attributes,
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

        date_value = self.record.xpath(f"{self.xpath}/gmd:date/gco:Date/text()", namespaces=self.ns.nsmap())
        if len(date_value) == 1:
            try:
                if len(date_value[0]) == 4:
                    # Assume a year only date
                    date_value[0] = f"{date_value[0]}-01-01"
                    _["date_precision"] = "year"

                _["date"] = datetime.fromisoformat(date_value[0]).date()
            except ValueError:  # pragma: no cover
                raise RuntimeError("Date could not be parsed as an ISO date value")

        date_time_value = self.record.xpath(f"{self.xpath}/gmd:date/gco:DateTime/text()", namespaces=self.ns.nsmap())
        if len(date_time_value) == 1:
            try:
                _["date"] = datetime.fromisoformat(date_time_value[0])
            except ValueError:  # pragma: no cover
                raise RuntimeError("Date could not be parsed as an ISO datetime value")

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

        date_value = SubElement(date_element, date_value_element)
        date_value.text = Utils.format_date_string(self.element_attributes["date"])

        if "date_precision" in self.element_attributes:
            if self.element_attributes["date_precision"] == "year":
                date_value.text = str(self.element_attributes["date"].year)

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
            xpath=f"{xpath}/gmd:MD_Identifier",
        )

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

        identifier_title = self.record.xpath(
            f"{self.xpath}/gmd:code/gmx:Anchor/@xlink:title", namespaces=self.ns.nsmap()
        )
        if len(identifier_title) == 1:
            _["title"] = identifier_title[0]

        return _

    def make_element(self):
        identifier_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}identifier")
        identifier_wrapper = SubElement(identifier_container, f"{{{self.ns.gmd}}}MD_Identifier")
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


class DataIdentification(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            xpath=f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation",
        )
        _citation = citation.make_config()
        if bool(_citation):
            _ = {**_, **_citation}
        # # Remove erroneous citation contact
        # del _["contact"]

        abstract = Abstract(
            record=self.record,
            attributes=self.attributes,
            xpath=f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract",
        )
        _abstract = abstract.make_config()
        if _abstract != "":
            _["abstract"] = _abstract

        _contacts = []
        contacts_length = int(
            self.record.xpath(
                f"count(/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact)",
                namespaces=self.ns.nsmap(),
            )
        )
        for contact_index in range(1, contacts_length + 1):
            contact = PointOfContact(
                record=self.record,
                attributes=self.attributes,
                xpath=f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact"
                f"[{contact_index}]",
            )
            _contact = contact.make_config()
            if bool(_contact):
                _contacts.append(_contact)
        if len(_contacts) > 0:
            _["contacts"] = _contacts

        resource_maintenance = ResourceMaintenance(record=self.record, attributes=self.attributes)
        _resource_maintenance = resource_maintenance.make_config()
        if bool(_resource_maintenance):
            _["maintenance"] = _resource_maintenance

        _descriptive_keywords = []
        keywords_length = int(
            self.record.xpath(
                f"count(/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords)",
                namespaces=self.ns.nsmap(),
            )
        )
        for keyword_index in range(1, keywords_length + 1):
            keywords = DescriptiveKeywords(
                record=self.record,
                attributes=self.attributes,
                xpath=f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords"
                f"[{keyword_index}]",
            )
            _keywords = keywords.make_config()
            if bool(_keywords):
                _descriptive_keywords.append(_keywords)
        if len(_descriptive_keywords) > 0:
            _["keywords"] = _descriptive_keywords

        _resource_constraints = {}
        constraints_length = int(
            self.record.xpath(
                f"count(/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints)",
                namespaces=self.ns.nsmap(),
            )
        )
        for constraint_index in range(1, constraints_length + 1):
            constraint = ResourceConstraints(
                record=self.record,
                attributes=self.attributes,
                xpath=f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints"
                f"[{constraint_index}]",
            )
            _constraint = constraint.make_config()
            if bool(_constraint):
                if "access" in _constraint.keys():
                    if "access" not in _resource_constraints.keys():
                        _resource_constraints["access"] = []
                    _resource_constraints["access"].append(_constraint["access"])
                elif "usage" in _constraint.keys():
                    if "usage" not in _resource_constraints.keys():
                        _resource_constraints["usage"] = []
                    _resource_constraints["usage"].append(_constraint["usage"])
        if len(_resource_constraints) > 0:
            _["constraints"] = _resource_constraints

        spatial_representation_type = SpatialRepresentationType(
            record=self.record,
            attributes=self.attributes,
            xpath=f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType",
        )
        _spatial_representation_type = spatial_representation_type.make_config()
        if _spatial_representation_type != "":
            _["spatial_representation_type"] = _spatial_representation_type

        spatial_resolution = SpatialResolution(
            record=self.record,
            attributes=self.attributes,
            xpath=f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution",
        )
        _spatial_resolution = spatial_resolution.make_config()
        if _spatial_resolution != "":  # pragma: no cover
            _["spatial_resolution"] = _spatial_resolution

        language = Language(
            record=self.record,
            attributes=self.attributes,
            xpath="/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language",
        )
        _language = language.make_config()
        if _language != "":
            _["language"] = _language

        character_set = CharacterSet(
            record=self.record,
            attributes=self.attributes,
            xpath="/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:characterSet",
        )
        _character_set = character_set.make_config()
        if _character_set != "":  # pragma: no cover
            _["character_set"] = _character_set

        _topic_categories = []
        topics_length = int(
            self.record.xpath(
                f"count(/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory)",
                namespaces=self.ns.nsmap(),
            )
        )
        for topic_index in range(1, topics_length + 1):
            topic = TopicCategory(
                record=self.record,
                attributes=self.attributes,
                xpath=f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory"
                f"[{topic_index}]",
            )
            _topic = topic.make_config()
            if _topic != "":
                _topic_categories.append(_topic)
        if len(_topic_categories) > 0:
            _["topics"] = _topic_categories

        extent = Extent(record=self.record, attributes=self.attributes)
        _extent = extent.make_config()
        if bool(_extent):
            _["extent"] = _extent

        supplemental_information = SupplementalInformation(
            record=self.record,
            attributes=self.attributes,
            xpath=f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation",
        )
        _supplemental_information = supplemental_information.make_config()
        if _supplemental_information != "":
            _["supplemental_information"] = _supplemental_information

        return _

    def make_element(self):
        data_identification_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}identificationInfo")
        data_identification_element = SubElement(data_identification_wrapper, f"{{{self.ns.gmd}}}MD_DataIdentification")

        citation_wrapper = SubElement(data_identification_element, f"{{{self.ns.gmd}}}citation")
        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=citation_wrapper,
            element_attributes=self.element_attributes["resource"],
        )
        citation.make_element()

        abstract = Abstract(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes["resource"],
        )
        abstract.make_element()

        if "contacts" in self.attributes["resource"]:
            for point_of_contact_attributes in self.attributes["resource"]["contacts"]:
                for role in point_of_contact_attributes["role"]:
                    if role != "distributor":
                        _point_of_contact = point_of_contact_attributes.copy()
                        _point_of_contact["role"] = role

                        point_of_contact = PointOfContact(
                            record=self.record,
                            attributes=self.attributes,
                            parent_element=data_identification_element,
                            element_attributes=_point_of_contact,
                        )
                        point_of_contact.make_element()

        if "maintenance" in self.attributes["resource"]:
            resource_maintenance = ResourceMaintenance(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.element_attributes["resource"]["maintenance"],
            )
            resource_maintenance.make_element()

        if "keywords" in self.attributes["resource"]:
            for keyword_attributes in self.attributes["resource"]["keywords"]:
                descriptive_keywords = DescriptiveKeywords(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_identification_element,
                    element_attributes=keyword_attributes,
                )
                descriptive_keywords.make_element()

        if "constraints" in self.attributes["resource"]:
            constraints = ResourceConstraints(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["resource"]["constraints"],
            )
            constraints.make_element()

        if "spatial_representation_type" in self.attributes["resource"]:
            spatial_representation_type = SpatialRepresentationType(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["resource"],
            )
            spatial_representation_type.make_element()

        if "spatial_resolution" in self.attributes["resource"]:  # pragma: no cover
            spatial_resolution = SpatialResolution(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["resource"],
            )
            spatial_resolution.make_element()

        language = Language(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes["resource"],
        )
        language.make_element()

        if "topics" in self.attributes["resource"]:
            for topic_attribute in self.attributes["resource"]["topics"]:
                topic = TopicCategory(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_identification_element,
                    element_attributes={"topic": topic_attribute},
                )
                topic.make_element()

        if "extent" in self.attributes["resource"]:
            extent = Extent(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["resource"]["extent"],
            )
            extent.make_element()

        if "supplemental_information" in self.attributes["resource"]:
            supplemental_information = SupplementalInformation(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=self.attributes["resource"],
            )
            supplemental_information.make_element()


class Abstract(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        abstract_value = self.record.xpath(f"{self.xpath}/gco:CharacterString/text()", namespaces=self.ns.nsmap())
        if len(abstract_value) == 1:
            _ = abstract_value[0]

        return _

    def make_element(self):
        abstract_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}abstract")
        abstract_value = SubElement(abstract_element, f"{{{self.ns.gco}}}CharacterString")
        abstract_value.text = self.element_attributes["abstract"]


class PointOfContact(MetadataRecordElement):
    def make_config(self) -> dict:
        responsible_party = ResponsibleParty(record=self.record, attributes=self.attributes, xpath=self.xpath)
        _responsible_party = responsible_party.make_config()

        return _responsible_party

    def make_element(self):
        point_of_contact_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}pointOfContact")

        responsible_party = ResponsibleParty(
            record=self.record,
            attributes=self.attributes,
            parent_element=point_of_contact_element,
            element_attributes=self.element_attributes,
        )
        responsible_party.make_element()


class ResourceMaintenance(MetadataRecordElement):
    def make_config(self) -> dict:
        maintenance_information = MaintenanceInformation(
            record=self.record,
            attributes=self.attributes,
            xpath=f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance",
        )
        return maintenance_information.make_config()

    def make_element(self):
        resource_maintenance_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}resourceMaintenance")
        maintenance_information = MaintenanceInformation(
            record=self.record,
            attributes=self.attributes,
            parent_element=resource_maintenance_element,
            element_attributes=self.element_attributes,
        )
        maintenance_information.make_element()


class DescriptiveKeywords(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        _terms = []
        terms_values = self.record.xpath(
            f"{self.xpath}/gmd:MD_Keywords/gmd:keyword/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        for term in terms_values:
            _terms.append({"term": term})
        terms_links = self.record.xpath(
            f"{self.xpath}/gmd:MD_Keywords/gmd:keyword/gmx:Anchor", namespaces=self.ns.nsmap()
        )
        for term in terms_links:
            _term = {}
            _term_value = term.xpath("./text()", namespaces=self.ns.nsmap())
            if len(_term_value) > 0:
                _term["term"] = _term_value[0]
            _term_href = term.xpath("./@xlink:href", namespaces=self.ns.nsmap())
            if len(_term_href) > 0:
                _term["href"] = _term_href[0]
            if bool(_term):
                _terms.append(_term)
        if bool(_terms):
            _["terms"] = _terms

        descriptive_keywords_type = DescriptiveKeywordsType(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:MD_Keywords/gmd:type"
        )
        _descriptive_keywords_type = descriptive_keywords_type.make_config()
        if _descriptive_keywords_type != "":
            _["type"] = _descriptive_keywords_type

        thesaurus = Thesaurus(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:MD_Keywords/gmd:thesaurusName"
        )
        _thesaurus = thesaurus.make_config()
        if bool(_thesaurus):
            _["thesaurus"] = _thesaurus

        return _

    def make_element(self):
        keywords_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}descriptiveKeywords")
        keywords_element = SubElement(keywords_wrapper, f"{{{self.ns.gmd}}}MD_Keywords")

        for term in self.element_attributes["terms"]:
            term_element = SubElement(keywords_element, f"{{{self.ns.gmd}}}keyword")
            if "href" in term:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=term_element,
                    element_attributes=term,
                    element_value=term["term"],
                )
                anchor.make_element()
            else:
                term_value = SubElement(term_element, f"{{{self.ns.gco}}}CharacterString")
                term_value.text = term["term"]

        if "type" in self.element_attributes:
            keyword_type = DescriptiveKeywordsType(
                record=self.record,
                attributes=self.attributes,
                parent_element=keywords_element,
                element_attributes=self.element_attributes,
            )
            keyword_type.make_element()

        if "thesaurus" in self.element_attributes:
            thesaurus = Thesaurus(
                record=self.record,
                attributes=self.attributes,
                parent_element=keywords_element,
                element_attributes=self.element_attributes["thesaurus"],
            )
            thesaurus.make_element()


class DescriptiveKeywordsType(CodeListElement):
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
            xpath=f"{xpath}/gmd:MD_KeywordTypeCode",
        )
        self.code_list_values = ["discipline", "place", "stratum", "temporal", "theme"]
        self.code_list = (
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/"
            "codelist/gmxCodelists.xml#MD_KeywordTypeCode"
        )
        self.element = f"{{{self.ns.gmd}}}type"
        self.element_code = f"{{{self.ns.gmd}}}MD_KeywordTypeCode"
        self.attribute = "type"


class Thesaurus(MetadataRecordElement):
    def make_config(self) -> dict:
        citation = Citation(record=self.record, attributes=self.attributes, xpath=self.xpath)
        _citation = citation.make_config()

        return _citation

    def make_element(self):
        thesaurus_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}thesaurusName")

        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=thesaurus_element,
            element_attributes=self.element_attributes,
        )
        citation.make_element()


class ResourceConstraints(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        _id = self.record.xpath(f"{self.xpath}/gmd:MD_LegalConstraints/@id", namespaces=self.ns.nsmap())
        if len(_id) == 1:
            _id = _id[0]

        access_constraint = AccessConstraint(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:MD_LegalConstraints/gmd:accessConstraints",
        )
        _access_constraint = access_constraint.make_config()
        if _access_constraint != "":
            _["access"] = {"restriction_code": _access_constraint}

            other_constraint = OtherConstraints(
                record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:MD_LegalConstraints"
            )
            _other_constraint = other_constraint.make_config()
            if _other_constraint != "":
                _["access"]["statement"] = _other_constraint

        use_constraint = UseLimitation(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:MD_LegalConstraints/gmd:useLimitation",
        )
        _usage_constraint = use_constraint.make_config()
        if bool(_usage_constraint):
            _["usage"] = _usage_constraint

            if _id == "copyright":
                _["usage"] = {"copyright_licence": _usage_constraint}
                if (
                    "href" in _usage_constraint
                    and _usage_constraint["href"]
                    == "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"
                ):
                    # noinspection PyUnresolvedReferences
                    _["usage"]["copyright_licence"]["code"] = "OGL-UK-3.0"
            elif _id == "citation":
                _["usage"] = {"required_citation": _usage_constraint}

        if _id == "InspireLimitationsOnPublicAccess":
            limitations_on_access = self.record.xpath(
                f"{self.xpath}/gmd:MD_LegalConstraints/gmd:otherConstraints/gmx:Anchor/text()",
                namespaces=self.ns.nsmap(),
            )
            if len(limitations_on_access) == 1:
                if "access" in _.keys():
                    _["access"]["inspire_limitations_on_public_access"] = limitations_on_access[0]

        return _

    def make_element(self):
        if "access" in self.element_attributes:
            for access_constraint_attributes in self.element_attributes["access"]:
                constraints_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}resourceConstraints")
                constraints_element = SubElement(constraints_wrapper, f"{{{self.ns.gmd}}}MD_LegalConstraints")

                access_constraint = AccessConstraint(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=constraints_element,
                    element_attributes=access_constraint_attributes,
                )
                access_constraint.make_element()

                if "statement" in access_constraint_attributes:
                    element_attributes = {"value": deepcopy(access_constraint_attributes["statement"])}

                    other_constraint = OtherConstraints(
                        record=self.record,
                        attributes=self.attributes,
                        parent_element=constraints_element,
                        element_attributes=element_attributes,
                    )
                    other_constraint.make_element()

                if "inspire_limitations_on_public_access" in access_constraint_attributes:
                    constraints_element.set("id", "InspireLimitationsOnPublicAccess")

                    public_access_limitation = InspireLimitationsOnPublicAccess(
                        record=self.record,
                        attributes=self.attributes,
                        parent_element=constraints_element,
                        element_attributes=access_constraint_attributes,
                    )
                    public_access_limitation.make_element()

        if "usage" in self.element_attributes:
            for usage_constraint_attributes in self.element_attributes["usage"]:
                constraints_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}resourceConstraints")
                constraints_element = SubElement(constraints_wrapper, f"{{{self.ns.gmd}}}MD_LegalConstraints")

                if "statement" in usage_constraint_attributes:
                    element_attributes = {"value": deepcopy(usage_constraint_attributes["statement"])}

                    use_limitation = UseLimitation(
                        record=self.record,
                        attributes=self.attributes,
                        parent_element=constraints_element,
                        element_attributes=element_attributes,
                    )
                    use_limitation.make_element()

                if "copyright_licence" in usage_constraint_attributes:
                    constraints_element.set("id", "copyright")

                    element_attributes = deepcopy(usage_constraint_attributes["copyright_licence"])
                    element_attributes["value"] = element_attributes["statement"]

                    use_limitation = UseLimitation(
                        record=self.record,
                        attributes=self.attributes,
                        parent_element=constraints_element,
                        element_attributes=element_attributes,
                    )
                    use_limitation.make_element()

                if "required_citation" in usage_constraint_attributes:
                    constraints_element.set("id", "citation")

                    element_attributes = {}
                    if "statement" in usage_constraint_attributes["required_citation"]:
                        element_attributes["value"] = usage_constraint_attributes["required_citation"]["statement"]
                    elif "doi" in usage_constraint_attributes["required_citation"]:
                        citation = self._get_doi_citation(doi=usage_constraint_attributes["required_citation"]["doi"])
                        element_attributes["value"] = f'Cite this information as "{citation}"'

                    use_limitation = UseLimitation(
                        record=self.record,
                        attributes=self.attributes,
                        parent_element=constraints_element,
                        element_attributes=element_attributes,
                    )
                    use_limitation.make_element()

    @staticmethod
    def _get_doi_citation(doi: str) -> str:
        """
        Get citation for a DOI using crosscite.org

        This is a standalone method to allow for mocking during tests.

        @:type doi: str
        @:param doi: DOI to get citation for

        @:rtype: str
        @:return APA style citation for DOI
        """
        citation_response = requests.get(doi, headers={"Accept": "text/x-bibliography; style=apa; locale=en-GB"})
        citation_response.raise_for_status()
        return citation_response.text


class AccessConstraint(CodeListElement):
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
            xpath=f"{xpath}/gmd:MD_RestrictionCode",
        )
        self.code_list_values = [
            "copyright",
            "patent",
            "patentPending",
            "trademark",
            "license",
            "intellectualPropertyRights",
            "restricted",
            "otherRestrictions",
        ]
        self.code_list = (
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/"
            "codelist/gmxCodelists.xml#MD_RestrictionCode"
        )
        self.element = f"{{{self.ns.gmd}}}accessConstraints"
        self.element_code = f"{{{self.ns.gmd}}}MD_RestrictionCode"
        self.attribute = "restriction_code"


class InspireLimitationsOnPublicAccess(MetadataRecordElement):
    def make_element(self):
        other_constraints_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}otherConstraints")

        other_constraints_value = AnchorElement(
            record=self.record,
            attributes=self.attributes,
            parent_element=other_constraints_element,
            element_attributes={
                "href": f"http://inspire.ec.europa.eu/metadata-codelist/LimitationsOnPublicAccess/"
                f"{self.element_attributes['inspire_limitations_on_public_access']}"
            },
            element_value=self.element_attributes["inspire_limitations_on_public_access"],
        )
        other_constraints_value.make_element()


class OtherConstraints(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        other_constraint = self.record.xpath(
            f"{self.xpath}/gmd:otherConstraints/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(other_constraint) == 1:
            _ = other_constraint[0]

        return _

    def make_element(self):
        other_constraints_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}otherConstraints")
        other_constraints_value = SubElement(other_constraints_element, f"{{{self.ns.gco}}}CharacterString")
        other_constraints_value.text = self.element_attributes["value"]


class UseLimitation(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        use_constraint_statement = self.record.xpath(
            f"{self.xpath}/gco:CharacterString/text() | {self.xpath}/gmx:Anchor/text()", namespaces=self.ns.nsmap(),
        )
        if len(use_constraint_statement) == 1:
            _["statement"] = use_constraint_statement[0]

        use_constraint_href = self.record.xpath(f"{self.xpath}/gmx:Anchor/@xlink:href", namespaces=self.ns.nsmap())
        if len(use_constraint_href) == 1:
            _["href"] = use_constraint_href[0]

        return _

    def make_element(self):
        use_limitation_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}useLimitation")

        if "href" in self.element_attributes:
            use_limitation_value = AnchorElement(
                record=self.record,
                attributes=self.attributes,
                parent_element=use_limitation_element,
                element_attributes=self.element_attributes,
                element_value=self.element_attributes["value"],
            )
            use_limitation_value.make_element()
        else:
            use_limitation_value = SubElement(use_limitation_element, f"{{{self.ns.gco}}}CharacterString")
            use_limitation_value.text = self.element_attributes["value"]


class SupplementalInformation(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        supplemental_value = self.record.xpath(f"{self.xpath}/gco:CharacterString/text()", namespaces=self.ns.nsmap())
        if len(supplemental_value) == 1:
            _ = supplemental_value[0]

        return _

    def make_element(self):
        if "supplemental_information" in self.element_attributes:
            supplemental_info_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}supplementalInformation")
            supplemental_info_value = SubElement(supplemental_info_element, f"{{{self.ns.gco}}}CharacterString")
            supplemental_info_value.text = self.element_attributes["supplemental_information"]


class SpatialRepresentationType(CodeListElement):
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
            xpath=f"{xpath}/gmd:MD_SpatialRepresentationTypeCode",
        )
        self.code_list_values = ["vector", "grid", "textTable", "tin", "stereoModel", "video"]
        self.code_list = (
            "http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/"
            "codelist/gmxCodelists.xml#MD_SpatialRepresentationTypeCode"
        )
        self.element = f"{{{self.ns.gmd}}}spatialRepresentationType"
        self.element_code = f"{{{self.ns.gmd}}}MD_SpatialRepresentationTypeCode"
        self.attribute = "spatial_representation_type"


class SpatialResolution(MetadataRecordElement):  # pragma: no cover
    def make_config(self) -> str:
        _ = ""

        spatial_resolution_value = self.record.xpath(
            f"{self.xpath}/gmd:MD_Resolution/gco:Distance/text()", namespaces=self.ns.nsmap()
        )
        if len(spatial_resolution_value) == 1:
            _ = spatial_resolution_value[0]

        return _

    def make_element(self):
        resolution_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}spatialResolution")
        resolution_element = SubElement(resolution_wrapper, f"{{{self.ns.gmd}}}MD_Resolution")

        if self.element_attributes["spatial_resolution"] is None:
            SubElement(
                resolution_element, f"{{{self.ns.gco}}}Distance", attrib={f"{{{self.ns.gco}}}nilReason": "inapplicable"}
            )


class TopicCategory(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        topic_category_value = self.record.xpath(
            f"{self.xpath}/gmd:MD_TopicCategoryCode/text()", namespaces=self.ns.nsmap()
        )
        if len(topic_category_value) == 1:
            _ = topic_category_value[0]

        return _

    def make_element(self):
        topic_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}topicCategory")
        topic_value = SubElement(topic_element, f"{{{self.ns.gmd}}}MD_TopicCategoryCode")
        topic_value.text = self.element_attributes["topic"]


class Extent(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        geographic_extent = GeographicExtent(
            record=self.record,
            attributes=self.attributes,
            xpath=f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent",
        )
        _geographic_extent = geographic_extent.make_config()
        if bool(_geographic_extent):
            _["geographic"] = _geographic_extent

        temporal_extent = TemporalExtent(
            record=self.record,
            attributes=self.attributes,
            xpath=f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent",
        )
        _temporal_extent = temporal_extent.make_config()
        if bool(_temporal_extent):
            _["temporal"] = _temporal_extent

        vertical_extent = VerticalExtent(
            record=self.record,
            attributes=self.attributes,
            xpath=f"/gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/"
            f"gmd:verticalElement",
        )
        _vertical_extent = vertical_extent.make_config()
        if bool(_vertical_extent):
            _["vertical"] = _vertical_extent

        return _

    def make_element(self):
        extent_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}extent")
        extent_element = SubElement(extent_wrapper, f"{{{self.ns.gmd}}}EX_Extent")

        if "geographic" in self.element_attributes:
            geographic_extent = GeographicExtent(
                record=self.record,
                attributes=self.attributes,
                parent_element=extent_element,
                element_attributes=self.element_attributes["geographic"],
            )
            geographic_extent.make_element()

        if "temporal" in self.element_attributes:
            temporal_extent = TemporalExtent(
                record=self.record,
                attributes=self.attributes,
                parent_element=extent_element,
                element_attributes=self.element_attributes["temporal"],
            )
            temporal_extent.make_element()

        if "vertical" in self.element_attributes:
            vertical_extent = VerticalExtent(
                record=self.record,
                attributes=self.attributes,
                parent_element=extent_element,
                element_attributes=self.element_attributes["vertical"],
            )
            vertical_extent.make_element()


class GeographicExtent(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        bounding_box = BoundingBox(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:geographicElement",
        )
        _bounding_box = bounding_box.make_config()
        if bool(_bounding_box):
            _["bounding_box"] = _bounding_box

        return _

    def make_element(self):
        geographic_extent_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}geographicElement")

        if "bounding_box" in self.element_attributes:
            bounding_box = BoundingBox(
                record=self.record,
                attributes=self.attributes,
                parent_element=geographic_extent_element,
                element_attributes=self.element_attributes["bounding_box"],
            )
            bounding_box.make_element()


class BoundingBox(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        west_element_value = self.record.xpath(
            f"{self.xpath}/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(west_element_value) == 1:
            _["west_longitude"] = float(west_element_value[0])

        east_element_value = self.record.xpath(
            f"{self.xpath}/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(east_element_value) == 1:
            _["east_longitude"] = float(east_element_value[0])

        south_element_value = self.record.xpath(
            f"{self.xpath}/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(south_element_value) == 1:
            _["south_latitude"] = float(south_element_value[0])

        north_element_value = self.record.xpath(
            f"{self.xpath}/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(north_element_value) == 1:
            _["north_latitude"] = float(north_element_value[0])

        return _

    def make_element(self):
        bounding_box_element = SubElement(self.parent_element, f"{{{self.ns.gmd}}}EX_GeographicBoundingBox")

        west_element = SubElement(bounding_box_element, f"{{{self.ns.gmd}}}westBoundLongitude")
        west_value = SubElement(west_element, f"{{{self.ns.gco}}}Decimal")
        west_value.text = str(self.element_attributes["west_longitude"])

        east_element = SubElement(bounding_box_element, f"{{{self.ns.gmd}}}eastBoundLongitude")
        east_value = SubElement(east_element, f"{{{self.ns.gco}}}Decimal")
        east_value.text = str(self.element_attributes["east_longitude"])

        south_element = SubElement(bounding_box_element, f"{{{self.ns.gmd}}}southBoundLatitude")
        south_value = SubElement(south_element, f"{{{self.ns.gco}}}Decimal")
        south_value.text = str(self.element_attributes["south_latitude"])

        north_element = SubElement(bounding_box_element, f"{{{self.ns.gmd}}}northBoundLatitude")
        north_value = SubElement(north_element, f"{{{self.ns.gco}}}Decimal")
        north_value.text = str(self.element_attributes["north_latitude"])


class VerticalExtent(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        minimum_value = self.record.xpath(
            f"{self.xpath}/gmd:EX_VerticalExtent/gmd:minimumValue/gco:Real/text()", namespaces=self.ns.nsmap(),
        )
        if len(minimum_value) == 1:
            _["minimum"] = float(minimum_value[0])

        maximum_value = self.record.xpath(
            f"{self.xpath}/gmd:EX_VerticalExtent/gmd:maximumValue/gco:Real/text()", namespaces=self.ns.nsmap(),
        )
        if len(maximum_value) == 1:
            _["maximum"] = float(maximum_value[0])

        vertical_crs = VerticalCRS(
            record=self.record, attributes=self.attributes, xpath=f"{self.xpath}/gmd:EX_VerticalExtent"
        )
        _vertical_crs = vertical_crs.make_config()
        if bool(_vertical_crs):
            _ = {**_, **_vertical_crs}

        return _

    def make_element(self):
        vertical_extent_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}verticalElement")
        vertical_extent_element = SubElement(vertical_extent_wrapper, f"{{{self.ns.gmd}}}EX_VerticalExtent")

        if "minimum" in self.element_attributes:
            minimum_element = SubElement(vertical_extent_element, f"{{{self.ns.gmd}}}minimumValue")
            minimum_value = SubElement(minimum_element, f"{{{self.ns.gco}}}Real")
            minimum_value.text = str(self.element_attributes["minimum"])

        if "maximum" in self.element_attributes:
            maximum_element = SubElement(vertical_extent_element, f"{{{self.ns.gmd}}}maximumValue")
            maximum_value = SubElement(maximum_element, f"{{{self.ns.gco}}}Real")
            maximum_value.text = str(self.element_attributes["maximum"])

        if "code" in self.element_attributes:
            vertical_crs = VerticalCRS(
                record=self.record,
                attributes=self.attributes,
                parent_element=vertical_extent_element,
                element_attributes=self.element_attributes,
            )
            vertical_crs.make_element()


class VerticalCRS(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        identifier_value = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/@gml:id", namespaces=self.ns.nsmap(),
        )
        if len(identifier_value) == 1:
            _["identifier"] = identifier_value[0]

        code_value = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/gml:identifier/text()", namespaces=self.ns.nsmap(),
        )
        if len(code_value) == 1:
            _["code"] = code_value[0]

        name_value = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/gml:name/text()", namespaces=self.ns.nsmap(),
        )
        if len(name_value) == 1:
            _["name"] = name_value[0]

        remarks_value = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/gml:remarks/text()", namespaces=self.ns.nsmap(),
        )
        if len(remarks_value) == 1:
            _["remarks"] = remarks_value[0]

        domain_of_validity_href = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/gml:domainOfValidity/@xlink:href",
            namespaces=self.ns.nsmap(),
        )
        if len(domain_of_validity_href) == 1:
            _["domain_of_validity"] = {"href": domain_of_validity_href[0]}

        scope_value = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/gml:scope/text()", namespaces=self.ns.nsmap(),
        )
        if len(scope_value) == 1:
            _["scope"] = scope_value[0]

        vertical_cs_href = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/gml:verticalCS/@xlink:href", namespaces=self.ns.nsmap(),
        )
        if len(vertical_cs_href) == 1:
            _["vertical_cs"] = {"href": vertical_cs_href[0]}

        vertical_datum_href = self.record.xpath(
            f"{self.xpath}/gmd:verticalCRS/gml:VerticalCRS/gml:verticalDatum/@xlink:href", namespaces=self.ns.nsmap(),
        )
        if len(vertical_datum_href) == 1:
            _["vertical_datum"] = {"href": vertical_datum_href[0]}

        return _

    def make_element(self):
        vertical_crs_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}verticalCRS")
        vertical_crs_element = SubElement(
            vertical_crs_wrapper,
            f"{{{self.ns.gml}}}VerticalCRS",
            attrib={f"{{{self.ns.gml}}}id": self.element_attributes["identifier"]},
        )
        vertical_crs_code = SubElement(
            vertical_crs_element, f"{{{self.ns.gml}}}identifier", attrib={"codeSpace": "OGP"}
        )
        vertical_crs_code.text = self.element_attributes["code"]

        name = SubElement(vertical_crs_element, f"{{{self.ns.gml}}}name")
        name.text = self.element_attributes["name"]

        remarks = SubElement(vertical_crs_element, f"{{{self.ns.gml}}}remarks")
        remarks.text = self.element_attributes["remarks"]

        SubElement(
            vertical_crs_element,
            f"{{{self.ns.gml}}}domainOfValidity",
            attrib={f"{{{self.ns.xlink}}}href": self.element_attributes["domain_of_validity"]["href"]},
        )

        scope = SubElement(vertical_crs_element, f"{{{self.ns.gml}}}scope")
        scope.text = self.element_attributes["scope"]

        SubElement(
            vertical_crs_element,
            f"{{{self.ns.gml}}}verticalCS",
            attrib={f"{{{self.ns.xlink}}}href": self.element_attributes["vertical_cs"]["href"]},
        )

        SubElement(
            vertical_crs_element,
            f"{{{self.ns.gml}}}verticalDatum",
            attrib={f"{{{self.ns.xlink}}}href": self.element_attributes["vertical_datum"]["href"]},
        )


class TemporalExtent(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        begin_value = self.record.xpath(
            f"{self.xpath}/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:beginPosition/"
            f"text()",
            namespaces=self.ns.nsmap(),
        )
        if len(begin_value) == 1:
            if "period" not in _.keys():
                _["period"] = {}
            try:
                _["period"]["start"] = datetime.fromisoformat(begin_value[0])
            except ValueError:  # pragma: no cover
                raise RuntimeError("date time could not be parsed as an ISO datetime value")

        end_value = self.record.xpath(
            f"{self.xpath}/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:endPosition/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(end_value) == 1:
            if "period" not in _.keys():  # pragma: no cover
                _["period"] = {}
            try:
                _["period"]["end"] = datetime.fromisoformat(end_value[0])
            except ValueError:  # pragma: no cover
                raise RuntimeError("date time could not be parsed as an ISO datetime value")

        return _

    def make_element(self):
        temporal_extent_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}temporalElement")
        temporal_extent_wrapper = SubElement(temporal_extent_container, f"{{{self.ns.gmd}}}EX_TemporalExtent")
        temporal_extent_element = SubElement(temporal_extent_wrapper, f"{{{self.ns.gmd}}}extent")

        if "period" in self.element_attributes:
            time_period_element = SubElement(
                temporal_extent_element,
                f"{{{self.ns.gml}}}TimePeriod",
                attrib={f"{{{self.ns.gml}}}id": "boundingExtent"},
            )
            begin_position_element = SubElement(time_period_element, f"{{{self.ns.gml}}}beginPosition")
            begin_position_element.text = Utils.format_date_string(self.element_attributes["period"]["start"])

            end_position_element = SubElement(time_period_element, f"{{{self.ns.gml}}}endPosition")
            end_position_element.text = Utils.format_date_string(self.element_attributes["period"]["end"])


class DataDistribution(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        _distribution_formats = []
        formats_length = int(
            self.record.xpath(
                f"count(/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat)",
                namespaces=self.ns.nsmap(),
            )
        )
        for format_index in range(1, formats_length + 1):
            format_ = DistributionFormat(
                record=self.record,
                attributes=self.attributes,
                xpath=f"/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat"
                f"[{format_index}]",
            )
            _format = format_.make_config()
            if bool(_format):
                _distribution_formats.append(_format)
        if len(_distribution_formats) > 0:
            _["formats"] = _distribution_formats

        _distributors = []
        distributors_length = int(
            self.record.xpath(
                f"count(/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/"
                f"gmd:distributorContact)",
                namespaces=self.ns.nsmap(),
            )
        )
        for distributor_index in range(1, distributors_length + 1):
            distributor = Distributor(
                record=self.record,
                attributes=self.attributes,
                xpath=f"/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/"
                f"gmd:distributorContact"
                f"[{distributor_index}]",
            )
            _distributor = distributor.make_config()
            if bool(_distributor):
                _distributors.append(_distributor)
        if len(_distributors) > 0:
            _["distributors"] = _distributors

        _transfer_options = []
        transfer_options_length = int(
            self.record.xpath(
                f"count(/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions)",
                namespaces=self.ns.nsmap(),
            )
        )
        for transfer_option_index in range(1, transfer_options_length + 1):
            transfer_option = TransferOptions(
                record=self.record,
                attributes=self.attributes,
                xpath=f"/gmd:MD_Metadata/gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions"
                f"[{transfer_option_index}]",
            )
            _transfer_option = transfer_option.make_config()
            if bool(_transfer_option):
                _transfer_options.append(_transfer_option)
        if len(_transfer_options) > 0:
            _["transfer_options"] = _transfer_options

        return _

    def make_element(self):
        data_distribution_wrapper = SubElement(self.record, f"{{{self.ns.gmd}}}distributionInfo")
        data_distribution_element = SubElement(data_distribution_wrapper, f"{{{self.ns.gmd}}}MD_Distribution")

        if "formats" in self.attributes["resource"]:
            for format_attributes in self.attributes["resource"]["formats"]:
                distribution_format = DistributionFormat(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_distribution_element,
                    element_attributes=format_attributes,
                )
                distribution_format.make_element()

        if "contacts" in self.attributes["resource"]:
            for point_of_contact_attributes in self.attributes["resource"]["contacts"]:
                for role in point_of_contact_attributes["role"]:
                    if role == "distributor":
                        _point_of_contact = point_of_contact_attributes.copy()
                        _point_of_contact["role"] = role

                        distributor = Distributor(
                            record=self.record,
                            attributes=self.attributes,
                            parent_element=data_distribution_element,
                            element_attributes=_point_of_contact,
                        )
                        distributor.make_element()

        if "transfer_options" in self.attributes["resource"]:
            for transfer_attributes in self.attributes["resource"]["transfer_options"]:
                transfer_options = TransferOptions(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_distribution_element,
                    element_attributes=transfer_attributes,
                )
                transfer_options.make_element()


class DistributionFormat(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        format_name = self.record.xpath(
            f"{self.xpath}/gmd:MD_Format/gmd:name/gco:CharacterString/text() | "
            f"{self.xpath}/gmd:MD_Format/gmd:name/gmx:Anchor/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(format_name) == 1:
            _["format"] = format_name[0]

        format_href = self.record.xpath(
            f"{self.xpath}/gmd:MD_Format/gmd:name/gmx:Anchor/@xlink:href", namespaces=self.ns.nsmap(),
        )
        if len(format_href) == 1:
            _["href"] = format_href[0]

        version_value = self.record.xpath(
            f"{self.xpath}/gmd:MD_Format/gmd:version/gco:CharacterString/text()", namespaces=self.ns.nsmap(),
        )
        if len(version_value) == 1:  # pragma: no cover
            _["value"] = version_value[0]

        return _

    def make_element(self):
        distribution_format_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}distributionFormat")
        distribution_format_element = SubElement(distribution_format_wrapper, f"{{{self.ns.gmd}}}MD_Format")

        format_name_element = SubElement(distribution_format_element, f"{{{self.ns.gmd}}}name")
        if "href" in self.element_attributes:
            anchor = AnchorElement(
                record=self.record,
                attributes=self.attributes,
                parent_element=format_name_element,
                element_attributes=self.element_attributes,
                element_value=self.element_attributes["format"],
            )
            anchor.make_element()
        else:
            format_name_value = SubElement(format_name_element, f"{{{self.ns.gco}}}CharacterString")
            format_name_value.text = self.element_attributes["format"]

        if "version" in self.element_attributes:
            format_version_element = SubElement(distribution_format_element, f"{{{self.ns.gmd}}}version")
            format_version_value = SubElement(format_version_element, f"{{{self.ns.gco}}}CharacterString")
            format_version_value.text = self.element_attributes["version"]
        else:
            SubElement(
                distribution_format_element,
                f"{{{self.ns.gmd}}}version",
                attrib={f"{{{self.ns.gco}}}nilReason": "unknown"},
            )


class Distributor(MetadataRecordElement):
    def make_config(self) -> dict:
        responsible_party = ResponsibleParty(record=self.record, attributes=self.attributes, xpath=self.xpath)
        _responsible_party = responsible_party.make_config()
        if not bool(_responsible_party):  # pragma: no cover
            return {}

        return _responsible_party

    def make_element(self):
        distributor_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}distributor")
        distributor_wrapper = SubElement(distributor_container, f"{{{self.ns.gmd}}}MD_Distributor")
        distributor_element = SubElement(distributor_wrapper, f"{{{self.ns.gmd}}}distributorContact")

        responsible_party = ResponsibleParty(
            record=self.record,
            attributes=self.attributes,
            parent_element=distributor_element,
            element_attributes=self.element_attributes,
        )
        responsible_party.make_element()


class TransferOptions(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        size_unit = self.record.xpath(
            f"{self.xpath}/gmd:MD_DigitalTransferOptions/gmd:unitsOfDistribution/gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(size_unit) == 1:
            if "size" not in _.keys():
                _["size"] = {}
            _["size"]["unit"] = size_unit[0]

        size_magnitude = self.record.xpath(
            f"{self.xpath}/gmd:MD_DigitalTransferOptions/gmd:transferSize/gco:Real/text()", namespaces=self.ns.nsmap(),
        )
        if len(size_magnitude) == 1:
            if "size" not in _.keys():  # pragma: no cover
                _["size"] = {}
            _["size"]["magnitude"] = float(size_magnitude[0])

        online_resource = OnlineResource(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:MD_DigitalTransferOptions/gmd:onLine",
        )
        _online_resource = online_resource.make_config()
        if list(_online_resource.keys()) == ["function"] and _online_resource["function"] == "":  # pragma: no cover
            _online_resource = {}
        if bool(_online_resource):
            _["online_resource"] = _online_resource

        return _

    def make_element(self):
        transfer_options_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}transferOptions")
        transfer_options_wrapper = SubElement(transfer_options_container, f"{{{self.ns.gmd}}}MD_DigitalTransferOptions")

        if "size" in self.element_attributes:
            if "unit" in self.element_attributes["size"]:
                transfer_size_unit_element = SubElement(
                    transfer_options_wrapper, f"{{{self.ns.gmd}}}unitsOfDistribution"
                )
                transfer_size_unit_value = SubElement(transfer_size_unit_element, f"{{{self.ns.gco}}}CharacterString")
                transfer_size_unit_value.text = self.element_attributes["size"]["unit"]
            if "magnitude" in self.element_attributes["size"]:
                transfer_size_magnitude_element = SubElement(transfer_options_wrapper, f"{{{self.ns.gmd}}}transferSize")
                transfer_size_magnitude_value = SubElement(transfer_size_magnitude_element, f"{{{self.ns.gco}}}Real")
                transfer_size_magnitude_value.text = str(self.element_attributes["size"]["magnitude"])

        transfer_options_element = SubElement(transfer_options_wrapper, f"{{{self.ns.gmd}}}onLine")
        online_resource = OnlineResource(
            record=self.record,
            attributes=self.attributes,
            parent_element=transfer_options_element,
            element_attributes=self.element_attributes["online_resource"],
        )
        online_resource.make_element()


class DataQuality(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        report = Report(
            record=self.record,
            attributes=self.attributes,
            xpath=f"/gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/",
        )
        _report = report.make_config()
        if bool(_report):
            _["measures"] = [_report]

        lineage = Lineage(
            record=self.record,
            attributes=self.attributes,
            xpath=f"/gmd:MD_Metadata/gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage",
        )
        _lineage = lineage.make_config()
        if _lineage != "":
            _["lineage"] = _lineage

        return _

    def make_element(self):
        data_quality_wrapper = SubElement(self.record, f"{{{self.ns.gmd}}}dataQualityInfo")
        data_quality_element = SubElement(data_quality_wrapper, f"{{{self.ns.gmd}}}DQ_DataQuality")

        scope = Scope(record=self.record, attributes=self.attributes, parent_element=data_quality_element)
        scope.make_element()

        if "measures" in self.attributes["resource"]:
            for measure_attributes in self.attributes["resource"]["measures"]:
                report = Report(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_quality_element,
                    element_attributes=measure_attributes,
                )
                report.make_element()

        lineage = Lineage(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_quality_element,
            element_attributes=self.attributes["resource"],
        )
        lineage.make_element()


class Scope(MetadataRecordElement):
    def make_element(self):
        scope_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}scope")
        scope_element = SubElement(scope_wrapper, f"{{{self.ns.gmd}}}DQ_Scope")

        scope_code = ScopeCode(record=self.record, attributes=self.attributes, parent_element=scope_element)
        scope_code.make_element()


class Report(MetadataRecordElement):
    def make_config(self) -> dict:
        _ = {}

        report_code = self.record.xpath(
            f"{self.xpath}/gmd:DQ_DomainConsistency/gmd:measureIdentification/gmd:RS_Identifier/gmd:code/"
            f"gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(report_code) == 1:
            _["code"] = report_code[0]

        report_code_space = self.record.xpath(
            f"{self.xpath}/gmd:DQ_DomainConsistency/gmd:measureIdentification/gmd:RS_Identifier/gmd:codeSpace/"
            f"gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(report_code_space) == 1:
            _["code_space"] = report_code_space[0]

        specification = Citation(
            record=self.record,
            attributes=self.attributes,
            xpath=f"{self.xpath}/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:specification",
        )
        _specification = specification.make_config()
        if bool(_specification):
            _ = {**_, **_specification}

        report_explanation = self.record.xpath(
            f"{self.xpath}/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:explanation/"
            f"gco:CharacterString/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(report_explanation) == 1:
            _["explanation"] = report_explanation[0]

        report_result = self.record.xpath(
            f"{self.xpath}/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:pass/gco:Boolean/text()",
            namespaces=self.ns.nsmap(),
        )
        if len(report_result) == 1:
            _["pass"] = bool(report_result[0])

        return _

    def make_element(self):
        report_wrapper = SubElement(self.parent_element, f"{{{self.ns.gmd}}}report")
        report_element = SubElement(report_wrapper, f"{{{self.ns.gmd}}}DQ_DomainConsistency")

        identification_wrapper = SubElement(report_element, f"{{{self.ns.gmd}}}measureIdentification")
        identification_element = SubElement(identification_wrapper, f"{{{self.ns.gmd}}}RS_Identifier")

        identification_code_element = SubElement(identification_element, f"{{{self.ns.gmd}}}code")
        identification_code_value = SubElement(identification_code_element, f"{{{self.ns.gco}}}CharacterString")
        identification_code_value.text = self.element_attributes["code"]

        identification_code_space_element = SubElement(identification_element, f"{{{self.ns.gmd}}}codeSpace")
        identification_code_space_value = SubElement(
            identification_code_space_element, f"{{{self.ns.gco}}}CharacterString"
        )
        identification_code_space_value.text = self.element_attributes["code_space"]

        result_wrapper = SubElement(report_element, f"{{{self.ns.gmd}}}result")
        result_element = SubElement(result_wrapper, f"{{{self.ns.gmd}}}DQ_ConformanceResult")

        specification_element = SubElement(result_element, f"{{{self.ns.gmd}}}specification")
        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=specification_element,
            element_attributes=self.element_attributes,
        )
        citation.make_element()

        explanation_element = SubElement(result_element, f"{{{self.ns.gmd}}}explanation")
        explanation_value = SubElement(explanation_element, f"{{{self.ns.gco}}}CharacterString")
        explanation_value.text = self.element_attributes["explanation"]

        pass_element = SubElement(result_element, f"{{{self.ns.gmd}}}pass")
        pass_value = SubElement(pass_element, f"{{{self.ns.gco}}}Boolean")
        pass_value.text = str(self.element_attributes["pass"]).lower()


class Lineage(MetadataRecordElement):
    def make_config(self) -> str:
        _ = ""

        lineage_value = self.record.xpath(
            f"{self.xpath}/gmd:LI_Lineage/gmd:statement/gco:CharacterString/text()", namespaces=self.ns.nsmap()
        )
        if len(lineage_value) == 1:
            _ = lineage_value[0]

        return _

    def make_element(self):
        if "lineage" in self.element_attributes:
            lineage_container = SubElement(self.parent_element, f"{{{self.ns.gmd}}}lineage")
            lineage_wrapper = SubElement(lineage_container, f"{{{self.ns.gmd}}}LI_Lineage")
            lineage_element = SubElement(lineage_wrapper, f"{{{self.ns.gmd}}}statement")
            lineage_value = SubElement(lineage_element, f"{{{self.ns.gco}}}CharacterString")
            lineage_value.text = self.element_attributes["lineage"]
