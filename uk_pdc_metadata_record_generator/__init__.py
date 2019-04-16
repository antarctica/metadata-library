from datetime import datetime
from typing import Optional

from flask import Flask, Response

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# We don't currently allow untrusted/user-provided XML so this is not a risk
from lxml import etree  # nosec
from lxml.etree import Element  # nosec

from tests import config


class Namespaces(object):
    gmd = 'http://www.isotc211.org/2005/gmd'
    gco = 'http://www.isotc211.org/2005/gco'
    gml = 'http://www.opengis.net/gml/3.2'
    gmx = 'http://www.isotc211.org/2005/gmx'
    srv = 'http://www.isotc211.org/2005/srv'
    xlink = 'http://www.w3.org/1999/xlink'
    xsi = 'http://www.w3.org/2001/XMLSchema-instance'

    _schema_locations = {
        'gmd': 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gmd/gmd.xsd',
        'gco': 'https://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gco/gco.xsd',
        'gmx': 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gmx/gmx.xsd',
        'srv': 'http://inspire.ec.europa.eu/draft-schemas/inspire-md-schemas/srv/1.0/srv.xsd'
    }

    def __init__(self):
        self._namespaces = {
            'gmd': self.gmd,
            'gco': self.gco,
            'gml': self.gml,
            'gmx': self.gmx,
            'srv': self.srv,
            'xlink': self.xlink,
            'xsi': self.xsi
        }

    def nsmap(self) -> dict:
        nsmap = {}
        for prefix, namespace in self._namespaces.items():
            nsmap[prefix] = namespace

        return nsmap

    def schema_locations(self) -> str:
        schema_locations = ''
        for prefix, location in self._schema_locations.items():
            schema_locations = f"{ schema_locations } { self._namespaces[prefix] } { location }"

        return schema_locations.lstrip()


class MetadataRecord(object):
    def __init__(self, **kwargs):
        self._ns = Namespaces()
        self.attributes = kwargs

        self.record = self._record()
        self._file_identifier()
        self._language()
        self._character_set()
        self._hierarchy_level()
        self._contact()
        self._date_stamp()
        self._metadata_maintenance()
        self._metadata_standard()
        self._reference_system_identifier()
        self._data_identification()

    def _record(self) -> Element:
        return etree.Element(
            f"{{{self._ns.gmd}}}MD_Metadata",
            attrib={f"{{{ self._ns.xsi }}}schemaLocation": self._ns.schema_locations()},
            nsmap=self._ns.nsmap()
        )

    def _file_identifier(self):
        file_identifier = etree.SubElement(self.record, f"{{{ self._ns.gmd }}}fileIdentifier")

        if 'file_identifier' in self.attributes:
            file_identifier_val = etree.SubElement(file_identifier, f"{{{ self._ns.gco }}}CharacterString")
            file_identifier_val.text = self.attributes['file_identifier']

    def _language(self):
        language = Language(record=self.record, attributes=self.attributes)
        language.make_element()

    def _character_set(self):
        character_set = CharacterSet(record=self.record, attributes=self.attributes)
        character_set.make_element()

    def _hierarchy_level(self):
        hierarchy_level = HierarchyLevel(record=self.record, attributes=self.attributes)
        hierarchy_level.make_element()

    def _contact(self):
        contact = Contact(record=self.record, attributes=self.attributes)
        contact.make_element()

    def _date_stamp(self):
        date_stamp = DateStamp(record=self.record, attributes=self.attributes)
        date_stamp.make_element()

    def _metadata_maintenance(self):
        metadata_maintenance = MetadataMaintenance(record=self.record, attributes=self.attributes)
        metadata_maintenance.make_element()

    def _metadata_standard(self):
        metadata_standard = MetadataStandard(record=self.record, attributes=self.attributes)
        metadata_standard.make_element()

    def _reference_system_identifier(self):
        reference_system_identifier = ReferenceSystemInfo(record=self.record, attributes=self.attributes)
        reference_system_identifier.make_element()

    def _data_identification(self):
        data_identification = DataIdentification(record=self.record, attributes=self.attributes)
        data_identification.make_element()


class MetadataRecordElement(object):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        self._ns = Namespaces()
        self.record = record
        self.attributes = attributes
        self.parent_element = parent_element
        self.element_attributes = element_attributes

    def make_element(self):
        pass


