from datetime import datetime, date
from typing import Optional, Union

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
            schema_locations = f"{schema_locations} {self._namespaces[prefix]} {location}"

        return schema_locations.lstrip()


class Utils(object):
    @staticmethod
    def get_epsg_code(candidate_code: str) -> Optional[str]:
        if candidate_code.startswith('urn:ogc:def:crs:EPSG'):
            code_parts = candidate_code.split(':')
            return code_parts[-1]

        return None

    @staticmethod
    def format_date_string(date_datetime: Union[date, datetime]) -> str:
        return date_datetime.isoformat()


class MetadataRecord(object):
    def __init__(self, **kwargs):
        self.ns = Namespaces()
        self.attributes = kwargs
        self.record = self.make_element()

    def make_element(self):
        metadata_record = etree.Element(
            f"{{{self.ns.gmd}}}MD_Metadata",
            attrib={f"{{{ self.ns.xsi }}}schemaLocation": self.ns.schema_locations()},
            nsmap=self.ns.nsmap()
        )

        identifier = FileIdentifier(
            record=metadata_record,
            attributes=self.attributes
        )
        identifier.make_element()

        language = Language(
            record=metadata_record,
            attributes=self.attributes
        )
        language.make_element()

        character_set = CharacterSet(
            record=metadata_record,
            attributes=self.attributes
        )
        character_set.make_element()

        hierarchy_level = HierarchyLevel(
            record=metadata_record,
            attributes=self.attributes
        )
        hierarchy_level.make_element()

        contact = Contact(
            record=metadata_record,
            attributes=self.attributes
        )
        contact.make_element()

        date_stamp = DateStamp(
            record=metadata_record,
            attributes=self.attributes
        )
        date_stamp.make_element()

        metadata_maintenance = MetadataMaintenance(
            record=metadata_record,
            attributes=self.attributes
        )
        metadata_maintenance.make_element()

        metadata_standard = MetadataStandard(
            record=metadata_record,
            attributes=self.attributes
        )
        metadata_standard.make_element()

        reference_system_identifier = ReferenceSystemInfo(
            record=metadata_record,
            attributes=self.attributes
        )
        reference_system_identifier.make_element()

        data_identification = DataIdentification(
            record=metadata_record,
            attributes=self.attributes
        )
        data_identification.make_element()

        data_distribution = DataDistribution(
            record=metadata_record,
            attributes=self.attributes
        )
        data_distribution.make_element()

        data_quality = DataQuality(
            record=metadata_record,
            attributes=self.attributes
        )
        data_quality.make_element()

        return metadata_record


class MetadataRecordElement(object):
    def __init__(
        self,
        record: MetadataRecord,
        attributes: dict,
        parent_element: Element = None,
        element_attributes: dict = None
    ):
        self.ns = Namespaces()
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


class FileIdentifier(MetadataRecordElement):
    def make_element(self):
        file_identifier = etree.SubElement(self.record, f"{{{self.ns.gmd}}}fileIdentifier")

        if 'file-identifier' in self.attributes:
            file_identifier_val = etree.SubElement(file_identifier, f"{{{self.ns.gco}}}CharacterString")
            file_identifier_val.text = self.attributes['file-identifier']


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
        self.element = f"{{{self.ns.gmd}}}language"
        self.element_code = f"{{{self.ns.gmd}}}LanguageCode"
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
        self.element = f"{{{self.ns.gmd}}}characterSet"
        self.element_code = f"{{{self.ns.gmd}}}MD_CharacterSetCode"
        self.attribute = 'character-set'


class ScopeCode(CodeListElement):
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
        self.element = f"{{{self.ns.gmd}}}level"
        self.element_code = f"{{{self.ns.gmd}}}MD_ScopeCode"
        self.attribute = 'hierarchy-level'


class HierarchyLevel(ScopeCode):
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
        self.element = f"{{{self.ns.gmd}}}hierarchyLevel"

    def make_element(self):
        super().make_element()
        hierarchy_level_name_element = etree.SubElement(self.record, f"{{{self.ns.gmd}}}hierarchyLevelName")
        if self.attribute in self.attributes and self.attributes[self.attribute] in self.code_list_values:
            hierarchy_level_name_value = etree.SubElement(
                hierarchy_level_name_element,
                f"{{{self.ns.gco}}}CharacterString"
            )
            hierarchy_level_name_value.text = self.attributes[self.attribute]


