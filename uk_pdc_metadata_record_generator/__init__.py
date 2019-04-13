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

    def _record(self) -> Element:
        return etree.Element(
            f"{{{self._ns.gmd}}}MD_Metadata",
            attrib={f"{{{self._ns.xsi}}}schemaLocation": self._ns.schema_locations()},
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
            code_list_value = etree.SubElement(code_list_element, self.element_code, attrib={
                'codeList': self.code_list,
                'codeListValue': self.element_attributes[self.attribute]
            })
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

        if 'organisation' in self.element_attributes and 'name' in self.element_attributes['organisation']:
            organisation_element = etree.SubElement(responsible_party_element, f"{{{self._ns.gmd}}}organisationName")
            organisation_name_value = etree.SubElement(organisation_element, f"{{{self._ns.gco}}}CharacterString")
            organisation_name_value.text = self.element_attributes['organisation']['name']

        if 'phone' in self.element_attributes or 'address' in self.element_attributes \
                or 'email' in self.element_attributes or 'url' in self.element_attributes:
            contact_wrapper = etree.SubElement(responsible_party_element, f"{{{self._ns.gmd}}}contactInfo")
            contact_element = etree.SubElement(contact_wrapper, f"{{{self._ns.gmd}}}CI_Contact")

            if 'phone' in self.element_attributes:
                phone_wrapper = etree.SubElement(contact_element, f"{{{self._ns.gmd}}}phone")
                phone_element = etree.SubElement(phone_wrapper, f"{{{self._ns.gmd}}}CI_Telephone")
                phone_voice = etree.SubElement(phone_element, f"{{{self._ns.gmd}}}voice")
                phone_voice_value = etree.SubElement(phone_voice, f"{{{self._ns.gco}}}CharacterString")
                phone_voice_value.text = self.element_attributes['phone']

            if 'address' in self.element_attributes or 'email' in self.element_attributes:
                address_wrapper = etree.SubElement(contact_element, f"{{{self._ns.gmd}}}address")
                address_element = etree.SubElement(address_wrapper, f"{{{self._ns.gmd}}}CI_Address")

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

            if 'url' in self.element_attributes:
                url_wrapper = etree.SubElement(contact_element, f"{{{self._ns.gmd}}}onlineResource")
                url_element = etree.SubElement(url_wrapper, f"{{{self._ns.gmd}}}CI_OnlineResource")
                linkage = Linkage(
                    record=self.record,
                    attributes=self.attributes,
                    parent_element=url_element,
                    element_attributes=self.element_attributes
                )
                linkage.make_element()


class Linkage(MetadataRecordElement):
    def make_element(self):
        linkage_element = etree.SubElement(self.parent_element, f"{{{self._ns.gmd}}}linkage")
        if 'url' in self.element_attributes:
            url_value = etree.SubElement(linkage_element, f"{{{self._ns.gmd}}}URL")
            url_value.text = self.element_attributes['url']


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
            element_attributes=self.attributes['metadata-maintenance']
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