class CodeListElement(MetadataRecordElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        if parent_element is None:
            self.parent_element = self.record
        if element_attributes is None:
            self.element_attributes = self.attributes

        self.element = None
        self.element_code = None
        self.attribute = None

        self.code_list = None
        self.code_list_values = []

    def make_element(self):
        code_list_element = etree.SubElement(self.parent_element, self.element)
        if self.attribute in self.element_attributes \
                and self.element_attributes[self.attribute] in self.code_list_values:
            code_list_value = etree.SubElement(
                code_list_element,
                self.element_code,
                attrib={
                    'codeList': self.code_list,
                    'codeListValue': self.element_attributes[self.attribute]
                }
            )
            code_list_value.text = self.element_attributes[self.attribute]


class Language(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = ['eng']
        self.code_list = 'http://www.loc.gov/standards/iso639-2/php/code_list.php'
        self.element = f"{{{self._ns.gmd}}}language"
        self.element_code = f"{{{self._ns.gmd}}}LanguageCode"
        self.attribute = 'language'


class CharacterSet(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = ['utf8']
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#MD_CharacterSetCode'
        self.element = f"{{{self._ns.gmd}}}characterSet"
        self.element_code = f"{{{self._ns.gmd}}}MD_CharacterSetCode"
        self.attribute = 'character_set'


class HierarchyLevel(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'attribute',
            'attributeType',
            'collectionHardware',
            'collectionSession',
            'dataset',
            'series',
            'nonGeographicDataset',
            'dimensionGroup',
            'feature',
            'featureType',
            'propertyType',
            'fieldSession',
            'software',
            'service',
            'model',
            'tile'
        ]
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#MD_ScopeCode'
        self.element = f"{{{self._ns.gmd}}}hierarchyLevel"
        self.element_code = f"{{{self._ns.gmd}}}MD_ScopeCode"
        self.attribute = 'hierarchy-level'

    def make_element(self):
        super().make_element()
        hierarchy_level_name_element = etree.SubElement(self.record, f"{{{self._ns.gmd}}}hierarchyLevelName")
        if self.attribute in self.attributes and self.attributes[self.attribute] in self.code_list_values:
            hierarchy_level_name_value = etree.SubElement(
                hierarchy_level_name_element,
                f"{{{self._ns.gco}}}CharacterString"
            )
            hierarchy_level_name_value.text = self.attributes[self.attribute]


class Contact(MetadataRecordElement):
    def make_element(self):
        contact_element = etree.SubElement(self.record, f"{{{self._ns.gmd}}}contact")

        if 'contact' in self.attributes:
            responsible_party = ResponsibleParty(
                record=self.record,
                attributes=self.attributes,
                parent_element=contact_element,
                element_attributes=self.attributes['contact']
            )
            responsible_party.make_element()


class ResponsibleParty(MetadataRecordElement):
    def make_element(self):
        responsible_party_element = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}CI_ResponsibleParty")

        if 'individual' in self.element_attributes and 'name' in self.element_attributes['individual']:
            individual_element = etree.SubElement(responsible_party_element, f"{{{self._ns.gmd}}}individualName")
            if 'href' in self.element_attributes['individual']:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=individual_element,
                    element_attributes=self.element_attributes['individual'],
                    element_value=self.element_attributes['individual']['name']
                )
                anchor.make_element()
            else:
                individual_value = etree.SubElement(individual_element, f"{{{self._ns.gco}}}CharacterString")
                individual_value.text = self.element_attributes['individual']['name']

        if 'organisation' in self.element_attributes and 'name' in self.element_attributes['organisation']:
            organisation_element = etree.SubElement(responsible_party_element, f"{{{self._ns.gmd}}}organisationName")
            if 'href' in self.element_attributes['organisation']:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=organisation_element,
                    element_attributes=self.element_attributes['organisation'],
                    element_value=self.element_attributes['organisation']['name']
                )
                anchor.make_element()
            else:
                organisation_name_value = etree.SubElement(organisation_element, f"{{{self._ns.gco}}}CharacterString")
                organisation_name_value.text = self.element_attributes['organisation']['name']

        contact_wrapper = etree.SubElement(responsible_party_element, f"{{{self._ns.gmd}}}contactInfo")
        contact_element = etree.SubElement(contact_wrapper, f"{{{self._ns.gmd}}}CI_Contact")

        if 'phone' in self.element_attributes:
            phone_wrapper = etree.SubElement(contact_element, f"{{{self._ns.gmd}}}phone")
            phone_element = etree.SubElement(phone_wrapper, f"{{{self._ns.gmd}}}CI_Telephone")
            phone_voice = etree.SubElement(phone_element, f"{{{self._ns.gmd}}}voice")
            phone_voice_value = etree.SubElement(phone_voice, f"{{{self._ns.gco}}}CharacterString")
            phone_voice_value.text = self.element_attributes['phone']

        address_wrapper = etree.SubElement(contact_element, f"{{{self._ns.gmd}}}address")
        address_element = etree.SubElement(address_wrapper, f"{{{self._ns.gmd}}}CI_Address")

        if 'address' in self.element_attributes:
            if 'delivery-point' in self.element_attributes['address']:
                delivery_point_element = etree.SubElement(address_element, f"{{{self._ns.gmd}}}deliveryPoint")
                delivery_point_value = etree.SubElement(
                    delivery_point_element,
                    f"{{{self._ns.gco}}}CharacterString"
                )
                delivery_point_value.text = self.element_attributes['address']['delivery-point']
            if 'city' in self.element_attributes['address']:
                city_element = etree.SubElement(address_element, f"{{{self._ns.gmd}}}city")
                city_value = etree.SubElement(city_element, f"{{{self._ns.gco}}}CharacterString")
                city_value.text = self.element_attributes['address']['city']
            if 'administrative-area' in self.element_attributes['address']:
                administrative_area_element = etree.SubElement(
                    address_element,
                    f"{{{self._ns.gmd}}}administrativeArea"
                )
                administrative_area_value = etree.SubElement(
                    administrative_area_element,
                    f"{{{self._ns.gco}}}CharacterString"
                )
                administrative_area_value.text = self.element_attributes['address']['administrative-area']
            if 'postal-code' in self.element_attributes['address']:
                postal_code_element = etree.SubElement(address_element, f"{{{self._ns.gmd}}}postalCode")
                postal_code_value = etree.SubElement(postal_code_element, f"{{{self._ns.gco}}}CharacterString")
                postal_code_value.text = self.element_attributes['address']['postal-code']
            if 'country' in self.element_attributes['address']:
                country_element = etree.SubElement(address_element, f"{{{self._ns.gmd}}}country")
                country_value = etree.SubElement(country_element, f"{{{self._ns.gco}}}CharacterString")
                country_value.text = self.element_attributes['address']['country']

        if 'email' in self.element_attributes:
            email_element = etree.SubElement(address_element, f"{{{self._ns.gmd}}}electronicMailAddress")
            email_value = etree.SubElement(email_element, f"{{{self._ns.gco}}}CharacterString")
            email_value.text = self.element_attributes['email']
        else:
            etree.SubElement(
                address_element,
                f"{{{self._ns.gmd}}}electronicMailAddress",
                attrib={f"{{{self._ns.gco}}}nilReason": 'unknown'}
            )

        if 'online-resource' in self.element_attributes:
            online_resource_wrapper = etree.SubElement(contact_element, f"{{{self._ns.gmd}}}onlineResource")
            online_resource_element = etree.SubElement(
                online_resource_wrapper,
                f"{{{self._ns.gmd}}}CI_OnlineResource"
            )

            if 'href' in self.element_attributes['online-resource']:
                linkage = Linkage(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=online_resource_element,
                    element_attributes=self.element_attributes['online-resource']
                )
                linkage.make_element()

            if 'title' in self.element_attributes['online-resource']:
                title_wrapper = etree.SubElement(online_resource_element, f"{{{self._ns.gmd}}}name")
                title_element = etree.SubElement(title_wrapper, f"{{{self._ns.gco}}}CharacterString")
                title_element.text = self.element_attributes['online-resource']['title']

            if 'description' in self.element_attributes['online-resource']:
                title_wrapper = etree.SubElement(online_resource_element, f"{{{self._ns.gmd}}}description")
                title_element = etree.SubElement(title_wrapper, f"{{{self._ns.gco}}}CharacterString")
                title_element.text = self.element_attributes['online-resource']['description']

            if 'function' in self.element_attributes['online-resource']:
                function = OnlineRole(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=responsible_party_element,
                    element_attributes=self.element_attributes
                )
                function.make_element()

        if 'role' in self.element_attributes:
            role = Role(
                record=self.record,
                attributes=self.attributes,
                parent_element=responsible_party_element,
                element_attributes=self.element_attributes
            )
            role.make_element()


