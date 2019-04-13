import unittest

from datetime import datetime
from http import HTTPStatus

from flask import current_app

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# This is a testing environment, testing against endpoints that don't themselves allow user input, so the XML returned
# should be safe. In any case the test environment is not exposed and so does not present a risk.
from lxml import etree  # nosec

from uk_pdc_metadata_record_generator import create_app, Namespaces, MetadataRecord, ReferenceSystemInfo
from tests import config


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['ENV'] = 'testing'
        self.app.config['DEBUG'] = True
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        self.ns = Namespaces()

        self.record_attributes = config.test_record

        self.test_record = MetadataRecord(**self.record_attributes)
        self.test_document = etree.tostring(
            etree.ElementTree(self.test_record.record),
            pretty_print=True,
            xml_declaration=True,
            encoding="utf-8"
        )
        self.test_response = etree.fromstring(self.test_document)

        self.maxDiff = None

    def tearDown(self):
        self.app_context.pop()


class AppTestCase(BaseTestCase):
    def _test_responsible_party(self, responsible_party, responsible_party_attributes):
        organisation_name = responsible_party.find(
            f"{{{self.ns.gmd}}}organisationName/{{{self.ns.gco}}}CharacterString"
        )
        self.assertIsNotNone(organisation_name)
        self.assertEqual(organisation_name.text, responsible_party_attributes['organisation']['name'])

        contact_info = responsible_party.find(f"{{{self.ns.gmd}}}contactInfo/{{{self.ns.gmd}}}CI_Contact")
        self.assertIsNotNone(contact_info)

        if 'phone' in responsible_party_attributes:
            phone = contact_info.find(
                f"{{{self.ns.gmd}}}phone/{{{self.ns.gmd}}}CI_Telephone/{{{self.ns.gmd}}}voice/"
                f"{{{self.ns.gco}}}CharacterString"
            )
            self.assertIsNotNone(phone)
            self.assertEqual(phone.text, responsible_party_attributes['phone'])

        if 'address' in responsible_party_attributes or 'email' in responsible_party_attributes:
            address = contact_info.find(f"{{{self.ns.gmd}}}address/{{{self.ns.gmd}}}CI_Address")
            self.assertIsNotNone(address)

            if 'address' in responsible_party and 'delivery-point' in responsible_party['address']:
                delivery_point = address.find(f"{{{self.ns.gmd}}}deliveryPoint/{{{self.ns.gco}}}CharacterString")
                self.assertIsNotNone(delivery_point)
                self.assertEqual(delivery_point.text, responsible_party_attributes['address']['delivery-point'])

            if 'address' in responsible_party and 'city' in responsible_party['address']:
                city = address.find(f"{{{self.ns.gmd}}}city/{{{self.ns.gco}}}CharacterString")
                self.assertIsNotNone(city)
                self.assertEqual(city.text, responsible_party_attributes['address']['city'])

            if 'address' in responsible_party and 'administrative-area' in responsible_party['address']:
                administrative_area = address.find(
                    f"{{{self.ns.gmd}}}administrativeArea/{{{self.ns.gco}}}CharacterString"
                )
                self.assertIsNotNone(administrative_area)
                self.assertEqual(
                    administrative_area.text,
                    responsible_party_attributes['address']['administrative-area']
                )

            if 'address' in responsible_party and 'postal-code' in responsible_party['address']:
                postal_code = address.find(f"{{{self.ns.gmd}}}postalCode/{{{self.ns.gco}}}CharacterString")
                self.assertIsNotNone(postal_code)
                self.assertEqual(postal_code.text, responsible_party_attributes['address']['postal-code'])

            if 'address' in responsible_party and 'country' in responsible_party['address']:
                country = address.find(f"{{{self.ns.gmd}}}country/{{{self.ns.gco}}}CharacterString")
                self.assertIsNotNone(country)
                self.assertEqual(country.text, responsible_party_attributes['address']['country'])

            if 'email' in responsible_party:
                email = address.find(f"{{{self.ns.gmd}}}electronicMailAddress/{{{self.ns.gco}}}CharacterString")
                self.assertIsNotNone(email)
                self.assertEqual(email.text, responsible_party_attributes['email'])

        if 'url' in responsible_party:
            url = contact_info.find(
                f"{{{self.ns.gmd}}}onlineResource/{{{self.ns.gmd}}}CI_OnlineResource/{{{self.ns.gmd}}}linkage/"
                f"{{{self.ns.gmd}}}URL"
            )
            self.assertIsNotNone(url)
            self.assertEqual(url.text, responsible_party_attributes['url'])

        if 'role' in responsible_party:
            role = responsible_party.find(f"{{{self.ns.gmd}}}role/{{{self.ns.gmd}}}CI_RoleCode")
            self.assertIsNotNone(role)
            self.assertEqual(
                role.attrib['codeList'],
                'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
                '/codelist/gmxCodelists.xml#CI_RoleCode'
            )
            self.assertEqual(role.attrib['codeListValue'], responsible_party_attributes['role'])
            self.assertEqual(role.text, responsible_party_attributes['role'])

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_record_xml_response(self):
        response = self.client.get(
            '/',
            base_url='http://localhost:9000'
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.mimetype, 'text/xml')

    def test_record_xml_declaration(self):
        response_xml = etree.ElementTree(etree.XML(self.test_document))
        self.assertEqual(response_xml.docinfo.xml_version, '1.0')
        self.assertEqual(response_xml.docinfo.encoding, 'utf-8')

    def test_record_root_element(self):
        self.assertEqual(self.test_response.tag, f"{{{ self.ns.gmd }}}MD_Metadata")
        self.assertDictEqual(self.test_response.nsmap, self.ns.nsmap())
        self.assertEqual(self.test_response.attrib[f"{{{ self.ns.xsi }}}schemaLocation"], self.ns.schema_locations())

    def test_record_file_identifier(self):
        file_identifier = self.test_response.find(
            f"{{{ self.ns.gmd }}}fileIdentifier/{{{ self.ns.gco }}}CharacterString"
        )
        self.assertIsNotNone(file_identifier)
        self.assertEqual(file_identifier.text, self.record_attributes['file_identifier'])

    def test_record_language(self):
        language = self.test_response.find(f"{{{ self.ns.gmd }}}language")
        self.assertIsNotNone(language)

        language_code = language.find(f"{{{ self.ns.gmd }}}LanguageCode")
        self.assertIsNotNone(language_code)
        self.assertEqual(language_code.attrib['codeList'], 'http://www.loc.gov/standards/iso639-2/php/code_list.php')
        self.assertEqual(language_code.attrib['codeListValue'], self.record_attributes['language'])
        self.assertEqual(language_code.text, self.record_attributes['language'])

    def test_record_character_set(self):
        character_set = self.test_response.find(f"{{{ self.ns.gmd }}}characterSet")
        self.assertIsNotNone(character_set)

        character_set_code = character_set.find(f"{{{ self.ns.gmd }}}MD_CharacterSetCode")
        self.assertIsNotNone(character_set_code)
        self.assertEqual(
            character_set_code.attrib['codeList'],
            'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
            '/codelist/gmxCodelists.xml#MD_CharacterSetCode'
        )
        self.assertEqual(character_set_code.attrib['codeListValue'], self.record_attributes['character_set'])
        self.assertEqual(character_set_code.text, self.record_attributes['character_set'])

    def test_record_hierarchy_level(self):
        hierarchy_level = self.test_response.find(f"{{{ self.ns.gmd }}}hierarchyLevel")
        self.assertIsNotNone(hierarchy_level)

        hierarchy_level_code = hierarchy_level.find(f"{{{ self.ns.gmd }}}MD_ScopeCode")
        self.assertIsNotNone(hierarchy_level_code)
        self.assertEqual(
            hierarchy_level_code.attrib['codeList'],
            'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
            '/codelist/gmxCodelists.xml#MD_ScopeCode'
        )
        self.assertEqual(hierarchy_level_code.attrib['codeListValue'], self.record_attributes['hierarchy-level'])
        self.assertEqual(hierarchy_level_code.text, self.record_attributes['hierarchy-level'])

        hierarchy_level_name = self.test_response.find(
            f"{{{ self.ns.gmd }}}hierarchyLevelName/{{{ self.ns.gco }}}CharacterString"
        )
        self.assertIsNotNone(hierarchy_level_name)
        self.assertEqual(hierarchy_level_name.text, self.record_attributes['hierarchy-level'])

    def test_record_contact(self):
        contact = self.test_response.find(f"{{{ self.ns.gmd }}}contact")
        self.assertIsNotNone(contact)

        responsible_party = contact.find(f"{{{ self.ns.gmd }}}CI_ResponsibleParty")
        self.assertIsNotNone(responsible_party)

        self._test_responsible_party(responsible_party, self.record_attributes['contact'])

    def test_record_date_stamp(self):
        date_stamp = self.test_response.find(f"{{{ self.ns.gmd }}}dateStamp/{{{ self.ns.gco }}}DateTime")
        self.assertIsNotNone(date_stamp)
        self.assertEqual(datetime.fromisoformat(date_stamp.text), self.record_attributes['date-stamp'])

    def test_metadata_maintenance(self):
        metadata_maintenance = self.test_response.find(
            f"{{{ self.ns.gmd }}}metadataMaintenance/{{{ self.ns.gmd }}}MD_MaintenanceInformation"
        )
        self.assertIsNotNone(metadata_maintenance)

        metadata_maintenance_frequency = metadata_maintenance.find(
            f"{{{ self.ns.gmd }}}maintenanceAndUpdateFrequency/{{{ self.ns.gmd }}}MD_MaintenanceFrequencyCode"
        )
        self.assertIsNotNone(metadata_maintenance_frequency)
        self.assertEqual(
            metadata_maintenance_frequency.attrib['codeList'],
            'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
            '/codelist/gmxCodelists.xml#MD_MaintenanceFrequencyCode'
        )
        self.assertEqual(
            metadata_maintenance_frequency.attrib['codeListValue'],
            self.record_attributes['metadata-maintenance']['maintenance-frequency']
        )
        self.assertEqual(
            metadata_maintenance_frequency.text,
            self.record_attributes['metadata-maintenance']['maintenance-frequency']
        )

        metadata_maintenance_progress = metadata_maintenance.find(
            f"{{{ self.ns.gmd }}}maintenanceNote/{{{ self.ns.gmd }}}MD_ProgressCode"
        )
        self.assertIsNotNone(metadata_maintenance_progress)
        self.assertEqual(
            metadata_maintenance_progress.attrib['codeList'],
            'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
            '/codelist/gmxCodelists.xml#MD_ProgressCode'
        )
        self.assertEqual(
            metadata_maintenance_progress.attrib['codeListValue'],
            self.record_attributes['metadata-maintenance']['progress']
        )
        self.assertEqual(
            metadata_maintenance_progress.text,
            self.record_attributes['metadata-maintenance']['progress']
        )

    def test_metadata_standard(self):
        metadata_standard_name = self.test_response.find(
            f"{{{self.ns.gmd}}}metadataStandardName/{{{ self.ns.gco }}}CharacterString"
        )
        self.assertIsNotNone(metadata_standard_name)
        self.assertEqual(metadata_standard_name.text, self.record_attributes['metadata-standard']['name'])

        metadata_standard_version = self.test_response.find(
            f"{{{self.ns.gmd}}}metadataStandardVersion/{{{ self.ns.gco }}}CharacterString"
        )
        self.assertIsNotNone(metadata_standard_version)
        self.assertEqual(metadata_standard_version.text, self.record_attributes['metadata-standard']['version'])

    def test_reference_system_identifier(self):
        reference_system_identifier = self.test_response.find(
            f"{{{self.ns.gmd}}}referenceSystemInfo/{{{self.ns.gmd}}}MD_ReferenceSystem/"
            f"{{{self.ns.gmd}}}referenceSystemIdentifier/{{{self.ns.gmd}}}RS_Identifier"
        )
        self.assertIsNotNone(reference_system_identifier)

        reference_system_authority = reference_system_identifier.find(
            f"{{{self.ns.gmd}}}authority/{{{self.ns.gmd}}}CI_Citation"
        )
        self.assertIsNotNone(reference_system_authority)

        authority_title = reference_system_authority.find(f"{{{self.ns.gmd}}}title/{{{ self.ns.gco }}}CharacterString")
        self.assertIsNotNone(authority_title)
        self.assertEqual(authority_title.text, ReferenceSystemInfo.epsg_citation['title'])

        authority_date_container = reference_system_authority.find(f"{{{self.ns.gmd}}}date/{{{self.ns.gmd}}}CI_Date")
        self.assertIsNotNone(authority_date_container)

        authority_date = authority_date_container.find(f"{{{self.ns.gmd}}}date/{{{self.ns.gco}}}DateTime")
        self.assertIsNotNone(authority_date)
        self.assertEqual(datetime.fromisoformat(authority_date.text), ReferenceSystemInfo.epsg_citation['date']['date'])

        authority_date_type = authority_date_container.find(
            f"{{{self.ns.gmd}}}dateType/{{{self.ns.gmd}}}CI_DateTypeCode"
        )
        self.assertIsNotNone(authority_date_type)
        self.assertEqual(
            authority_date_type.attrib['codeList'],
            'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
            '/codelist/gmxCodelists.xml#CI_DateTypeCode'
        )
        self.assertEqual(
            authority_date_type.attrib['codeListValue'],
            ReferenceSystemInfo.epsg_citation['date']['date-type']
        )
        self.assertEqual(authority_date_type.text, ReferenceSystemInfo.epsg_citation['date']['date-type'])

        authority_citation = reference_system_authority.find(f"{{{self.ns.gmd}}}citedResponsibleParty")
        self.assertIsNotNone(authority_citation)

        responsible_party = authority_citation.find(f"{{{ self.ns.gmd }}}CI_ResponsibleParty")
        self.assertIsNotNone(responsible_party)

        self._test_responsible_party(responsible_party, ReferenceSystemInfo.epsg_citation['contact'])

        reference_system_code = reference_system_identifier.find(f"{{{ self.ns.gmd }}}code/{{{ self.ns.gmx }}}Anchor")
        self.assertIsNotNone(reference_system_code)
        self.assertEqual(
            reference_system_code.attrib[f"{{{self.ns.xlink}}}href"],
            'http://www.opengis.net/def/crs/EPSG/0/4326'
        )
        self.assertEqual(reference_system_code.attrib[f"{{{self.ns.xlink}}}actuate"], 'onRequest')
        self.assertEqual(reference_system_code.text, self.record_attributes['reference-system-info']['code'])

        reference_system_version = reference_system_identifier.find(
            f"{{{self.ns.gmd}}}version/{{{ self.ns.gco }}}CharacterString"
        )
        self.assertIsNotNone(reference_system_version)
        self.assertEqual(reference_system_version.text, self.record_attributes['reference-system-info']['version'])