class Contact(MetadataRecordElement):
    def make_element(self):
        contact_element = etree.SubElement(self.record, f"{{{self.ns.gmd}}}contact")

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
        responsible_party_element = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}CI_ResponsibleParty")

        if 'individual' in self.element_attributes and 'name' in self.element_attributes['individual']:
            individual_element = etree.SubElement(responsible_party_element, f"{{{self.ns.gmd}}}individualName")
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
                individual_value = etree.SubElement(individual_element, f"{{{self.ns.gco}}}CharacterString")
                individual_value.text = self.element_attributes['individual']['name']

        if 'organisation' in self.element_attributes and 'name' in self.element_attributes['organisation']:
            organisation_element = etree.SubElement(responsible_party_element, f"{{{self.ns.gmd}}}organisationName")
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
                organisation_name_value = etree.SubElement(organisation_element, f"{{{self.ns.gco}}}CharacterString")
                organisation_name_value.text = self.element_attributes['organisation']['name']

        contact_wrapper = etree.SubElement(responsible_party_element, f"{{{self.ns.gmd}}}contactInfo")
        contact_element = etree.SubElement(contact_wrapper, f"{{{self.ns.gmd}}}CI_Contact")

        if 'phone' in self.element_attributes:
            phone_wrapper = etree.SubElement(contact_element, f"{{{self.ns.gmd}}}phone")
            phone_element = etree.SubElement(phone_wrapper, f"{{{self.ns.gmd}}}CI_Telephone")
            phone_voice = etree.SubElement(phone_element, f"{{{self.ns.gmd}}}voice")
            phone_voice_value = etree.SubElement(phone_voice, f"{{{self.ns.gco}}}CharacterString")
            phone_voice_value.text = self.element_attributes['phone']

        address_wrapper = etree.SubElement(contact_element, f"{{{self.ns.gmd}}}address")
        address_element = etree.SubElement(address_wrapper, f"{{{self.ns.gmd}}}CI_Address")

        if 'address' in self.element_attributes:
            if 'delivery-point' in self.element_attributes['address']:
                delivery_point_element = etree.SubElement(address_element, f"{{{self.ns.gmd}}}deliveryPoint")
                delivery_point_value = etree.SubElement(
                    delivery_point_element,
                    f"{{{self.ns.gco}}}CharacterString"
                )
                delivery_point_value.text = self.element_attributes['address']['delivery-point']
            if 'city' in self.element_attributes['address']:
                city_element = etree.SubElement(address_element, f"{{{self.ns.gmd}}}city")
                city_value = etree.SubElement(city_element, f"{{{self.ns.gco}}}CharacterString")
                city_value.text = self.element_attributes['address']['city']
            if 'administrative-area' in self.element_attributes['address']:
                administrative_area_element = etree.SubElement(
                    address_element,
                    f"{{{self.ns.gmd}}}administrativeArea"
                )
                administrative_area_value = etree.SubElement(
                    administrative_area_element,
                    f"{{{self.ns.gco}}}CharacterString"
                )
                administrative_area_value.text = self.element_attributes['address']['administrative-area']
            if 'postal-code' in self.element_attributes['address']:
                postal_code_element = etree.SubElement(address_element, f"{{{self.ns.gmd}}}postalCode")
                postal_code_value = etree.SubElement(postal_code_element, f"{{{self.ns.gco}}}CharacterString")
                postal_code_value.text = self.element_attributes['address']['postal-code']
            if 'country' in self.element_attributes['address']:
                country_element = etree.SubElement(address_element, f"{{{self.ns.gmd}}}country")
                country_value = etree.SubElement(country_element, f"{{{self.ns.gco}}}CharacterString")
                country_value.text = self.element_attributes['address']['country']

        if 'email' in self.element_attributes:
            email_element = etree.SubElement(address_element, f"{{{self.ns.gmd}}}electronicMailAddress")
            email_value = etree.SubElement(email_element, f"{{{self.ns.gco}}}CharacterString")
            email_value.text = self.element_attributes['email']
        else:
            etree.SubElement(
                address_element,
                f"{{{self.ns.gmd}}}electronicMailAddress",
                attrib={f"{{{self.ns.gco}}}nilReason": 'unknown'}
            )

        if 'online-resource' in self.element_attributes:
            online_resource_wrapper = etree.SubElement(responsible_party_element, f"{{{self.ns.gmd}}}onlineResource")
            online_resource = OnlineResource(
                record=self.record,
                attributes=self.attributes,
                parent_element=online_resource_wrapper,
                element_attributes=self.element_attributes['online-resource']
            )
            online_resource.make_element()

        if 'role' in self.element_attributes:
            role = Role(
                record=self.record,
                attributes=self.attributes,
                parent_element=responsible_party_element,
                element_attributes=self.element_attributes
            )
            role.make_element()


class OnlineResource(MetadataRecordElement):
    def make_element(self):
        online_resource_element = etree.SubElement(
            self.parent_element,
            f"{{{self.ns.gmd}}}CI_OnlineResource"
        )

        if 'href' in self.element_attributes:
            linkage = Linkage(
                record=self.record,
                attributes=self.attributes,
                parent_element=online_resource_element,
                element_attributes=self.element_attributes
            )
            linkage.make_element()

        if 'title' in self.element_attributes:
            title_wrapper = etree.SubElement(online_resource_element, f"{{{self.ns.gmd}}}name")
            title_element = etree.SubElement(title_wrapper, f"{{{self.ns.gco}}}CharacterString")
            title_element.text = self.element_attributes['title']

        if 'description' in self.element_attributes:
            title_wrapper = etree.SubElement(online_resource_element, f"{{{self.ns.gmd}}}description")
            title_element = etree.SubElement(title_wrapper, f"{{{self.ns.gco}}}CharacterString")
            title_element.text = self.element_attributes['description']

        if 'function' in self.element_attributes:
            function = OnlineRole(
                record=self.record,
                attributes=self.attributes,
                parent_element=online_resource_element,
                element_attributes=self.element_attributes
            )
            function.make_element()