class Linkage(MetadataRecordElement):
    def make_element(self):
        linkage_element = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}linkage")
        if 'href' in self.element_attributes:
            url_value = etree.SubElement(linkage_element, f"{{{self._ns.gmd}}}URL")
            url_value.text = self.element_attributes['href']


class Role(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'resourceProvider',
            'custodian',
            'owner',
            'user',
            'distributor',
            'originator',
            'pointOfContact',
            'principalInvestigator',
            'processor',
            'publisher',
            'author'
        ]
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#CI_RoleCode'
        self.element = f"{{{self._ns.gmd}}}role"
        self.element_code = f"{{{self._ns.gmd}}}CI_RoleCode"
        self.attribute = 'role'


class OnlineRole(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'download',
            'information',
            'offlineAccess',
            'order',
            'search'
        ]
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#CI_OnLineFunctionCode'
        self.element = f"{{{self._ns.gmd}}}function"
        self.element_code = f"{{{self._ns.gmd}}}CI_OnLineFunctionCode"
        self.attribute = 'function'


class DateStamp(MetadataRecordElement):
    def make_element(self):
        date_stamp_element = etree.SubElement(self.record, f"{{{self._ns.gmd}}}dateStamp")
        date_stamp_value = etree.SubElement(date_stamp_element, f"{{{self._ns.gco}}}DateTime")
        date_stamp_value.text = self.attributes['date-stamp'].isoformat()


