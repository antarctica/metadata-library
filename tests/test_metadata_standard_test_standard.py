from http import HTTPStatus

from flask import Response

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# This is a testing environment, testing against endpoints that don't themselves allow user input, so the XML returned
# should be safe. In any case the test environment is not exposed and so does not present a risk.
from lxml.etree import ElementTree, XML, fromstring  # nosec

from tests.test_base import BaseTestCase
from tests.standards.test_standard import MetadataRecordConfig, MetadataRecord, Namespaces
from tests import config


def test_standard_route(configuration: str):
    if configuration == 'minimal':
        configuration_object = config.test_standard_minimal_record
    elif configuration == 'typical':
        configuration_object = config.test_standard_typical_record
    elif configuration == 'complete':
        configuration_object = config.test_standard_complete_record
    else:
        return KeyError('Invalid configuration, valid options: [minimal, typical, complete]')

    configuration = MetadataRecordConfig(**configuration_object)
    record = MetadataRecord(configuration)

    return Response(record.generate_xml_document(), mimetype='text/xml')


class MinimalMetadataRecordTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.app.add_url_rule('/standards/test-standard/<configuration>', 'standard_test_standard', test_standard_route)

        self.ns = Namespaces()
        self.configuration = 'minimal'
        self._set_metadata_config(configuration=config.test_standard_minimal_record)

    # Utilities

    def _set_metadata_config(self, configuration: dict):
        self.record_configuration = MetadataRecordConfig(**configuration)
        self.record_attributes = self.record_configuration.config

        self.test_record = MetadataRecord(self.record_configuration)
        self.test_document = self.test_record.generate_xml_document()
        self.test_response = fromstring(self.test_document)

    # Document tests

    def test_record_xml_declaration(self):
        response_xml = ElementTree(XML(self.test_document))
        self.assertEqual(response_xml.docinfo.xml_version, '1.0')
        self.assertEqual(response_xml.docinfo.encoding, 'utf-8')

    def test_record_root_element(self):
        self.assertEqual(self.test_response.tag, f"MetadataRecord")
        self.assertDictEqual(self.test_response.nsmap, self.ns.nsmap())
        self.assertEqual(self.test_response.attrib[f"{{{self.ns.xsi}}}schemaLocation"], self.ns.schema_locations())

    def test_record_contents(self):
        with open(f"tests/resources/records/test-standard/{self.configuration}-record.xml") as expected_contents_file:
            expected_contents = expected_contents_file.read()
            # noinspection PyUnresolvedReferences
            self.assertEqual(expected_contents, self.test_document.decode())

    # Element tests

    def test_resource(self):
        resource = self.test_response.find(f"Resource")
        self.assertIsNotNone(resource)

    def test_resource_title(self):
        resource_title = self.test_response.find(f"Resource/Title")
        self.assertIsNotNone(resource_title)

        if 'href' in self.record_attributes['resource']['title']:
            if f"{{{self.ns.xlink}}}href" in resource_title.attrib:
                self.assertEqual(
                    resource_title.attrib[f"{{{self.ns.xlink}}}href"],
                    self.record_attributes['resource']['title']['href']
                )
        if 'title' in self.record_attributes['resource']['title']:
            if f"{{{self.ns.xlink}}}title" in resource_title.attrib:
                self.assertEqual(
                    resource_title.attrib[f"{{{self.ns.xlink}}}title"],
                    self.record_attributes['resource']['title']['title']
                )
        if 'value' in self.record_attributes['resource']['title']:
            self.assertEqual(resource_title.text, self.record_attributes['resource']['title']['value'])

    # Route test

    def test_record_xml_response(self):
        response = self.client.get(
            f"/standards/test-standard/{self.configuration}",
            base_url='http://localhost:9000'
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.mimetype, 'text/xml')
        self.assertEqual(response.data, self.test_document)


class TypicalMetadataRecordTestCase(MinimalMetadataRecordTestCase):
    def setUp(self):
        super().setUp()

        self.configuration = 'typical'
        self._set_metadata_config(configuration=config.test_standard_typical_record)


class CompleteMetadataRecordTestCase(MinimalMetadataRecordTestCase):
    def setUp(self):
        super().setUp()

        self.configuration = 'complete'
        self._set_metadata_config(configuration=config.test_standard_complete_record)