class Linkage(MetadataRecordElement):
    def make_element(self):
        linkage_element = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}linkage")
        if 'href' in self.element_attributes:
            url_value = etree.SubElement(linkage_element, f"{{{self.ns.gmd}}}URL")
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
        self.element = f"{{{self.ns.gmd}}}role"
        self.element_code = f"{{{self.ns.gmd}}}CI_RoleCode"
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
        self.element = f"{{{self.ns.gmd}}}function"
        self.element_code = f"{{{self.ns.gmd}}}CI_OnLineFunctionCode"
        self.attribute = 'function'


class DateStamp(MetadataRecordElement):
    def make_element(self):
        date_stamp_element = etree.SubElement(self.record, f"{{{self.ns.gmd}}}dateStamp")
        date_stamp_value = etree.SubElement(date_stamp_element, f"{{{self.ns.gco}}}DateTime")
        date_stamp_value.text = Utils.format_date_string(self.attributes['date-stamp'])


class MetadataMaintenance(MetadataRecordElement):
    def make_element(self):
        metadata_maintenance_element = etree.SubElement(self.record, f"{{{self.ns.gmd}}}metadataMaintenance")
        maintenance_information = MaintenanceInformation(
            record=self.record,
            attributes=self.attributes,
            parent_element=metadata_maintenance_element,
            element_attributes=self.attributes['maintenance']
        )
        maintenance_information.make_element()


class MaintenanceInformation(MetadataRecordElement):
    def make_element(self):
        maintenance_element = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}MD_MaintenanceInformation")

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
        self.element = f"{{{self.ns.gmd}}}maintenanceAndUpdateFrequency"
        self.element_code = f"{{{self.ns.gmd}}}MD_MaintenanceFrequencyCode"
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
        self.element = f"{{{self.ns.gmd}}}maintenanceNote"
        self.element_code = f"{{{self.ns.gmd}}}MD_ProgressCode"
        self.attribute = 'progress'


class MetadataStandard(MetadataRecordElement):
    def make_element(self):
        if 'name' in self.attributes['metadata-standard']:
            metadata_standard_name_element = etree.SubElement(self.record, f"{{{self.ns.gmd}}}metadataStandardName")
            metadata_standard_name_value = etree.SubElement(
                metadata_standard_name_element,
                f"{{{self.ns.gco}}}CharacterString"
            )
            metadata_standard_name_value.text = self.attributes['metadata-standard']['name']
        if 'version' in self.attributes['metadata-standard']:
            metadata_standard_version_element = etree.SubElement(
                self.record,
                f"{{{self.ns.gmd}}}metadataStandardVersion"
            )
            metadata_standard_version_value = etree.SubElement(
                metadata_standard_version_element,
                f"{{{self.ns.gco}}}CharacterString"
            )
            metadata_standard_version_value.text = self.attributes['metadata-standard']['version']


class ReferenceSystemInfo(MetadataRecordElement):
    def make_element(self):
        reference_system_wrapper = etree.SubElement(self.record, f"{{{self.ns.gmd}}}referenceSystemInfo")
        reference_system_element = etree.SubElement(reference_system_wrapper, f"{{{self.ns.gmd}}}MD_ReferenceSystem")
        reference_system_identifier_wrapper = etree.SubElement(
            reference_system_element,
            f"{{{self.ns.gmd}}}referenceSystemIdentifier"
        )
        reference_system_identifier_element = etree.SubElement(
            reference_system_identifier_wrapper,
            f"{{{self.ns.gmd}}}RS_Identifier"
        )

        if 'authority' in self.attributes['reference-system-info']:
            reference_system_identifier_authority_element = etree.SubElement(
                reference_system_identifier_element,
                f"{{{self.ns.gmd}}}authority"
            )
            citation = Citation(
                record=self.record,
                attributes=self.attributes,
                parent_element=reference_system_identifier_authority_element,
                element_attributes=self.attributes['reference-system-info']['authority']
            )
            citation.make_element()

        if 'code' in self.attributes['reference-system-info']:
            reference_system_identifier_code_element = etree.SubElement(
                reference_system_identifier_element,
                f"{{{self.ns.gmd}}}code"
            )
            if 'href' in self.attributes['reference-system-info']['code']:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=reference_system_identifier_code_element,
                    element_attributes=self.attributes['reference-system-info']['code'],
                    element_value=self.attributes['reference-system-info']['code']['value']
                )
                anchor.make_element()
            else:
                reference_system_identifier_code_value = etree.SubElement(
                    reference_system_identifier_code_element,
                    f"{{{self.ns.gco}}}CharacterString"
                )
                reference_system_identifier_code_value.text = self.attributes['reference-system-info']['code']['value']

        if 'version' in self.attributes['reference-system-info']:
            reference_system_identifier_version_element = etree.SubElement(
                reference_system_identifier_element,
                f"{{{self.ns.gmd}}}version"
            )
            reference_system_identifier_version_value = etree.SubElement(
                reference_system_identifier_version_element,
                f"{{{self.ns.gco}}}CharacterString"
            )
            reference_system_identifier_version_value.text = self.attributes['reference-system-info']['version']


