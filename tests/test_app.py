import unittest

from http import HTTPStatus

from flask import current_app

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# This is a testing environment, testing against endpoints that don't themselves allow user input, so the XML returned
# should be safe. In any case the test environment is not exposed and so does not present a risk.
from lxml import etree  # nosec

from uk_pdc_metadata_record_generator import create_app, Namespaces


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

        self.maxDiff = None

    def tearDown(self):
        self.app_context.pop()


class AppTestCase(BaseTestCase):
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_record_xml_declaration(self):
        response = self.client.get(
            '/',
            base_url='http://localhost:9000'
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.mimetype, 'text/xml')

        response_xml = etree.ElementTree(etree.XML(response.data))
        self.assertEqual(response_xml.docinfo.xml_version, '1.0')
        self.assertEqual(response_xml.docinfo.encoding, 'utf-8')

    def test_record_root_element(self):
        response = self.client.get(
            '/',
            base_url='http://localhost:9000'
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.mimetype, 'text/xml')

        response_xml = etree.fromstring(response.data)
        self.assertEqual(response_xml.tag, f"{{{ self.ns.gmd }}}MD_Metadata")
        self.assertDictEqual(response_xml.nsmap, self.ns.nsmap())
        self.assertEqual(response_xml.attrib[f"{{{ self.ns.xsi }}}schemaLocation"], self.ns.schema_locations())

    def test_record_file_identifier(self):
        response = self.client.get(
            '/',
            base_url='http://localhost:9000'
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.mimetype, 'text/xml')

        response_xml = etree.fromstring(response.data)
        self.assertIsNotNone(response_xml.find(f"{{{ self.ns.gmd }}}fileIdentifier"))