class MetadataMaintenance(MetadataRecordElement):
    def make_element(self):
        metadata_maintenance_element = etree.SubElement(self.record, f"{{{self._ns.gmd}}}metadataMaintenance")
        maintenance_information = MaintenanceInformation(
            record=self.record,
            attributes=self.attributes,
            parent_element=metadata_maintenance_element,
            element_attributes=self.attributes['maintenance']
        )
        maintenance_information.make_element()


class MaintenanceInformation(MetadataRecordElement):
    def make_element(self):
        maintenance_element = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}MD_MaintenanceInformation")

        if 'maintenance-frequency' in self.element_attributes:
            maintenance_and_update_frequency = MaintenanceAndUpdateFrequency(
                record=self.record,
                attributes=self.attributes,
                parent_element=maintenance_element,
                element_attributes=self.element_attributes
            )
            maintenance_and_update_frequency.make_element()
        if 'progress' in self.element_attributes:
            maintenance_process = MaintenanceProgress(
                record=self.record,
                attributes=self.attributes,
                parent_element=maintenance_element,
                element_attributes=self.element_attributes
            )
            maintenance_process.make_element()


class MaintenanceAndUpdateFrequency(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'continual',
            'daily',
            'weekly',
            'fortnightly',
            'monthly',
            'quarterly',
            'biannually',
            'annually',
            'asNeeded',
            'irregular',
            'notPlanned',
            'unknown'
        ]
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#MD_MaintenanceFrequencyCode'
        self.element = f"{{{self._ns.gmd}}}maintenanceAndUpdateFrequency"
        self.element_code = f"{{{self._ns.gmd}}}MD_MaintenanceFrequencyCode"
        self.attribute = 'maintenance-frequency'


class MaintenanceProgress(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'completed',
            'historicalArchive',
            'obsolete',
            'onGoing',
            'planned',
            'required',
            'underDevelopment'
        ]
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#MD_ProgressCode'
        self.element = f"{{{self._ns.gmd}}}maintenanceNote"
        self.element_code = f"{{{self._ns.gmd}}}MD_ProgressCode"
        self.attribute = 'progress'


class MetadataStandard(MetadataRecordElement):
    def make_element(self):
        if 'name' in self.attributes['metadata-standard']:
            metadata_standard_name_element = etree.SubElement(self.record, f"{{{self._ns.gmd}}}metadataStandardName")
            metadata_standard_name_value = etree.SubElement(
                metadata_standard_name_element,
                f"{{{self._ns.gco}}}CharacterString"
            )
            metadata_standard_name_value.text = self.attributes['metadata-standard']['name']
        if 'version' in self.attributes['metadata-standard']:
            metadata_standard_version_element = etree.SubElement(
                self.record,
                f"{{{self._ns.gmd}}}metadataStandardVersion"
            )
            metadata_standard_version_value = etree.SubElement(
                metadata_standard_version_element,
                f"{{{self._ns.gco}}}CharacterString"
            )
            metadata_standard_version_value.text = self.attributes['metadata-standard']['version']