class Citation(MetadataRecordElement):
    def make_element(self):
        citation_element = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}CI_Citation")

        if 'title' in self.element_attributes:
            title_element = etree.SubElement(citation_element, f"{{{self.ns.gmd}}}title")
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
                title_value = etree.SubElement(title_element, f"{{{self.ns.gco}}}CharacterString")
                title_value.text = self.element_attributes['title']['value']

        if 'dates' in self.element_attributes:
            for date_attributes in self.element_attributes['dates']:
                citation_date = Date(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=citation_element,
                    element_attributes=date_attributes
                )
                citation_date.make_element()

        if 'edition' in self.element_attributes:
            edition_element = etree.SubElement(citation_element, f"{{{self.ns.gmd}}}edition")
            edition_value = etree.SubElement(edition_element, f"{{{self.ns.gco}}}CharacterString")
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
                f"{{{self.ns.gmd}}}citedResponsibleParty"
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
        date_container_wrapper = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}date")
        date_container_element = etree.SubElement(date_container_wrapper, f"{{{self.ns.gmd}}}CI_Date")

        date_element = etree.SubElement(date_container_element, f"{{{self.ns.gmd}}}date")

        date_value_element = f"{{{self.ns.gco}}}Date"
        if isinstance(self.element_attributes['date'], datetime):
            date_value_element = f"{{{self.ns.gco}}}DateTime"

        date_value = etree.SubElement(date_element, date_value_element)
        date_value.text = Utils.format_date_string(self.element_attributes['date'])

        if 'date-precision' in self.element_attributes:
            if self.element_attributes['date-precision'] == 'year':
                date_value.text = str(self.element_attributes['date'].year)

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
        self.element = f"{{{self.ns.gmd}}}dateType"
        self.element_code = f"{{{self.ns.gmd}}}CI_DateTypeCode"
        self.attribute = 'date-type'


class Identifier(MetadataRecordElement):
    def make_element(self):
        identifier_container = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}identifier")
        identifier_wrapper = etree.SubElement(identifier_container, f"{{{self.ns.gmd}}}MD_Identifier")
        identifier_element = etree.SubElement(identifier_wrapper, f"{{{self.ns.gmd}}}code")

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
            identifier_value = etree.SubElement(identifier_element, f"{{{self.ns.gco}}}CharacterString")
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
            attributes[f"{{{self.ns.xlink}}}href"] = self.element_attributes['href']
            attributes[f"{{{self.ns.xlink}}}actuate"] = 'onRequest'
        if 'title' in self.element_attributes:
            attributes[f"{{{self.ns.xlink}}}title"] = self.element_attributes['title']

        anchor = etree.SubElement(self.parent_element, f"{{{self.ns.gmx}}}Anchor", attrib=attributes)
        anchor.text = self.text


class DataIdentification(MetadataRecordElement):
    def make_element(self):
        data_identification_wrapper = etree.SubElement(self.record, f"{{{self.ns.gmd}}}identificationInfo")
        data_identification_element = etree.SubElement(
            data_identification_wrapper,
            f"{{{self.ns.gmd}}}MD_DataIdentification"
        )

        citation_wrapper = etree.SubElement(data_identification_element, f"{{{self.ns.gmd}}}citation")
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
                    if role != 'distributor':
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

        extent = Extent(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_identification_element,
            element_attributes=self.attributes['resource']
        )
        extent.make_element()


class Abstract(MetadataRecordElement):
    def make_element(self):
        abstract_element = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}abstract")
        abstract_value = etree.SubElement(abstract_element, f"{{{self.ns.gco}}}CharacterString")
        abstract_value.text = self.element_attributes['abstract']


class PointOfContact(MetadataRecordElement):
    def make_element(self):
        point_of_contact_element = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}pointOfContact")

        responsible_party = ResponsibleParty(
            record=self.record,
            attributes=self.attributes,
            parent_element=point_of_contact_element,
            element_attributes=self.element_attributes
        )
        responsible_party.make_element()


class ResourceMaintenance(MetadataRecordElement):
    def make_element(self):
        resource_maintenance_element = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}resourceMaintenance")
        maintenance_information = MaintenanceInformation(
            record=self.record,
            attributes=self.attributes,
            parent_element=resource_maintenance_element,
            element_attributes=self.attributes['maintenance']
        )
        maintenance_information.make_element()


