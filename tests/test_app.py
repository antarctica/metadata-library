import unittest

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
        )



        )