class ReferenceSystemInfo(MetadataRecordElement):
    epsg_citation = {
        'title': {
            'value': 'European Petroleum Survey Group (EPSG) Geodetic Parameter Registry'
        },
        'dates': [{
            'date': datetime(2008, 11, 12),
            'date-type': 'publication'
        }],
        'contact': {
            'organisation': {
                'name': 'European Petroleum Survey Group'
            },
            'email': 'EPSGadministrator@iogp.org',
            'online-resource': {
                'href': 'https://www.epsg-registry.org/',
                'function': 'information'
            },
            'role': 'publisher'
        }
    }

    def make_element(self):
        reference_system_wrapper = etree.SubElement(self.record, f"{{{self._ns.gmd}}}referenceSystemInfo")
        reference_system_element = etree.SubElement(reference_system_wrapper, f"{{{self._ns.gmd}}}MD_ReferenceSystem")
        reference_system_identifier_wrapper = etree.SubElement(
            reference_system_element,
            f"{{{self._ns.gmd}}}referenceSystemIdentifier"
        )
        reference_system_identifier_element = etree.SubElement(
            reference_system_identifier_wrapper,
            f"{{{self._ns.gmd}}}RS_Identifier"
        )

        if 'code' in self.attributes['reference-system-info']:
            reference_system_identifier_code_element = etree.SubElement(
                reference_system_identifier_element,
                f"{{{self._ns.gmd}}}code"
            )
            _epsg_code = self._get_epsg_code(self.attributes['reference-system-info']['code'])
            if _epsg_code is not None:
                reference_system_identifier_authority_element = etree.SubElement(
                    reference_system_identifier_element,
                    f"{{{self._ns.gmd}}}authority"
                )
                citation = Citation(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=reference_system_identifier_authority_element,
                    element_attributes=self.epsg_citation
                )
                citation.make_element()

                reference_system_identifier_code_value = etree.SubElement(
                    reference_system_identifier_code_element,
                    f"{{{self._ns.gmx}}}Anchor",
                    attrib={
                        f"{{{self._ns.xlink}}}href": f"http://www.opengis.net/def/crs/EPSG/0/{ _epsg_code }",
                        f"{{{self._ns.xlink}}}actuate": 'onRequest'
                    }
                )
            else:
                reference_system_identifier_code_value = etree.SubElement(
                    reference_system_identifier_code_element,
                    f"{{{self._ns.gco}}}CharacterString"
                )
            reference_system_identifier_code_value.text = self.attributes['reference-system-info']['code']

        if 'version' in self.attributes['reference-system-info']:
            reference_system_identifier_version_element = etree.SubElement(
                reference_system_identifier_element,
                f"{{{self._ns.gmd}}}version"
            )
            reference_system_identifier_version_value = etree.SubElement(
                reference_system_identifier_version_element,
                f"{{{self._ns.gco}}}CharacterString"
            )
            reference_system_identifier_version_value.text = self.attributes['reference-system-info']['version']

    @staticmethod
    def _get_epsg_code(candidate_code: str) -> Optional[str]:
        if candidate_code.startswith('urn:ogc:def:crs:EPSG'):
            code_parts = candidate_code.split(':')
            return code_parts[-1]

        return None


class Citation(MetadataRecordElement):
    def make_element(self):
        citation_element = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}CI_Citation")

        if 'title' in self.element_attributes:
            title_element = etree.SubElement(citation_element, f"{{{self._ns.gmd}}}title")
            if 'href' in self.element_attributes['title']:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=title_element,
                    element_attributes=self.element_attributes['title'],
                    element_value=self.element_attributes['title']['value']
                )
                anchor.make_element()
            else:
                title_value = etree.SubElement(title_element, f"{{{self._ns.gco}}}CharacterString")
                title_value.text = self.element_attributes['title']['value']

        if 'dates' in self.element_attributes:
            for date_attributes in self.element_attributes['dates']:
                date = Date(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=citation_element,
                    element_attributes=date_attributes
                )
                date.make_element()

        if 'edition' in self.element_attributes:
            edition_element = etree.SubElement(citation_element, f"{{{self._ns.gmd}}}edition")
            edition_value = etree.SubElement(edition_element, f"{{{self._ns.gco}}}CharacterString")
            edition_value.text = str(self.element_attributes['edition'])

        if 'identifiers' in self.element_attributes:
            for identifier_attributes in self.element_attributes['identifiers']:
                identifier = Identifier(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=citation_element,
                    element_attributes=identifier_attributes
                )
                identifier.make_element()

        if 'contact' in self.element_attributes:
            citated_responsible_party_element = etree.SubElement(
                citation_element,
                f"{{{self._ns.gmd}}}citedResponsibleParty"
            )
            responsible_party = ResponsibleParty(
                record=self.record,
                attributes=self.attributes,
                parent_element=citated_responsible_party_element,
                element_attributes=self.element_attributes['contact']
            )
            responsible_party.make_element()