class DescriptiveKeywords(MetadataRecordElement):
    def make_element(self):
        keywords_wrapper = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}descriptiveKeywords")
        keywords_element = etree.SubElement(keywords_wrapper, f"{{{self.ns.gmd}}}MD_Keywords")

        for term in self.element_attributes['terms']:
            term_element = etree.SubElement(keywords_element, f"{{{self.ns.gmd}}}keyword")
            if 'href' in term:
                anchor = AnchorElement(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=term_element,
                    element_attributes=term,
                    element_value=term['term']
                )
                anchor.make_element()
            else:
                term_value = etree.SubElement(term_element, f"{{{self.ns.gco}}}CharacterString")
                term_value.text = term['term']

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
        self.element = f"{{{self.ns.gmd}}}type"
        self.element_code = f"{{{self.ns.gmd}}}MD_KeywordTypeCode"
        self.attribute = 'type'


class Thesaurus(MetadataRecordElement):
    def make_element(self):
        thesaurus_element = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}thesaurusName")

        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=thesaurus_element,
            element_attributes=self.element_attributes
        )
        citation.make_element()


class ResourceConstraints(MetadataRecordElement):
    def make_element(self):
        if 'access' in self.element_attributes['constraints']:
            for access_constraint_attributes in self.element_attributes['constraints']['access']:
                constraints_wrapper = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}resourceConstraints")
                constraints_element = etree.SubElement(constraints_wrapper, f"{{{self.ns.gmd}}}MD_LegalConstraints")

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
                constraints_wrapper = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}resourceConstraints")
                constraints_element = etree.SubElement(constraints_wrapper, f"{{{self.ns.gmd}}}MD_LegalConstraints")

                use_constraint = UseConstraint(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=constraints_element,
                    element_attributes=usage_constraint_attributes
                )
                use_constraint.make_element()

                if 'copyright-licence' in usage_constraint_attributes:
                    other_constraint_element = etree.SubElement(
                        constraints_element,
                        f"{{{self.ns.gmd}}}otherConstraints"
                    )

                    if 'href' in usage_constraint_attributes['copyright-licence']:
                        copyright_statement = AnchorElement(
                            record=self.record,
                            attributes=self.attributes,
                            parent_element=other_constraint_element,
                            element_attributes=usage_constraint_attributes['copyright-licence'],
                            element_value=usage_constraint_attributes['copyright-licence']['statement']
                        )
                        copyright_statement.make_element()
                    else:
                        copyright_statement = etree.SubElement(
                            other_constraint_element,
                            f"{{{self.ns.gco}}}CharacterString"
                        )
                        copyright_statement.text = usage_constraint_attributes['copyright-licence']['statement']

                if 'required-citation' in usage_constraint_attributes:
                    other_constraint_element = etree.SubElement(
                        constraints_element,
                        f"{{{self.ns.gmd}}}otherConstraints"
                    )
                    other_constraint_wrapper = etree.SubElement(
                        other_constraint_element,
                        f"{{{self.ns.gco}}}CharacterString"
                    )
                    other_constraint_wrapper.text = f"Cite this information as: " \
                        f"\"{usage_constraint_attributes['required-citation']}\""


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
        self.element = f"{{{self.ns.gmd}}}accessConstraints"
        self.element_code = f"{{{self.ns.gmd}}}MD_RestrictionCode"
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
        self.element = f"{{{self.ns.gmd}}}useConstraints"


class InspireLimitationsOnPublicAccess(MetadataRecordElement):
    def make_element(self):
        other_constraints_element = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}otherConstraints")

        other_constraints_value = AnchorElement(
            record=self.record,
            attributes=self.attributes,
            parent_element=other_constraints_element,
            element_attributes={
                'href': f"http://inspire.ec.europa.eu/metadata-codelist/LimitationsOnPublicAccess/"
                f"{self.element_attributes['inspire-limitations-on-public-access']}"
            },
            element_value=self.element_attributes['inspire-limitations-on-public-access']
        )
        other_constraints_value.make_element()


class SupplementalInformation(MetadataRecordElement):
    def make_element(self):
        supplemental_info_element = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}supplementalInformation")
        supplemental_info_value = etree.SubElement(supplemental_info_element, f"{{{self.ns.gco}}}CharacterString")
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
        self.element = f"{{{self.ns.gmd}}}spatialRepresentationType"
        self.element_code = f"{{{self.ns.gmd}}}MD_SpatialRepresentationTypeCode"
        self.attribute = 'spatial-representation-type'


class SpatialResolution(MetadataRecordElement):
    def make_element(self):
        resolution_wrapper = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}spatialResolution")
        resolution_element = etree.SubElement(resolution_wrapper, f"{{{self.ns.gmd}}}MD_Resolution")
        etree.SubElement(
            resolution_element,
            f"{{{self.ns.gmd}}}distance",
            attrib={f"{{{self.ns.gco}}}nilReason": 'inapplicable'}
        )


