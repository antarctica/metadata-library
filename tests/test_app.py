import unittest

from datetime import datetime
from http import HTTPStatus

from flask import current_app

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# This is a testing environment, testing against endpoints that don't themselves allow user input, so the XML returned
# should be safe. In any case the test environment is not exposed and so does not present a risk.
from lxml import etree  # nosec

from uk_pdc_metadata_record_generator import create_app, Namespaces, MetadataRecord, ReferenceSystemInfo, \
    ResourceConstraints
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
        if 'individual' in responsible_party_attributes and 'name' in responsible_party_attributes['individual']:
            if 'href' in responsible_party_attributes['individual']:
                individual_name = responsible_party.find(
                    f"{{{self.ns.gmd}}}individualName/{{{self.ns.gmx}}}Anchor"
                )
                self.assertIsNotNone(individual_name)
                self.assertEqual(
                    individual_name.attrib[f"{{{ self.ns.xlink }}}href"],
                    responsible_party_attributes['individual']['href']
                )
                self.assertEqual(individual_name.attrib[f"{{{ self.ns.xlink }}}actuate"], 'onRequest')
                if 'title' in responsible_party_attributes['individual']:
                    self.assertEqual(
                        individual_name.attrib[f"{{{self.ns.xlink}}}title"],
                        responsible_party_attributes['individual']['title']
                    )
            else:
                individual_name = responsible_party.find(
                    f"{{{self.ns.gmd}}}individualName/{{{self.ns.gco}}}CharacterString"
                )
                self.assertIsNotNone(individual_name)
            self.assertEqual(individual_name.text, responsible_party_attributes['individual']['name'])

        if 'organisation' in responsible_party_attributes and 'name' in responsible_party_attributes['organisation']:
            if 'href' in responsible_party_attributes['organisation']:
                organisation_name = responsible_party.find(
                    f"{{{self.ns.gmd}}}organisationName/{{{self.ns.gmx}}}Anchor"
                )
                self.assertIsNotNone(organisation_name)
                self.assertEqual(
                    organisation_name.attrib[f"{{{ self.ns.xlink }}}href"],
                    responsible_party_attributes['organisation']['href']
                )
                self.assertEqual(organisation_name.attrib[f"{{{ self.ns.xlink }}}actuate"], 'onRequest')
                if 'title' in responsible_party_attributes['organisation']:
                    self.assertEqual(
                        organisation_name.attrib[f"{{{self.ns.xlink}}}title"],
                        responsible_party_attributes['organisation']['title']
                    )
            else:
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

        email = address.find(f"{{{self.ns.gmd}}}electronicMailAddress")
        self.assertIsNotNone(email)
        if 'email' in responsible_party_attributes:
            email = email.find(f"{{{self.ns.gco}}}CharacterString")
            self.assertIsNotNone(email)
            self.assertEqual(email.text, responsible_party_attributes['email'])
        else:
            self.assertEqual(email.attrib[f"{{{self.ns.gco}}}nilReason"], 'unknown')

        if 'online-resource' in responsible_party:
            online_resource = contact_info.find(
                f"{{{self.ns.gmd}}}onlineResource/{{{self.ns.gmd}}}CI_OnlineResource"

            )
            self.assertIsNotNone(online_resource)

            if 'href' in responsible_party['online-resource']:
                linkage = online_resource.find(f"{{{self.ns.gmd}}}linkage/{{{self.ns.gmd}}}URL")
                self.assertIsNotNone(linkage)
                self.assertEqual(linkage.text, responsible_party['online-resource']['href'])

            if 'title' in responsible_party['online-resource']:
                name = online_resource.find(f"{{{self.ns.gmd}}}name/{{{self.ns.gco}}}CharacterString")
                self.assertIsNotNone(name)
                self.assertEqual(name.text, responsible_party['online-resource']['title'])

            if 'description' in responsible_party['online-resource']:
                description = online_resource.find(f"{{{self.ns.gmd}}}description/{{{self.ns.gco}}}CharacterString")
                self.assertIsNotNone(description)
                self.assertEqual(description.text, responsible_party['online-resource']['description'])

            if 'function' in responsible_party['online-resource']:
                function = online_resource.find(f"{{{self.ns.gmd}}}function/{{{self.ns.gco}}}CI_OnLineFunctionCode")
                self.assertIsNotNone(function)
                self.assertEqual(
                    function.attrib['codeList'],
                    'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
                    '/codelist/gmxCodelists.xml#CI_OnLineFunctionCode'
                )
                self.assertEqual(function.attrib['codeListValue'], responsible_party['online-resource']['function'])
                self.assertEqual(function.text, responsible_party['online-resource']['function'])

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

    def _test_citation(self, citation, citation_attributes):
        if 'href' in citation_attributes['title']:
            citation_title = citation.find(f"{{{self.ns.gmd}}}title/{{{self.ns.gmx}}}Anchor")
            self.assertIsNotNone(citation_title)
            self.assertEqual(
                citation_title.attrib[f"{{{self.ns.xlink}}}href"],
                citation_attributes['title']['href']
            )
            self.assertEqual(citation_title.attrib[f"{{{self.ns.xlink}}}actuate"], 'onRequest')
            if 'title' in citation_attributes['title']:
                self.assertEqual(
                    citation_title.attrib[f"{{{self.ns.xlink}}}title"],
                    citation_attributes['title']['title']
                )
        else:
            citation_title = citation.find(f"{{{self.ns.gmd}}}title/{{{self.ns.gco}}}CharacterString")
            self.assertIsNotNone(citation_title)
        self.assertEqual(citation_title.text, citation_attributes['title']['value'])

        if 'dates' in citation_attributes:
            for expected_date in citation_attributes['dates']:
                # Check the record for each expected date based on it's 'date-type', get the parent 'gmd:CI_Date'
                # element so we can check both the gmd:date and gmd:dateType elements are as expected
                record_date_container = citation.xpath(
                    './gmd:date/gmd:CI_Date[gmd:dateType[gmd:CI_DateTypeCode[@codeListValue=$date_type]]]',
                    date_type=expected_date['date-type'],
                    namespaces=self.ns.nsmap()
                )
                self.assertEqual(len(record_date_container), 1)
                record_date_container = record_date_container[0]
                self.assertEqual(record_date_container.tag, f"{{{self.ns.gmd}}}CI_Date")

                record_date = record_date_container.find(f"{{{self.ns.gmd}}}date/{{{self.ns.gco}}}DateTime")
                self.assertIsNotNone(record_date)

                # Partial dates (e.g. year only, '2018') are not supported by Python despite being allowed by ISO 8601.
                # We check these dates as strings, which is not ideal, to a given precision.
                if 'date-precision' in expected_date:
                    if expected_date['date-precision'] == 'year':
                        self.assertEqual(record_date.text, str(expected_date['date'].year))
                    elif expected_date['date-precision'] == 'month':
                        _expected_date = [
                            str(expected_date['date'].year),
                            str(expected_date['date'].month)
                        ]
                        self.assertEqual(record_date.text, '-'.join(_expected_date))
                else:
                    self.assertEqual(datetime.fromisoformat(record_date.text), expected_date['date'])

                record_date_type = record_date_container.find(
                    f"{{{self.ns.gmd}}}dateType/{{{self.ns.gmd}}}CI_DateTypeCode"
                )
                self.assertIsNotNone(record_date_type)
                self.assertEqual(
                    record_date_type.attrib['codeList'],
                    'https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_DateTypeCode'
                )
                self.assertEqual(record_date_type.attrib['codeListValue'], expected_date['date-type'])
                self.assertEqual(record_date_type.text, expected_date['date-type'])

        if 'edition' in citation_attributes:
            edition = citation.find(f"{{{self.ns.gmd}}}edition/{{{self.ns.gco}}}CharacterString")
            self.assertIsNotNone(edition)
            self.assertEqual(edition.text, citation_attributes['edition'])

        if 'identifiers' in citation_attributes:
            for expected_identifier in citation_attributes['identifiers']:
                # Check the record for each expected identifier based on it's 'identifier'
                value_element = 'gco:CharacterString'
                if 'href' in expected_identifier:
                    value_element = 'gmx:Anchor'

                identifier = citation.xpath(
                    f"./gmd:identifier/gmd:MD_Identifier/gmd:code/{value_element}[text()=$identifier]",
                    identifier=expected_identifier['identifier'],
                    namespaces=self.ns.nsmap()
                )
                self.assertEqual(len(identifier), 1)
                identifier = identifier[0]

                self.assertEqual(identifier.text, expected_identifier['identifier'])
                if 'href' in expected_identifier:
                    self.assertEqual(identifier.attrib[f"{{{ self.ns.xlink }}}href"], expected_identifier['href'])
                    self.assertEqual(identifier.attrib[f"{{{ self.ns.xlink }}}actuate"], 'onRequest')
                if 'title' in expected_identifier and 'href' in expected_identifier:
                    self.assertEqual(identifier.attrib[f"{{{self.ns.xlink}}}title"], expected_identifier['title'])

        if 'contact' in citation_attributes:
            cited_responsible_party = citation.find(f"{{{self.ns.gmd}}}citedResponsibleParty")
            self.assertIsNotNone(cited_responsible_party)

            responsible_party = cited_responsible_party.find(f"{{{self.ns.gmd}}}CI_ResponsibleParty")
            self.assertIsNotNone(responsible_party)

            self._test_responsible_party(responsible_party, citation_attributes['contact'])

    def _test_maintenance(self, maintenance, maintenance_attributes):
        maintenance_frequency = maintenance.find(
            f"{{{self.ns.gmd}}}maintenanceAndUpdateFrequency/{{{self.ns.gmd}}}MD_MaintenanceFrequencyCode"
        )
        self.assertIsNotNone(maintenance_frequency)
        self.assertEqual(
            maintenance_frequency.attrib['codeList'],
            'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
            '/codelist/gmxCodelists.xml#MD_MaintenanceFrequencyCode'
        )
        self.assertEqual(maintenance_frequency.attrib['codeListValue'], maintenance_attributes['maintenance-frequency'])
        self.assertEqual(maintenance_frequency.text, maintenance_attributes['maintenance-frequency'])

        maintenance_progress = maintenance.find(
            f"{{{self.ns.gmd}}}maintenanceNote/{{{self.ns.gmd}}}MD_ProgressCode"
        )
        self.assertIsNotNone(maintenance_progress)
        self.assertEqual(
            maintenance_progress.attrib['codeList'],
            'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
            '/codelist/gmxCodelists.xml#MD_ProgressCode'
        )
        self.assertEqual(maintenance_progress.attrib['codeListValue'], maintenance_attributes['progress'])
        self.assertEqual(maintenance_progress.text, maintenance_attributes['progress'])

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
        language = self.test_response.find(f"{{{ self.ns.gmd }}}language/{{{ self.ns.gmd }}}LanguageCode")
        self.assertIsNotNone(language)
        self.assertEqual(language.attrib['codeList'], 'http://www.loc.gov/standards/iso639-2/php/code_list.php')
        self.assertEqual(language.attrib['codeListValue'], self.record_attributes['language'])
        self.assertEqual(language.text, self.record_attributes['language'])

    def test_record_character_set(self):
        character_set = self.test_response.find(
            f"{{{ self.ns.gmd }}}characterSet/{{{ self.ns.gmd }}}MD_CharacterSetCode"
        )
        self.assertIsNotNone(character_set)
        self.assertEqual(
            character_set.attrib['codeList'],
            'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
            '/codelist/gmxCodelists.xml#MD_CharacterSetCode'
        )
        self.assertEqual(character_set.attrib['codeListValue'], self.record_attributes['character_set'])
        self.assertEqual(character_set.text, self.record_attributes['character_set'])

    def test_record_hierarchy_level(self):
        hierarchy_level = self.test_response.find(f"{{{ self.ns.gmd }}}hierarchyLevel/{{{ self.ns.gmd }}}MD_ScopeCode")
        self.assertIsNotNone(hierarchy_level)
        self.assertEqual(
            hierarchy_level.attrib['codeList'],
            'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
            '/codelist/gmxCodelists.xml#MD_ScopeCode'
        )
        self.assertEqual(hierarchy_level.attrib['codeListValue'], self.record_attributes['hierarchy-level'])
        self.assertEqual(hierarchy_level.text, self.record_attributes['hierarchy-level'])

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
        self._test_maintenance(metadata_maintenance, self.record_attributes['maintenance'])

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

        self._test_citation(reference_system_authority, ReferenceSystemInfo.epsg_citation)

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

    def test_data_identification(self):
        data_identification = self.test_response.find(
            f"{{{self.ns.gmd}}}identificationInfo/{{{self.ns.gmd}}}MD_DataIdentification/"
        )
        self.assertIsNotNone(data_identification)

    def test_data_identification_citation(self):
        citation = self.test_response.find(
            f"{{{self.ns.gmd}}}identificationInfo/{{{self.ns.gmd}}}MD_DataIdentification/"
            f"{{{self.ns.gmd}}}citation/{{{self.ns.gmd}}}CI_Citation"
        )

        self._test_citation(citation, self.record_attributes['resource'])

    def test_data_identification_abstract(self):
        abstract = self.test_response.find(
            f"{{{self.ns.gmd}}}identificationInfo/{{{self.ns.gmd}}}MD_DataIdentification/{{{self.ns.gmd}}}abstract/"
            f"{{{self.ns.gco}}}CharacterString"
        )
        self.assertIsNotNone(abstract)
        self.assertEqual(abstract.text, self.record_attributes['resource']['abstract'])

    def test_data_identification_point_of_contact(self):
        expected_pocs = []
        for expected_poc in self.record_attributes['resource']['contacts']:
            if isinstance(expected_poc['role'], list):
                for role in expected_poc['role']:
                    _expected_poc = expected_poc.copy()
                    _expected_poc['role'] = role
                    expected_pocs.append(_expected_poc)
            else:
                expected_pocs.append(expected_poc)

        for expected_poc in expected_pocs:
            with self.subTest(expected_poc=expected_poc):
                if 'individual' not in expected_poc and 'organisation' not in expected_poc:
                    self.skipTest('only pointsOfContact\'s with an individual and/or organisation name may be tested')
                if 'role' not in expected_poc:
                    self.skipTest('only pointsOfContact\'s with a role may be tested')

                # Check the record for each expected point of contact based on it's 'name' and 'role', then get the
                # parent 'CI_ResponsibleParty' element so we can check other properties
                name_element = 'gmd:individualName'
                value_element = 'gco:CharacterString'
                if 'individual' in expected_poc:
                    name = expected_poc['individual']['name']
                    if 'href' in expected_poc['individual']:
                        value_element = 'gmx:Anchor'
                else:
                    name_element = 'gmd:organisationName'
                    name = expected_poc['organisation']['name']
                    if 'href' in expected_poc['organisation']:
                        value_element = 'gmx:Anchor'

                base_xpath = './gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/' \
                             'gmd:CI_ResponsibleParty'
                xpath = f"{base_xpath}[{ name_element }[{ value_element }[text()=$name]] and " \
                    f"gmd:role[gmd:CI_RoleCode[text()=$role]]]"

                responsible_party = self.test_response.xpath(
                    xpath,
                    name=name,
                    role=expected_poc['role'],
                    namespaces=self.ns.nsmap()
                )
                self.assertEqual(len(responsible_party), 1)
                responsible_party = responsible_party[0]
                self._test_responsible_party(responsible_party, expected_poc)

    def test_data_identification_resource_maintenance(self):
        resource_maintenance = self.test_response.find(
            f"{{{self.ns.gmd}}}identificationInfo/{{{self.ns.gmd}}}MD_DataIdentification/"
            f"{{{self.ns.gmd}}}resourceMaintenance/{{{ self.ns.gmd }}}MD_MaintenanceInformation"
        )
        self.assertIsNotNone(resource_maintenance)
        self._test_maintenance(resource_maintenance, self.record_attributes['resource']['maintenance'])

    def test_data_identification_keywords(self):
        for expected_keyword in self.record_attributes['resource']['keywords']:
            with self.subTest(expected_keyword=expected_keyword):
                if 'thesaurus' not in expected_keyword:
                    self.skipTest('only keywords with a thesaurus may be tested')

                value_element = 'gco:CharacterString'
                if 'href' in expected_keyword['thesaurus']['title']:
                    value_element = 'gmx:Anchor'
                xpath = f"./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords" \
                    f"[gmd:thesaurusName[gmd:CI_Citation[gmd:title[{ value_element }[text()=$name]]]]]"
                keyword = self.test_response.xpath(
                    xpath,
                    name=expected_keyword['thesaurus']['title']['value'],
                    namespaces=self.ns.nsmap()
                )
                self.assertEqual(len(keyword), 1)
                keyword = keyword[0]

                for expected_term in expected_keyword['terms']:
                    value_element = 'gco:CharacterString'
                    if 'href' in expected_term:
                        value_element = 'gmx:Anchor'
                    term = keyword.xpath(
                        f"./gmd:keyword/{value_element}[text()=$term]",
                        term=expected_term['title'],
                        namespaces=self.ns.nsmap()
                    )
                    self.assertEqual(len(term), 1)
                    term = term[0]
                    self.assertEqual(term.text, expected_term['title'])
                    if 'href' in expected_term:
                        self.assertEqual(term.attrib[f"{{{self.ns.xlink}}}href"], expected_term['href'])
                        self.assertEqual(term.attrib[f"{{{self.ns.xlink}}}actuate"], 'onRequest')

                thesaurus_citation = keyword.find(f"{{{self.ns.gmd}}}thesaurusName/{{{self.ns.gmd}}}CI_Citation")
                self.assertIsNotNone(thesaurus_citation)
                self._test_citation(thesaurus_citation, expected_keyword['thesaurus'])

    def test_data_identification_resource_constraints(self):
        for expected_access_constraint in self.record_attributes['resource']['constraints']['access']:
            if 'inspire-limitations-on-public-access' in expected_access_constraint:
                constraint = self.test_response.xpath(
                    f"./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                    f"gmd:MD_LegalConstraints[gmd:otherConstraints[gmx:Anchor[text()=$term]]]",
                    term=expected_access_constraint['inspire-limitations-on-public-access'],
                    namespaces=self.ns.nsmap()
                )
                self.assertEqual(len(constraint), 1)
                constraint = constraint[0]

                access_constraint = constraint.find(f"{{{self.ns.gmd}}}accessConstraints/"
                                                    f"{{{self.ns.gmd}}}MD_RestrictionCode")
                self.assertIsNotNone(access_constraint)
                self.assertEqual(
                    access_constraint.attrib['codeList'],
                    'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
                    '/codelist/gmxCodelists.xml#MD_RestrictionCode'
                )
                self.assertEqual(
                    access_constraint.attrib['codeListValue'],
                    expected_access_constraint['restriction-code']
                )
                self.assertEqual(access_constraint.text, expected_access_constraint['restriction-code'])

                public_use_constraint = constraint.find(f"{{{self.ns.gmd}}}otherConstraints/{{{self.ns.gmx}}}Anchor")
                self.assertIsNotNone(public_use_constraint)
                self.assertEqual(
                    public_use_constraint.attrib[f"{{{self.ns.xlink}}}href"],
                    f"http://inspire.ec.europa.eu/metadata-codelist/LimitationsOnPublicAccess/"
                    f"{expected_access_constraint['inspire-limitations-on-public-access']}"
                )
                self.assertEqual(public_use_constraint.attrib[f"{{{self.ns.xlink}}}actuate"], 'onRequest')
                self.assertEqual(
                    public_use_constraint.text,
                    expected_access_constraint['inspire-limitations-on-public-access']
                )

        for expected_usage_constraint in self.record_attributes['resource']['constraints']['usage']:
            if 'copyright-licence' in expected_usage_constraint and \
                    expected_usage_constraint['copyright-licence'] == 'OGL-UK-3.0':
                constraint = self.test_response.xpath(
                    f"./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                    f"gmd:MD_LegalConstraints[gmd:otherConstraints[gmx:Anchor"
                    f"[@xlink:href='{ ResourceConstraints.uk_ogl_v3_anchor['href'] }']]]",
                    namespaces=self.ns.nsmap()
                )
                self.assertEqual(len(constraint), 1)
                constraint = constraint[0]

                usage_constraint = constraint.find(f"{{{self.ns.gmd}}}useConstraints/"
                                                   f"{{{self.ns.gmd}}}MD_RestrictionCode")
                self.assertIsNotNone(usage_constraint)
                self.assertEqual(
                    usage_constraint.attrib['codeList'],
                    'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
                    '/codelist/gmxCodelists.xml#MD_RestrictionCode'
                )
                self.assertEqual(
                    usage_constraint.attrib['codeListValue'],
                    expected_usage_constraint['restriction-code']
                )
                self.assertEqual(usage_constraint.text, expected_usage_constraint['restriction-code'])

                copyright_constraint = constraint.find(f"{{{self.ns.gmd}}}otherConstraints/{{{self.ns.gmx}}}Anchor")
                self.assertIsNotNone(copyright_constraint)
                self.assertEqual(
                    copyright_constraint.attrib[f"{{{self.ns.xlink}}}href"],
                    ResourceConstraints.uk_ogl_v3_anchor['href']
                )
                self.assertEqual(copyright_constraint.attrib[f"{{{self.ns.xlink}}}actuate"], 'onRequest')
                self.assertEqual(
                    copyright_constraint.text,
                    ResourceConstraints.uk_ogl_v3_anchor['value']
                )

            if 'required-citation' in expected_usage_constraint:
                constraint = self.test_response.xpath(
                    f"./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                    f"gmd:MD_LegalConstraints[gmd:otherConstraints[gco:CharacterString"
                    f"[starts-with(text(),'Cite this information as')]]]",
                    namespaces=self.ns.nsmap()
                )
                self.assertEqual(len(constraint), 1)
                constraint = constraint[0]

                citation_constraint = constraint.find(
                    f"{{{self.ns.gmd}}}otherConstraints/{{{self.ns.gco}}}CharacterString"
                )
                self.assertIsNotNone(citation_constraint)
                self.assertEqual(
                    citation_constraint.text,
                    f"Cite this information as: \"{ expected_usage_constraint['required-citation'] }\""
                )

    def test_data_identification_supplemental_information(self):
        supplemental_information = self.test_response.find(
            f"{{{self.ns.gmd}}}identificationInfo/{{{self.ns.gmd}}}MD_DataIdentification/"
            f"{{{self.ns.gmd}}}supplementalInformation/{{{ self.ns.gco }}}CharacterString"
        )
        self.assertIsNotNone(supplemental_information)
        self.assertEqual(supplemental_information.text, self.record_attributes['resource']['supplemental-information'])

    def test_data_identification_spatial_representation_type(self):
        representation_type = self.test_response.find(
            f"{{{self.ns.gmd}}}identificationInfo/{{{self.ns.gmd}}}MD_DataIdentification/"
            f"{{{self.ns.gmd}}}spatialRepresentationType/{{{self.ns.gmd}}}MD_SpatialRepresentationTypeCode"
        )
        self.assertIsNotNone(representation_type)
        self.assertEqual(
            representation_type.attrib['codeList'],
            'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
            '/codelist/gmxCodelists.xml#MD_SpatialRepresentationTypeCode'
        )
        self.assertEqual(
            representation_type.attrib['codeListValue'],
            self.record_attributes['resource']['spatial-representation-type']
        )
        self.assertEqual(representation_type.text, self.record_attributes['resource']['spatial-representation-type'])

    def test_data_identification_spatial_resolution(self):
        spatial_resolution = self.test_response.find(
            f"{{{self.ns.gmd}}}identificationInfo/{{{self.ns.gmd}}}MD_DataIdentification/"
            f"{{{self.ns.gmd}}}spatialResolution/{{{self.ns.gmd}}}MD_Resolution/{{{self.ns.gmd}}}distance"
        )
        self.assertIsNotNone(spatial_resolution)
        self.assertEqual(spatial_resolution.attrib[f"{{{self.ns.gco}}}nilReason"], 'inapplicable')