class Date(MetadataRecordElement):
    def make_element(self):
        date_container_wrapper = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}date")
        date_container_element = etree.SubElement(date_container_wrapper, f"{{{self._ns.gmd}}}CI_Date")

        date_element = etree.SubElement(date_container_element, f"{{{self._ns.gmd}}}date")
        date_value = etree.SubElement(date_element, f"{{{self._ns.gco}}}DateTime")
        date_value.text = self.element_attributes['date'].isoformat()

        if 'date-precision' in self.element_attributes:
            if self.element_attributes['date-precision'] == 'year':
                date_value.text = str(self.element_attributes['date'].year)
            elif self.element_attributes['date-precision'] == 'month':
                date_parts = [
                    str(self.element_attributes['date'].year),
                    str(self.element_attributes['date'].month)
                ]
                date_value.text = '-'.join(date_parts)

        date_type = DateType(
            record=self.record,
            attributes=self.attributes,
            parent_element=date_container_element,
            element_attributes=self.element_attributes
        )
        date_type.make_element()


class DateType(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'creation',
            'publication',
            'revision',
            'expiry',
            'lastUpdate',
            'lastRevision',
            'nextUpdate',
            'unavailable',
            'inForce',
            'adopted',
            'deprecated',
            'superseded',
            'validityBegins',
            'validityExpires',
            'released',
            'distribution'
        ]
        self.code_list = 'https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_DateTypeCode'
        self.element = f"{{{self._ns.gmd}}}dateType"
        self.element_code = f"{{{self._ns.gmd}}}CI_DateTypeCode"
        self.attribute = 'date-type'


class Identifier(MetadataRecordElement):
    def make_element(self):
        identifier_container = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}identifier")
        identifier_wrapper = etree.SubElement(identifier_container, f"{{{self._ns.gmd}}}MD_Identifier")
        identifier_element = etree.SubElement(identifier_wrapper, f"{{{self._ns.gmd}}}code")

        if 'href' in self.element_attributes:
            anchor = AnchorElement(
                record=self.record,
                attributes=self.attributes,
                parent_element=identifier_element,
                element_attributes=self.element_attributes,
                element_value=self.element_attributes['identifier']
            )
            anchor.make_element()
        else:
            identifier_value = etree.SubElement(identifier_element, f"{{{self._ns.gco}}}CharacterString")
            identifier_value.text = self.element_attributes['identifier']


class AnchorElement(MetadataRecordElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None,
        element_value: str = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.text = element_value

    def make_element(self):
        attributes = {}

        if 'href' in self.element_attributes:
            attributes[f"{{{self._ns.xlink}}}href"] = self.element_attributes['href']
            attributes[f"{{{self._ns.xlink}}}actuate"] = 'onRequest'
        if 'title' in self.element_attributes:
            attributes[f"{{{self._ns.xlink}}}title"] = self.element_attributes['title']

        anchor = etree.SubElement(self.parent_element, f"{{{self._ns.gmx}}}Anchor", attrib=attributes)
        anchor.text = self.text


class DataIdentification(MetadataRecordElement):
    def make_element(self):
        data_identification_wrapper = etree.SubElement(self.record, f"{{{self._ns.gmd}}}identificationInfo")
        data_identification_element = etree.SubElement(
            data_identification_wrapper,
            f"{{{self._ns.gmd}}}MD_DataIdentification"
        )

        citation_wrapper = etree.SubElement(data_identification_element, f"{{{self._ns.gmd}}}citation")
        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=citation_wrapper,
            element_attributes=self.attributes['resource']
        )
        citation.make_element()

        abstract = Abstract(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes['resource']
        )
        abstract.make_element()

        for point_of_contact_attributes in self.attributes['resource']['contacts']:
            if isinstance(point_of_contact_attributes['role'], list):
                for role in point_of_contact_attributes['role']:
                    _point_of_contact = point_of_contact_attributes.copy()
                    _point_of_contact['role'] = role

                    point_of_contact = PointOfContact(
                        record=self.record,
                        attributes=self.attributes,
                        parent_element=data_identification_element,
                        element_attributes=_point_of_contact
                    )
                    point_of_contact.make_element()
            else:
                point_of_contact = PointOfContact(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_identification_element,
                    element_attributes=point_of_contact_attributes
                )
                point_of_contact.make_element()

        resource_maintenance = ResourceMaintenance(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes['resource']
        )
        resource_maintenance.make_element()

        for keyword_attributes in self.attributes['resource']['keywords']:
            descriptive_keywords = DescriptiveKeywords(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes=keyword_attributes
            )
            descriptive_keywords.make_element()

        constraints = ResourceConstraints(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes['resource']
        )
        constraints.make_element()

        supplemental_information = SupplementalInformation(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes['resource']
        )
        supplemental_information.make_element()

        spatial_representation_type = SpatialRepresentationType(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes['resource']
        )
        spatial_representation_type.make_element()

        spatial_resolution = SpatialResolution(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes['resource']
        )
        spatial_resolution.make_element()

        language = Language(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes['resource']
        )
        language.make_element()

        for topic_attribute in self.attributes['resource']['topics']:
            topic = TopicCategory(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_identification_element,
                element_attributes={'topic': topic_attribute}
            )
            topic.make_element()