class TopicCategory(MetadataRecordElement):
    def make_element(self):
        topic_element = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}topicCategory")
        topic_value = etree.SubElement(topic_element, f"{{{self.ns.gmd}}}MD_TopicCategoryCode")
        topic_value.text = self.element_attributes['topic']


class Extent(MetadataRecordElement):
    def make_element(self):
        extent_wrapper = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}extent")
        extent_element = etree.SubElement(extent_wrapper, f"{{{self.ns.gmd}}}EX_Extent")

        if 'geographic' in self.element_attributes['extent']:
            geographic_extent = GeographicExtent(
                record=self.record,
                attributes=self.attributes,
                parent_element=extent_element,
                element_attributes=self.element_attributes['extent']['geographic']
            )
            geographic_extent.make_element()

        if 'vertical' in self.element_attributes['extent']:
            vertical_extent = VerticalExtent(
                record=self.record,
                attributes=self.attributes,
                parent_element=extent_element,
                element_attributes=self.element_attributes['extent']['vertical']
            )
            vertical_extent.make_element()

        if 'temporal' in self.element_attributes['extent']:
            temporal_extent = TemporalExtent(
                record=self.record,
                attributes=self.attributes,
                parent_element=extent_element,
                element_attributes=self.element_attributes['extent']['temporal']
            )
            temporal_extent.make_element()


class GeographicExtent(MetadataRecordElement):
    def make_element(self):
        geographic_extent_element = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}geographicElement")

        if 'bounding-box' in self.element_attributes:
            bounding_box = BoundingBox(
                record=self.record,
                attributes=self.attributes,
                parent_element=geographic_extent_element,
                element_attributes=self.element_attributes['bounding-box']
            )
            bounding_box.make_element()


class BoundingBox(MetadataRecordElement):
    def make_element(self):
        bounding_box_element = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}EX_GeographicBoundingBox")

        west_element = etree.SubElement(bounding_box_element, f"{{{self.ns.gmd}}}westBoundLongitude")
        west_value = etree.SubElement(west_element, f"{{{self.ns.gco}}}Decimal")
        west_value.text = str(self.element_attributes['west-longitude'])

        east_element = etree.SubElement(bounding_box_element, f"{{{self.ns.gmd}}}eastBoundLongitude")
        east_value = etree.SubElement(east_element, f"{{{self.ns.gco}}}Decimal")
        east_value.text = str(self.element_attributes['east-longitude'])

        south_element = etree.SubElement(bounding_box_element, f"{{{self.ns.gmd}}}southBoundLatitude")
        south_value = etree.SubElement(south_element, f"{{{self.ns.gco}}}Decimal")
        south_value.text = str(self.element_attributes['south-latitude'])

        north_element = etree.SubElement(bounding_box_element, f"{{{self.ns.gmd}}}northBoundLatitude")
        north_value = etree.SubElement(north_element, f"{{{self.ns.gco}}}Decimal")
        north_value.text = str(self.element_attributes['north-latitude'])


class VerticalExtent(MetadataRecordElement):
    def make_element(self):
        vertical_extent_wrapper = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}verticalElement")
        vertical_extent_element = etree.SubElement(vertical_extent_wrapper, f"{{{self.ns.gmd}}}EX_VerticalExtent")

        if 'minimum' in self.element_attributes:
            minimum_element = etree.SubElement(vertical_extent_element, f"{{{self.ns.gmd}}}minimumValue")
            minimum_value = etree.SubElement(minimum_element, f"{{{self.ns.gco}}}Real")
            minimum_value.text = self.element_attributes['minimum']
        else:
            etree.SubElement(
                vertical_extent_element,
                f"{{{self.ns.gmd}}}minimumValue",
                attrib={f"{{{self.ns.gco}}}nilReason": 'unknown'}
            )

        if 'maximum' in self.element_attributes:
            maximum_element = etree.SubElement(vertical_extent_element, f"{{{self.ns.gmd}}}maximumValue")
            maximum_value = etree.SubElement(maximum_element, f"{{{self.ns.gco}}}Real")
            maximum_value.text = self.element_attributes['maximum']
        else:
            etree.SubElement(
                vertical_extent_element,
                f"{{{self.ns.gmd}}}maximumValue",
                attrib={f"{{{self.ns.gco}}}nilReason": 'unknown'}
            )

        if 'code' in self.element_attributes:
            vertical_crs = VerticalCRS(
                record=self.record,
                attributes=self.attributes,
                parent_element=vertical_extent_element,
                element_attributes=self.element_attributes
            )
            vertical_crs.make_element()


