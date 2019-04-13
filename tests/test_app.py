import unittest

from datetime import datetime
from http import HTTPStatus

from flask import current_app

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# This is a testing environment, testing against endpoints that don't themselves allow user input, so the XML returned
# should be safe. In any case the test environment is not exposed and so does not present a risk.
from lxml import etree  # nosec

from uk_pdc_metadata_record_generator import create_app, Namespaces, MetadataRecord
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

        organiastion_name = responsible_party.find(
            f"{{{self.ns.gmd}}}organisationName/{{{self.ns.gco}}}CharacterString"
        )
        self.assertIsNotNone(organiastion_name)
        self.assertEqual(organiastion_name.text, self.record_attributes['contact']['organisation']['name'])

        contact_info = responsible_party.find(f"{{{self.ns.gmd}}}contactInfo/{{{self.ns.gmd}}}CI_Contact")
        self.assertIsNotNone(contact_info)

        phone = contact_info.find(
            f"{{{self.ns.gmd}}}phone/{{{self.ns.gmd}}}CI_Telephone/{{{self.ns.gmd}}}voice/"
            f"{{{self.ns.gco}}}CharacterString"
        )
        self.assertIsNotNone(phone)
        self.assertEqual(phone.text, self.record_attributes['contact']['phone'])

        address = contact_info.find(f"{{{self.ns.gmd}}}address/{{{self.ns.gmd}}}CI_Address")
        self.assertIsNotNone(address)

        delivery_point = address.find(f"{{{self.ns.gmd}}}deliveryPoint/{{{self.ns.gco}}}CharacterString")
        self.assertIsNotNone(delivery_point)
        self.assertEqual(delivery_point.text, self.record_attributes['contact']['address']['delivery-point'])

        city = address.find(f"{{{self.ns.gmd}}}city/{{{self.ns.gco}}}CharacterString")
        self.assertIsNotNone(city)
        self.assertEqual(city.text, self.record_attributes['contact']['address']['city'])

        administrative_area = address.find(f"{{{self.ns.gmd}}}administrativeArea/{{{self.ns.gco}}}CharacterString")
        self.assertIsNotNone(administrative_area)
        self.assertEqual(administrative_area.text, self.record_attributes['contact']['address']['administrative-area'])

        postal_code = address.find(f"{{{self.ns.gmd}}}postalCode/{{{self.ns.gco}}}CharacterString")
        self.assertIsNotNone(postal_code)
        self.assertEqual(postal_code.text, self.record_attributes['contact']['address']['postal-code'])

        country = address.find(f"{{{self.ns.gmd}}}country/{{{self.ns.gco}}}CharacterString")
        self.assertIsNotNone(country)
        self.assertEqual(country.text, self.record_attributes['contact']['address']['country'])

        email = address.find(f"{{{self.ns.gmd}}}electronicMailAddress/{{{self.ns.gco}}}CharacterString")
        self.assertIsNotNone(email)
        self.assertEqual(email.text, self.record_attributes['contact']['email'])

        url = contact_info.find(
            f"{{{self.ns.gmd}}}onlineResource/{{{self.ns.gmd}}}CI_OnlineResource/{{{self.ns.gmd}}}linkage/"
            f"{{{self.ns.gmd}}}URL"
        )
        self.assertIsNotNone(url)
        self.assertEqual(url.text, self.record_attributes['contact']['url'])

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