class Abstract(MetadataRecordElement):
    def make_element(self):
        abstract_element = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}abstract")
        abstract_value = etree.SubElement(abstract_element, f"{{{self._ns.gco}}}CharacterString")
        abstract_value.text = self.element_attributes['abstract']


class PointOfContact(MetadataRecordElement):
    def make_element(self):
        point_of_contact_element = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}pointOfContact")

        responsible_party = ResponsibleParty(
            record=self.record,
            attributes=self.attributes,
            parent_element=point_of_contact_element,
            element_attributes=self.element_attributes
        )
        responsible_party.make_element()


class ResourceMaintenance(MetadataRecordElement):
    def make_element(self):
        resource_maintenance_element = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}resourceMaintenance")
        maintenance_information = MaintenanceInformation(
            record=self.record,
            attributes=self.attributes,
            parent_element=resource_maintenance_element,
            element_attributes=self.attributes['maintenance']
        )
        maintenance_information.make_element()


class DescriptiveKeywords(MetadataRecordElement):
    def make_element(self):
        keywords_wrapper = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}descriptiveKeywords")
        keywords_element = etree.SubElement(keywords_wrapper, f"{{{self._ns.gmd}}}MD_Keywords")

        for term in self.element_attributes['terms']:
            term_element = etree.SubElement(keywords_element, f"{{{self._ns.gmd}}}keyword")
            if 'href' in term:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=term_element,
                    element_attributes=term,
                    element_value=term['title']
                )
                anchor.make_element()
            else:
                term_value = etree.SubElement(term_element, f"{{{self._ns.gco}}}CharacterString")
                term_value.text = term['title']

        keyword_type = DescriptiveKeywordsType(
            record=self.record,
            attributes=self.attributes,
            parent_element=keywords_element,
            element_attributes=self.element_attributes
        )
        keyword_type.make_element()

        if 'thesaurus' in self.element_attributes:
            thesaurus = Thesaurus(
                record=self.record,
                attributes=self.attributes,
                parent_element=keywords_element,
                element_attributes=self.element_attributes['thesaurus']
            )
            thesaurus.make_element()


class DescriptiveKeywordsType(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'discipline',
            'place',
            'stratum',
            'temporal',
            'theme'
        ]
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#MD_KeywordTypeCode'
        self.element = f"{{{self._ns.gmd}}}type"
        self.element_code = f"{{{self._ns.gmd}}}MD_KeywordTypeCode"
        self.attribute = 'type'


class Thesaurus(MetadataRecordElement):
    def make_element(self):
        thesaurus_element = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}thesaurusName")

        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=thesaurus_element,
            element_attributes=self.element_attributes
        )
        citation.make_element()