class VerticalCRS(MetadataRecordElement):
    def make_element(self):
        vertical_crs_wrapper = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}verticalCRS")
        vertical_crs_element = etree.SubElement(
            vertical_crs_wrapper,
            f"{{{self.ns.gml}}}VerticalCRS",
            attrib={f"{{{self.ns.gml}}}id": self.element_attributes['identifier']}
        )
        vertical_crs_code = etree.SubElement(
            vertical_crs_element,
            f"{{{self.ns.gml}}}identifier",
            attrib={'codeSpace': 'OGP'}
        )
        vertical_crs_code.text = self.element_attributes['code']

        name = etree.SubElement(vertical_crs_element, f"{{{self.ns.gml}}}name")
        name.text = self.element_attributes['name']

        remarks = etree.SubElement(vertical_crs_element, f"{{{self.ns.gml}}}remarks")
        remarks.text = self.element_attributes['remarks']

        etree.SubElement(
            vertical_crs_element,
            f"{{{self.ns.gml}}}domainOfValidity",
            attrib={
                f"{{{self.ns.xlink}}}href": self.element_attributes['domain-of-validity']['href']
            }
        )

        scope = etree.SubElement(vertical_crs_element, f"{{{self.ns.gml}}}scope")
        scope.text = self.element_attributes['scope']

        etree.SubElement(
            vertical_crs_element,
            f"{{{self.ns.gml}}}verticalCS",
            attrib={
                f"{{{self.ns.xlink}}}href": self.element_attributes['vertical-cs']['href']
            }
        )

        etree.SubElement(
            vertical_crs_element,
            f"{{{self.ns.gml}}}verticalDatum",
            attrib={
                f"{{{self.ns.xlink}}}href": self.element_attributes['vertical-datum']['href']
            }
        )


class TemporalExtent(MetadataRecordElement):
    def make_element(self):
        temporal_extent_container = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}temporalElement")
        temporal_extent_wrapper = etree.SubElement(temporal_extent_container, f"{{{self.ns.gmd}}}EX_TemporalExtent")
        temporal_extent_element = etree.SubElement(temporal_extent_wrapper, f"{{{self.ns.gmd}}}extent")

        if 'period' in self.element_attributes:
            time_period_element = etree.SubElement(
                temporal_extent_element,
                f"{{{self.ns.gml}}}TimePeriod",
                attrib={f"{{{self.ns.gml}}}id": 'boundingExtent'}
            )
            begin_position_element = etree.SubElement(time_period_element, f"{{{self.ns.gml}}}beginPosition")
            begin_position_element.text = Utils.format_date_string(self.element_attributes['period']['start'])

            end_position_element = etree.SubElement(time_period_element, f"{{{self.ns.gml}}}endPosition")
            end_position_element.text = Utils.format_date_string(self.element_attributes['period']['end'])


class DataDistribution(MetadataRecordElement):
    def make_element(self):
        data_distribution_wrapper = etree.SubElement(self.record, f"{{{self.ns.gmd}}}distributionInfo")
        data_distribution_element = etree.SubElement(data_distribution_wrapper, f"{{{self.ns.gmd}}}MD_Distribution")

        for format_attributes in self.attributes['resource']['formats']:
            distribution_format = DistributionFormat(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_distribution_element,
                element_attributes=format_attributes
            )
            distribution_format.make_element()

        for point_of_contact_attributes in self.attributes['resource']['contacts']:
            if isinstance(point_of_contact_attributes['role'], list):
                for role in point_of_contact_attributes['role']:
                    if role == 'distributor':
                        _point_of_contact = point_of_contact_attributes.copy()
                        _point_of_contact['role'] = role

                        distributor = Distributor(
                            record=self.record,
                            attributes=self.attributes,
                            parent_element=data_distribution_element,
                            element_attributes=_point_of_contact
                        )
                        distributor.make_element()
            elif point_of_contact_attributes['role'] == 'distributor':
                distributor = Distributor(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=data_distribution_element,
                    element_attributes=point_of_contact_attributes
                )
                distributor.make_element()

        for transfer_attributes in self.attributes['resource']['transfer-options']:
            transfer_options = TransformOptions(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_distribution_element,
                element_attributes=transfer_attributes
            )
            transfer_options.make_element()


class DistributionFormat(MetadataRecordElement):
    def make_element(self):
        distribution_format_wrapper = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}distributionFormat")
        distribution_format_element = etree.SubElement(distribution_format_wrapper, f"{{{self.ns.gmd}}}MD_Format")

        format_name_element = etree.SubElement(distribution_format_element, f"{{{self.ns.gmd}}}name")
        if 'href' in self.element_attributes:
            anchor = AnchorElement(
                record=self.record,
                attributes=self.attributes,
                parent_element=format_name_element,
                element_attributes=self.element_attributes,
                element_value=self.element_attributes['format']
            )
            anchor.make_element()
        else:
            format_name_value = etree.SubElement(format_name_element, f"{{{self.ns.gco}}}CharacterString")
            format_name_value.text = self.element_attributes['format']

        if 'version' in self.element_attributes:
            format_version_element = etree.SubElement(distribution_format_element, f"{{{self.ns.gmd}}}version")
            format_version_value = etree.SubElement(format_version_element, f"{{{self.ns.gco}}}CharacterString")
            format_version_value.text = self.element_attributes['version']
        else:
            etree.SubElement(
                distribution_format_element,
                f"{{{self.ns.gmd}}}version",
                attrib={f"{{{self.ns.gco}}}nilReason": 'unknown'}
            )