class ResourceConstraints(MetadataRecordElement):
    uk_ogl_v3_anchor = {
        'href': 'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
        'value': 'This information is licensed under the Open Government Licence v3.0. To view this licence, visit '
                 'http://www.nationalarchives.gov.uk/doc/open-government-licence/'
    }

    def make_element(self):
        if 'access' in self.element_attributes['constraints']:
            for access_constraint_attributes in self.element_attributes['constraints']['access']:
                constraints_wrapper = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}resourceConstraints")
                constraints_element = etree.SubElement(constraints_wrapper, f"{{{self._ns.gmd}}}MD_LegalConstraints")

                access_constraint = AccessConstraint(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=constraints_element,
                    element_attributes=access_constraint_attributes
                )
                access_constraint.make_element()

                if 'inspire-limitations-on-public-access' in access_constraint_attributes:
                    public_access_limitation = InspireLimitationsOnPublicAccess(
                        record=self.record,
                        attributes=self.attributes,
                        parent_element=constraints_element,
                        element_attributes=access_constraint_attributes
                    )
                    public_access_limitation.make_element()

        if 'usage' in self.element_attributes['constraints']:
            for usage_constraint_attributes in self.element_attributes['constraints']['usage']:
                constraints_wrapper = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}resourceConstraints")
                constraints_element = etree.SubElement(constraints_wrapper, f"{{{self._ns.gmd}}}MD_LegalConstraints")

                use_constraint = UseConstraint(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=constraints_element,
                    element_attributes=usage_constraint_attributes
                )
                use_constraint.make_element()

                if 'copyright-licence' in usage_constraint_attributes:
                    if usage_constraint_attributes['copyright-licence'] == 'OGL-UK-3.0':
                        other_constraint_element = etree.SubElement(
                            constraints_element,
                            f"{{{self._ns.gmd}}}otherConstraints"
                        )

                        copyright_statement = AnchorElement(
                            record=self.record,
                            attributes=self.attributes,
                            parent_element=other_constraint_element,
                            element_attributes=self.uk_ogl_v3_anchor,
                            element_value=self.uk_ogl_v3_anchor['value']
                        )
                        copyright_statement.make_element()

                if 'required-citation' in usage_constraint_attributes:
                    other_constraint_element = etree.SubElement(
                        constraints_element,
                        f"{{{self._ns.gmd}}}otherConstraints"
                    )
                    other_constraint_wrapper = etree.SubElement(
                        other_constraint_element,
                        f"{{{self._ns.gco}}}CharacterString"
                    )
                    other_constraint_wrapper.text = f"Cite this information as: " \
                        f"\"{ usage_constraint_attributes['required-citation'] }\""


class AccessConstraint(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'copyright',
            'patent',
            'patentPending',
            'trademark',
            'license',
            'intellectualPropertyRights',
            'restricted',
            'otherRestrictions'
        ]
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#MD_RestrictionCode'
        self.element = f"{{{self._ns.gmd}}}accessConstraints"
        self.element_code = f"{{{self._ns.gmd}}}MD_RestrictionCode"
        self.attribute = 'restriction-code'


class UseConstraint(AccessConstraint):

    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.element = f"{{{self._ns.gmd}}}useConstraints"


class InspireLimitationsOnPublicAccess(MetadataRecordElement):
    def make_element(self):
        other_constraints_element = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}otherConstraints")

        other_constraints_value = AnchorElement(
            record=self.record,
            attributes=self.attributes,
            parent_element=other_constraints_element,
            element_attributes={
                'href': f"http://inspire.ec.europa.eu/metadata-codelist/LimitationsOnPublicAccess/"
                f"{ self.element_attributes['inspire-limitations-on-public-access'] }"
            },
            element_value=self.element_attributes['inspire-limitations-on-public-access']
        )
        other_constraints_value.make_element()


class SupplementalInformation(MetadataRecordElement):
    def make_element(self):
        supplemental_info_element = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}supplementalInformation")
        supplemental_info_value = etree.SubElement(supplemental_info_element, f"{{{self._ns.gco}}}CharacterString")
        supplemental_info_value.text = self.element_attributes['supplemental-information']


class SpatialRepresentationType(CodeListElement):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        super().__init__(
            record=record,
            attributes=attributes,
            parent_element=parent_element,
            element_attributes=element_attributes
        )
        self.code_list_values = [
            'vector',
            'grid',
            'textTable',
            'tin',
            'stereoModel',
            'video'
        ]
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#MD_SpatialRepresentationTypeCode'
        self.element = f"{{{self._ns.gmd}}}spatialRepresentationType"
        self.element_code = f"{{{self._ns.gmd}}}MD_SpatialRepresentationTypeCode"
        self.attribute = 'spatial-representation-type'


class SpatialResolution(MetadataRecordElement):
    def make_element(self):
        resolution_wrapper = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}spatialResolution")
        resolution_element = etree.SubElement(resolution_wrapper, f"{{{self._ns.gmd}}}MD_Resolution")
        etree.SubElement(
            resolution_element,
            f"{{{self._ns.gmd}}}distance",
            attrib={f"{{{self._ns.gco}}}nilReason": 'inapplicable'}
        )


class TopicCategory(MetadataRecordElement):
    def make_element(self):
        topic_element = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}topicCategory")
        topic_value = etree.SubElement(topic_element, f"{{{self._ns.gmd}}}MD_TopicCategoryCode")
        topic_value.text = self.element_attributes['topic']


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        attributes = config.test_record
        record = MetadataRecord(**attributes)
        document = etree.ElementTree(record.record)
        document_str = etree.tostring(document, pretty_print=True, xml_declaration=True, encoding="utf-8")
        return Response(document_str, mimetype='text/xml')

    return app