class Distributor(MetadataRecordElement):
    def make_element(self):
        distributor_container = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}distributor")
        distributor_wrapper = etree.SubElement(distributor_container, f"{{{self.ns.gmd}}}MD_Distributor")
        distributor_element = etree.SubElement(distributor_wrapper, f"{{{self.ns.gmd}}}distributorContact")

        responsible_party = ResponsibleParty(
            record=self.record,
            attributes=self.attributes,
            parent_element=distributor_element,
            element_attributes=self.element_attributes
        )
        responsible_party.make_element()


class TransformOptions(MetadataRecordElement):
    def make_element(self):
        transfer_options_container = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}transferOptions")
        transfer_options_wrapper = etree.SubElement(
            transfer_options_container,
            f"{{{self.ns.gmd}}}MD_DigitalTransferOptions"
        )
        transfer_options_element = etree.SubElement(transfer_options_wrapper, f"{{{self.ns.gmd}}}onLine")

        online_resource = OnlineResource(
            record=self.record,
            attributes=self.attributes,
            parent_element=transfer_options_element,
            element_attributes=self.element_attributes['online-resource']
        )
        online_resource.make_element()


class DataQuality(MetadataRecordElement):
    def make_element(self):
        data_quality_wrapper = etree.SubElement(self.record, f"{{{self.ns.gmd}}}dataQualityInfo")
        data_quality_element = etree.SubElement(data_quality_wrapper, f"{{{self.ns.gmd}}}DQ_DataQuality")

        scope = Scope(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_quality_element
        )
        scope.make_element()

        for measure_attributes in self.attributes['resource']['measures']:
            report = Report(
                record=self.record,
                attributes=self.attributes,
                parent_element=data_quality_element,
                element_attributes=measure_attributes
            )
            report.make_element()

        lineage = Lineage(
            record=self.record,
            attributes=self.attributes,
            parent_element=data_quality_element,
            element_attributes=self.attributes['resource']
        )
        lineage.make_element()


class Scope(MetadataRecordElement):
    def make_element(self):
        scope_wrapper = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}scope")
        scope_element = etree.SubElement(scope_wrapper, f"{{{self.ns.gmd}}}DQ_Scope")

        scope_code = ScopeCode(
            record=self.record,
            attributes=self.attributes,
            parent_element=scope_element
        )
        scope_code.make_element()


class Report(MetadataRecordElement):
    def make_element(self):
        report_wrapper = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}report")
        report_element = etree.SubElement(report_wrapper, f"{{{self.ns.gmd}}}DQ_DomainConsistency")

        identification_wrapper = etree.SubElement(report_element, f"{{{self.ns.gmd}}}measureIdentification")
        identification_element = etree.SubElement(identification_wrapper, f"{{{self.ns.gmd}}}RS_Identifier")

        identification_code_element = etree.SubElement(identification_element, f"{{{self.ns.gmd}}}code")
        identification_code_value = etree.SubElement(identification_code_element, f"{{{self.ns.gco}}}CharacterString")
        identification_code_value.text = self.element_attributes['code']

        identification_code_space_element = etree.SubElement(identification_element, f"{{{self.ns.gmd}}}codeSpace")
        identification_code_space_value = etree.SubElement(
            identification_code_space_element,
            f"{{{self.ns.gco}}}CharacterString"
        )
        identification_code_space_value.text = self.element_attributes['code-space']

        result_wrapper = etree.SubElement(report_element, f"{{{self.ns.gmd}}}result")
        result_element = etree.SubElement(result_wrapper, f"{{{self.ns.gmd}}}DQ_ConformanceResult")

        specification_element = etree.SubElement(result_element, f"{{{self.ns.gmd}}}specification")
        citation = Citation(
            record=self.record,
            attributes=self.attributes,
            parent_element=specification_element,
            element_attributes=self.element_attributes
        )
        citation.make_element()

        explanation_element = etree.SubElement(result_element, f"{{{self.ns.gmd}}}explanation")
        explanation_value = etree.SubElement(explanation_element, f"{{{self.ns.gco}}}CharacterString")
        explanation_value.text = self.element_attributes['explanation']

        pass_element = etree.SubElement(result_element, f"{{{self.ns.gmd}}}pass")
        pass_value = etree.SubElement(pass_element, f"{{{self.ns.gco}}}Boolean")
        pass_value.text = str(self.element_attributes['pass']).lower()


class Lineage(MetadataRecordElement):
    def make_element(self):
        lineage_container = etree.SubElement(self.parent_element, f"{{{self.ns.gmd}}}lineage")
        lineage_wrapper = etree.SubElement(lineage_container, f"{{{self.ns.gmd}}}LI_Lineage")
        lineage_element = etree.SubElement(lineage_wrapper, f"{{{self.ns.gmd}}}statement")
        lineage_value = etree.SubElement(lineage_element, f"{{{self.ns.gco}}}CharacterString")
        lineage_value.text = self.element_attributes['lineage']


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
