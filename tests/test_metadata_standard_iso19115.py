from http import HTTPStatus
from datetime import date, datetime

# Exempting Bandit security issue (Using Element to parse untrusted XML data is known to be vulnerable to XML attacks)
#
# This is a testing environment, testing against endpoints that don't themselves allow user input, so the XML returned
# should be safe. In any case the test environment is not exposed and so does not present a risk.
from lxml.etree import ElementTree, XML, fromstring  # nosec

from uk_pdc_metadata_record_generator.standards.iso_19115_v1 import Namespaces, MetadataRecordConfig, MetadataRecord

from tests.test_base import BaseTestCase
from tests import config


class MinimalMetadataRecordTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.ns = Namespaces()
        self.configuration = 'minimal'
        self._set_metadata_config(configuration=config.iso_19115_v1_minimal_record)

    # Utilities

    def _set_metadata_config(self, configuration: dict):
        self.record_configuration = MetadataRecordConfig(**configuration)
        self.record_attributes = self.record_configuration.config

        self.test_record = MetadataRecord(self.record_configuration)
        self.test_document = self.test_record.generate_xml_document()
        self.test_response = fromstring(self.test_document)

    # Common tests

    @staticmethod
    def _test_date_datetime(date_datetime: str, expected_date_datetime):
        if type(expected_date_datetime) is date:
            return date.fromisoformat(date_datetime)
        elif type(expected_date_datetime) is datetime:
            return datetime.fromisoformat(date_datetime)

        raise TypeError('expected value must be a date or datetime')

    def _test_online_resource(self, online_resource, online_resource_attributes):
        if 'href' in online_resource_attributes:
            linkage = online_resource.find(f"{{{self.ns.gmd}}}linkage/{{{self.ns.gmd}}}URL")
            self.assertIsNotNone(linkage)
            self.assertEqual(linkage.text, online_resource_attributes['href'])

        if 'title' in online_resource_attributes:
            name = online_resource.find(f"{{{self.ns.gmd}}}name/{{{self.ns.gco}}}CharacterString")
            self.assertIsNotNone(name)
            self.assertEqual(name.text, online_resource_attributes['title'])

        if 'description' in online_resource_attributes:
            description = online_resource.find(f"{{{self.ns.gmd}}}description/{{{self.ns.gco}}}CharacterString")
            self.assertIsNotNone(description)
            self.assertEqual(description.text, online_resource_attributes['description'])

        if 'function' in online_resource_attributes:
            function = online_resource.find(f"{{{self.ns.gmd}}}function/{{{self.ns.gco}}}CI_OnLineFunctionCode")
            self.assertIsNotNone(function)
            self.assertEqual(
                function.attrib['codeList'],
                'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
                '/codelist/gmxCodelists.xml#CI_OnLineFunctionCode'
            )
            self.assertEqual(function.attrib['codeListValue'], online_resource_attributes['function'])
            self.assertEqual(function.text, online_resource_attributes['function'])

    def _test_responsible_party(self, responsible_party, responsible_party_attributes):
        if 'individual' in responsible_party_attributes and 'name' in responsible_party_attributes['individual']:
            if 'href' in responsible_party_attributes['individual']:
                individual_name = responsible_party.find(
                    f"{{{self.ns.gmd}}}individualName/{{{self.ns.gmx}}}Anchor"
                )
                self.assertIsNotNone(individual_name)
                self.assertEqual(
                    individual_name.attrib[f"{{{self.ns.xlink}}}href"],
                    responsible_party_attributes['individual']['href']
                )
                self.assertEqual(individual_name.attrib[f"{{{self.ns.xlink}}}actuate"], 'onRequest')
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
                    organisation_name.attrib[f"{{{self.ns.xlink}}}href"],
                    responsible_party_attributes['organisation']['href']
                )
                self.assertEqual(organisation_name.attrib[f"{{{self.ns.xlink}}}actuate"], 'onRequest')
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

        if 'address' in responsible_party and 'delivery_point' in responsible_party['address']:
            delivery_point = address.find(f"{{{self.ns.gmd}}}deliveryPoint/{{{self.ns.gco}}}CharacterString")
            self.assertIsNotNone(delivery_point)
            self.assertEqual(delivery_point.text, responsible_party_attributes['address']['delivery_point'])

        if 'address' in responsible_party and 'city' in responsible_party['address']:
            city = address.find(f"{{{self.ns.gmd}}}city/{{{self.ns.gco}}}CharacterString")
            self.assertIsNotNone(city)
            self.assertEqual(city.text, responsible_party_attributes['address']['city'])

        if 'address' in responsible_party and 'administrative_area' in responsible_party['address']:
            administrative_area = address.find(
                f"{{{self.ns.gmd}}}administrativeArea/{{{self.ns.gco}}}CharacterString"
            )
            self.assertIsNotNone(administrative_area)
            self.assertEqual(
                administrative_area.text,
                responsible_party_attributes['address']['administrative_area']
            )

        if 'address' in responsible_party and 'postal_code' in responsible_party['address']:
            postal_code = address.find(f"{{{self.ns.gmd}}}postalCode/{{{self.ns.gco}}}CharacterString")
            self.assertIsNotNone(postal_code)
            self.assertEqual(postal_code.text, responsible_party_attributes['address']['postal_code'])

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

        if 'online_resource' in responsible_party:
            online_resource = contact_info.find(
                f"{{{self.ns.gmd}}}onlineResource/{{{self.ns.gmd}}}CI_OnlineResource"

            )
            self.assertIsNotNone(online_resource)
            self._test_online_resource(online_resource, responsible_party_attributes['online_resource'])

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
                # Check the record for each expected date based on it's 'date_type', get the parent 'gmd:CI_Date'
                # element so we can check both the gmd:date and gmd:dateType elements are as expected
                record_date_container = citation.xpath(
                    './gmd:date/gmd:CI_Date[gmd:dateType[gmd:CI_DateTypeCode[@codeListValue=$date_type]]]',
                    date_type=expected_date['date_type'],
                    namespaces=self.ns.nsmap()
                )
                self.assertEqual(len(record_date_container), 1)
                record_date_container = record_date_container[0]
                self.assertEqual(record_date_container.tag, f"{{{self.ns.gmd}}}CI_Date")

                date_element = None
                if type(expected_date['date']) is date:
                    date_element = f"{{{self.ns.gco}}}Date"
                elif type(expected_date['date']) is datetime:
                    date_element = f"{{{self.ns.gco}}}DateTime"
                record_date = record_date_container.find(f"{{{self.ns.gmd}}}date/{date_element}")
                self.assertIsNotNone(record_date)

                # Partial dates (e.g. year only, '2018') are not supported by Python despite being allowed by ISO 8601.
                # We check these dates as strings, which is not ideal, to a given precision.
                if 'date_precision' in expected_date:
                    if expected_date['date_precision'] == 'year':
                        self.assertEqual(record_date.text, str(expected_date['date'].year))
                    elif expected_date['date_precision'] == 'month':
                        _expected_date = [
                            str(expected_date['date'].year),
                            str(expected_date['date'].month)
                        ]
                        self.assertEqual(record_date.text, '-'.join(_expected_date))
                else:
                    self.assertEqual(
                        self._test_date_datetime(record_date.text, expected_date['date']),
                        expected_date['date']
                    )

                record_date_type = record_date_container.find(
                    f"{{{self.ns.gmd}}}dateType/{{{self.ns.gmd}}}CI_DateTypeCode"
                )
                self.assertIsNotNone(record_date_type)
                self.assertEqual(
                    record_date_type.attrib['codeList'],
                    'https://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_DateTypeCode'
                )
                self.assertEqual(record_date_type.attrib['codeListValue'], expected_date['date_type'])
                self.assertEqual(record_date_type.text, expected_date['date_type'])

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
                    self.assertEqual(identifier.attrib[f"{{{self.ns.xlink}}}href"], expected_identifier['href'])
                    self.assertEqual(identifier.attrib[f"{{{self.ns.xlink}}}actuate"], 'onRequest')
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
        self.assertEqual(maintenance_frequency.attrib['codeListValue'], maintenance_attributes['maintenance_frequency'])
        self.assertEqual(maintenance_frequency.text, maintenance_attributes['maintenance_frequency'])

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

    def _test_language(self, language, language_attribute):
        self.assertEqual(language.attrib['codeList'], 'http://www.loc.gov/standards/iso639-2/php/code_list.php')
        self.assertEqual(language.attrib['codeListValue'], language_attribute)
        self.assertEqual(language.text, language_attribute)

    def _test_contact(self, contact_type, contact, base_xpath):
        if 'individual' not in contact and 'organisation' not in contact:
            self.skipTest(f"only {contact_type}'s with an individual and/or organisation name may be tested")
        if 'role' not in contact:
            self.skipTest(f"only {contact_type}'s with a role may be tested")

        # Check the record for each expected contact based on it's 'name' and 'role', then get the parent
        # 'CI_ResponsibleParty' element so we can check other properties
        name_element = 'gmd:individualName'
        value_element = 'gco:CharacterString'
        if 'individual' in contact:
            name = contact['individual']['name']
            if 'href' in contact['individual']:
                value_element = 'gmx:Anchor'
        else:
            name_element = 'gmd:organisationName'
            name = contact['organisation']['name']
            if 'href' in contact['organisation']:
                value_element = 'gmx:Anchor'

        xpath = f"{base_xpath}[{name_element}[{value_element}[text()=$name]] and " \
            f"gmd:role[gmd:CI_RoleCode[text()=$role]]]"

        responsible_party = self.test_response.xpath(
            xpath,
            name=name,
            role=contact['role'],
            namespaces=self.ns.nsmap()
        )
        self.assertEqual(len(responsible_party), 1)
        responsible_party = responsible_party[0]
        self._test_responsible_party(responsible_party, contact)

    # Document tests

    def test_record_xml_declaration(self):
        response_xml = ElementTree(XML(self.test_document))
        self.assertEqual(response_xml.docinfo.xml_version, '1.0')
        self.assertEqual(response_xml.docinfo.encoding, 'utf-8')

    def test_record_root_element(self):
        self.assertEqual(self.test_response.tag, f"{{{self.ns.gmd}}}MD_Metadata")
        self.assertDictEqual(self.test_response.nsmap, self.ns.nsmap())
        self.assertEqual(self.test_response.attrib[f"{{{self.ns.xsi}}}schemaLocation"], self.ns.schema_locations())

    # Element tests

    def test_record_file_identifier(self):
        if 'file_identifier' in self.record_attributes:
            file_identifier = self.test_response.find(
                f"{{{self.ns.gmd}}}fileIdentifier/{{{self.ns.gco}}}CharacterString"
            )
            self.assertIsNotNone(file_identifier)
            self.assertEqual(file_identifier.text, self.record_attributes['file_identifier'])

    def test_record_language(self):
        if 'language' in self.record_attributes:
            language = self.test_response.find(f"{{{self.ns.gmd}}}language/{{{self.ns.gmd}}}LanguageCode")
            self.assertIsNotNone(language)
            self._test_language(language, self.record_attributes['language'])

    def test_record_character_set(self):
        if 'character_set' in self.record_attributes:
            character_set = self.test_response.find(
                f"{{{self.ns.gmd}}}characterSet/{{{self.ns.gmd}}}MD_CharacterSetCode"
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
        if 'hierarchy_level' in self.record_attributes:
            hierarchy_level = self.test_response.find(f"{{{self.ns.gmd}}}hierarchyLevel/{{{self.ns.gmd}}}MD_ScopeCode")
            self.assertIsNotNone(hierarchy_level)
            self.assertEqual(
                hierarchy_level.attrib['codeList'],
                'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
                '/codelist/gmxCodelists.xml#MD_ScopeCode'
            )
            self.assertEqual(hierarchy_level.attrib['codeListValue'], self.record_attributes['hierarchy_level'])
            self.assertEqual(hierarchy_level.text, self.record_attributes['hierarchy_level'])

            hierarchy_level_name = self.test_response.find(
                f"{{{self.ns.gmd}}}hierarchyLevelName/{{{self.ns.gco}}}CharacterString"
            )
            self.assertIsNotNone(hierarchy_level_name)
            self.assertEqual(hierarchy_level_name.text, self.record_attributes['hierarchy_level'])

    def test_record_contact(self):
        expected_contacts = []
        for expected_contact in self.record_attributes['contacts']:
            for role in expected_contact['role']:
                _expected_contact = expected_contact.copy()
                _expected_contact['role'] = role
                expected_contacts.append(_expected_contact)

        base_xpath = './gmd:contact/gmd:CI_ResponsibleParty'

        for expected_contact in expected_contacts:
            with self.subTest(expected_contact=expected_contact):
                self._test_contact(contact_type='contact', contact=expected_contact, base_xpath=base_xpath)

    def test_record_date_stamp(self):
        date_stamp = self.test_response.find(f"{{{self.ns.gmd}}}dateStamp/{{{self.ns.gco}}}DateTime")
        self.assertIsNotNone(date_stamp)
        self.assertEqual(datetime.fromisoformat(date_stamp.text), self.record_attributes['date_stamp'])

    def test_metadata_maintenance(self):
        if 'maintenance' in self.record_attributes:
            metadata_maintenance = self.test_response.find(
                f"{{{self.ns.gmd}}}metadataMaintenance/{{{self.ns.gmd}}}MD_MaintenanceInformation"
            )
            self.assertIsNotNone(metadata_maintenance)
            self._test_maintenance(metadata_maintenance, self.record_attributes['maintenance'])

    def test_metadata_standard(self):
        if 'metadata_standard' in self.record_attributes:
            metadata_standard_name = self.test_response.find(
                f"{{{self.ns.gmd}}}metadataStandardName/{{{self.ns.gco}}}CharacterString"
            )
            self.assertIsNotNone(metadata_standard_name)
            self.assertEqual(metadata_standard_name.text, self.record_attributes['metadata_standard']['name'])

            metadata_standard_version = self.test_response.find(
                f"{{{self.ns.gmd}}}metadataStandardVersion/{{{self.ns.gco}}}CharacterString"
            )
            self.assertIsNotNone(metadata_standard_version)
            self.assertEqual(metadata_standard_version.text, self.record_attributes['metadata_standard']['version'])

    def test_reference_system_identifier(self):
        if 'reference_system_info' in self.record_attributes:
            reference_system_identifier = self.test_response.find(
                f"{{{self.ns.gmd}}}referenceSystemInfo/{{{self.ns.gmd}}}MD_ReferenceSystem/"
                f"{{{self.ns.gmd}}}referenceSystemIdentifier/{{{self.ns.gmd}}}RS_Identifier"
            )
            self.assertIsNotNone(reference_system_identifier)

            reference_system_authority = reference_system_identifier.find(
                f"{{{self.ns.gmd}}}authority/{{{self.ns.gmd}}}CI_Citation"
            )
            self.assertIsNotNone(reference_system_authority)
            self._test_citation(
                reference_system_authority,
                self.record_attributes['reference_system_info']['authority']
            )

            reference_system_code = reference_system_identifier.find(f"{{{self.ns.gmd}}}code/{{{self.ns.gmx}}}Anchor")
            self.assertIsNotNone(reference_system_code)
            self.assertEqual(
                reference_system_code.attrib[f"{{{self.ns.xlink}}}href"],
                self.record_attributes['reference_system_info']['code']['href']
            )
            self.assertEqual(reference_system_code.attrib[f"{{{self.ns.xlink}}}actuate"], 'onRequest')
            self.assertEqual(
                reference_system_code.text,
                self.record_attributes['reference_system_info']['code']['value']
            )

            reference_system_version = reference_system_identifier.find(
                f"{{{self.ns.gmd}}}version/{{{self.ns.gco}}}CharacterString"
            )
            self.assertIsNotNone(reference_system_version)
            self.assertEqual(reference_system_version.text, self.record_attributes['reference_system_info']['version'])

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
        self.assertIsNotNone(citation)
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
        if 'contacts' in self.record_attributes['resource']:
            for expected_poc in self.record_attributes['resource']['contacts']:
                for role in expected_poc['role']:
                    if role != 'distributor':
                        _expected_poc = expected_poc.copy()
                        _expected_poc['role'] = role
                        expected_pocs.append(_expected_poc)

            base_xpath = './gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty'

            for expected_poc in expected_pocs:
                with self.subTest(expected_poc=expected_poc):
                    self._test_contact(contact_type='pointOfContact', contact=expected_poc, base_xpath=base_xpath)

    def test_data_identification_resource_maintenance(self):
        if 'maintenance' in self.record_attributes['resource']:
            resource_maintenance = self.test_response.find(
                f"{{{self.ns.gmd}}}identificationInfo/{{{self.ns.gmd}}}MD_DataIdentification/"
                f"{{{self.ns.gmd}}}resourceMaintenance/{{{self.ns.gmd}}}MD_MaintenanceInformation"
            )
            self.assertIsNotNone(resource_maintenance)
            self._test_maintenance(resource_maintenance, self.record_attributes['resource']['maintenance'])

    def test_data_identification_keywords(self):
        if 'keywords' in self.record_attributes['resource']:
            for expected_keyword in self.record_attributes['resource']['keywords']:
                with self.subTest(expected_keyword=expected_keyword):
                    if 'thesaurus' not in expected_keyword:
                        self.skipTest('only keywords with a thesaurus may be tested')

                    value_element = 'gco:CharacterString'
                    if 'href' in expected_keyword['thesaurus']['title']:
                        value_element = 'gmx:Anchor'
                    xpath = f"./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/" \
                        f"gmd:MD_Keywords[gmd:thesaurusName[gmd:CI_Citation[gmd:title[{value_element}[text()=$name]]]]]"
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
                            term=expected_term['term'],
                            namespaces=self.ns.nsmap()
                        )
                        self.assertEqual(len(term), 1)
                        term = term[0]
                        self.assertEqual(term.text, expected_term['term'])
                        if 'href' in expected_term:
                            self.assertEqual(term.attrib[f"{{{self.ns.xlink}}}href"], expected_term['href'])
                            self.assertEqual(term.attrib[f"{{{self.ns.xlink}}}actuate"], 'onRequest')
                        if 'title' in expected_term:
                            self.assertEqual(term.attrib[f"{{{self.ns.xlink}}}title"], expected_term['title'])

                    thesaurus_citation = keyword.find(f"{{{self.ns.gmd}}}thesaurusName/{{{self.ns.gmd}}}CI_Citation")
                    self.assertIsNotNone(thesaurus_citation)
                    self._test_citation(thesaurus_citation, expected_keyword['thesaurus'])

    def test_data_identification_resource_constraints(self):
        if 'constraints' in self.record_attributes['resource']:
            for expected_access_constraint in self.record_attributes['resource']['constraints']['access']:
                if 'inspire_limitations_on_public_access' in expected_access_constraint:
                    constraint = self.test_response.xpath(
                        f"./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                        f"gmd:MD_LegalConstraints[gmd:otherConstraints[gmx:Anchor[text()=$term]]]",
                        term=expected_access_constraint['inspire_limitations_on_public_access'],
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
                        expected_access_constraint['restriction_code']
                    )
                    self.assertEqual(access_constraint.text, expected_access_constraint['restriction_code'])

                    public_use_constraint = constraint.find(
                        f"{{{self.ns.gmd}}}otherConstraints/{{{self.ns.gmx}}}Anchor"
                    )
                    self.assertIsNotNone(public_use_constraint)
                    self.assertEqual(
                        public_use_constraint.attrib[f"{{{self.ns.xlink}}}href"],
                        f"http://inspire.ec.europa.eu/metadata-codelist/LimitationsOnPublicAccess/"
                        f"{expected_access_constraint['inspire_limitations_on_public_access']}"
                    )
                    self.assertEqual(public_use_constraint.attrib[f"{{{self.ns.xlink}}}actuate"], 'onRequest')
                    self.assertEqual(
                        public_use_constraint.text,
                        expected_access_constraint['inspire_limitations_on_public_access']
                    )

            for expected_usage_constraint in self.record_attributes['resource']['constraints']['usage']:
                if 'copyright_licence' in expected_usage_constraint and \
                        'href' in expected_usage_constraint['copyright_licence']:
                    constraint = self.test_response.xpath(
                        f"./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                        f"gmd:MD_LegalConstraints[@id='copyright']",
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
                        expected_usage_constraint['restriction_code']
                    )
                    self.assertEqual(usage_constraint.text, expected_usage_constraint['restriction_code'])

                    copyright_constraint = constraint.find(f"{{{self.ns.gmd}}}otherConstraints/{{{self.ns.gmx}}}Anchor")
                    self.assertIsNotNone(copyright_constraint)
                    self.assertEqual(
                        copyright_constraint.attrib[f"{{{self.ns.xlink}}}href"],
                        expected_usage_constraint['copyright_licence']['href']
                    )
                    self.assertEqual(copyright_constraint.attrib[f"{{{self.ns.xlink}}}actuate"], 'onRequest')
                    self.assertEqual(
                        copyright_constraint.text,
                        expected_usage_constraint['copyright_licence']['statement']
                    )

                if 'required_citation' in expected_usage_constraint:
                    constraint = self.test_response.xpath(
                        f"./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/"
                        f"gmd:MD_LegalConstraints[@id='citation']",
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
                        f"Cite this information as: \"{expected_usage_constraint['required_citation']}\""
                    )

    def test_data_identification_supplemental_information(self):
        if 'supplemental_information' in self.record_attributes['resource']:
            supplemental_information = self.test_response.find(
                f"{{{self.ns.gmd}}}identificationInfo/{{{self.ns.gmd}}}MD_DataIdentification/"
                f"{{{self.ns.gmd}}}supplementalInformation/{{{self.ns.gco}}}CharacterString"
            )
            self.assertIsNotNone(supplemental_information)
            self.assertEqual(
                supplemental_information.text,
                self.record_attributes['resource']['supplemental_information']
            )

    def test_data_identification_spatial_representation_type(self):
        if 'spatial_representation_type' in self.record_attributes['resource']:
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
                self.record_attributes['resource']['spatial_representation_type']
            )
            self.assertEqual(
                representation_type.text,
                self.record_attributes['resource']['spatial_representation_type']
            )

    def test_data_identification_spatial_resolution(self):
        if 'spatial_resolution' in self.record_attributes['resource']:
            spatial_resolution = self.test_response.find(
                f"{{{self.ns.gmd}}}identificationInfo/{{{self.ns.gmd}}}MD_DataIdentification/"
                f"{{{self.ns.gmd}}}spatialResolution/{{{self.ns.gmd}}}MD_Resolution/{{{self.ns.gmd}}}distance"
            )
            self.assertIsNotNone(spatial_resolution)
            if self.record_attributes['resource']['spatial_resolution'] is None:
                self.assertEqual(spatial_resolution.attrib[f"{{{self.ns.gco}}}nilReason"], 'inapplicable')

    def test_data_identification_language(self):
        language = self.test_response.find(
            f"{{{self.ns.gmd}}}identificationInfo/{{{self.ns.gmd}}}MD_DataIdentification/"
            f"{{{self.ns.gmd}}}language/{{{self.ns.gmd}}}LanguageCode"
        )
        self.assertIsNotNone(language)
        self._test_language(language, self.record_attributes['resource']['language'])

    def test_data_identification_topic_categories(self):
        if 'topics' in self.record_attributes['resource']:
            for expected_topic in self.record_attributes['resource']['topics']:
                with self.subTest(expected_topic=expected_topic):
                    topic = self.test_response.xpath(
                        f"./gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory"
                        f"[gmd:MD_TopicCategoryCode[text()=$topic]]",
                        topic=expected_topic,
                        namespaces=self.ns.nsmap()
                    )
                    self.assertEqual(len(topic), 1)

    def test_data_identification_extent(self):
        if 'extent' in self.record_attributes['resource']:
            extent = self.test_response.find(
                f"{{{self.ns.gmd}}}identificationInfo/{{{self.ns.gmd}}}MD_DataIdentification/{{{self.ns.gmd}}}extent"
                f"/{{{self.ns.gmd}}}EX_Extent"
            )
            self.assertIsNotNone(extent)

    def test_data_identification_extent_geographic(self):
        if 'extent' in self.record_attributes['resource'] and 'geographic' in \
                self.record_attributes['resource']['extent'] and 'bounding_box' in \
                self.record_attributes['resource']['extent']['geographic']:
            expected_bounding_box = self.record_attributes['resource']['extent']['geographic']['bounding_box']
            bounding_box = self.test_response.find(
                f"{{{self.ns.gmd}}}identificationInfo/{{{self.ns.gmd}}}MD_DataIdentification/{{{self.ns.gmd}}}extent/"
                f"{{{self.ns.gmd}}}EX_Extent/{{{self.ns.gmd}}}geographicElement/"
                f"{{{self.ns.gmd}}}EX_GeographicBoundingBox"
            )
            self.assertIsNotNone(bounding_box)

            west = bounding_box.find(f"{{{self.ns.gmd}}}westBoundLongitude/{{{self.ns.gco}}}Decimal")
            self.assertIsNotNone(west)
            self.assertEqual(west.text, str(expected_bounding_box['west_longitude']))

            east = bounding_box.find(f"{{{self.ns.gmd}}}eastBoundLongitude/{{{self.ns.gco}}}Decimal")
            self.assertIsNotNone(east)
            self.assertEqual(east.text, str(expected_bounding_box['east_longitude']))

            south = bounding_box.find(f"{{{self.ns.gmd}}}southBoundLatitude/{{{self.ns.gco}}}Decimal")
            self.assertIsNotNone(south)
            self.assertEqual(south.text, str(expected_bounding_box['south_latitude']))

            north = bounding_box.find(f"{{{self.ns.gmd}}}northBoundLatitude/{{{self.ns.gco}}}Decimal")
            self.assertIsNotNone(north)
            self.assertEqual(north.text, str(expected_bounding_box['north_latitude']))

    def test_data_identification_extent_vertical(self):
        if 'extent' in self.record_attributes['resource'] and 'vertical' in \
                self.record_attributes['resource']['extent']:
            vertical_extent = self.test_response.find(
                f"{{{self.ns.gmd}}}identificationInfo/{{{self.ns.gmd}}}MD_DataIdentification/{{{self.ns.gmd}}}extent/"
                f"{{{self.ns.gmd}}}EX_Extent/{{{self.ns.gmd}}}verticalElement/{{{self.ns.gmd}}}EX_VerticalExtent"
            )
            self.assertIsNotNone(vertical_extent)

            minimum = vertical_extent.find(f"{{{self.ns.gmd}}}minimumValue")
            self.assertIsNotNone(minimum)
            if 'minimum' in self.record_attributes['resource']['extent']['vertical']:
                minimum_value = minimum.find(f"{{{self.ns.gco}}}Decimal")
                self.assertIsNotNone(minimum_value)
                self.assertEqual(
                    minimum_value.text,
                    str(self.record_attributes['resource']['extent']['vertical']['minimum'])
                )
            else:
                self.assertEqual(minimum.attrib[f"{{{self.ns.gco}}}nilReason"], 'unknown')

            maximum = vertical_extent.find(f"{{{self.ns.gmd}}}maximumValue")
            self.assertIsNotNone(maximum)
            if 'maximum' in self.record_attributes['resource']['extent']['vertical']:
                minimum_value = maximum.find(f"{{{self.ns.gco}}}Decimal")
                self.assertIsNotNone(minimum_value)
                self.assertEqual(
                    minimum_value.text,
                    str(self.record_attributes['resource']['extent']['vertical']['minimum'])
                )
            else:
                self.assertEqual(maximum.attrib[f"{{{self.ns.gco}}}nilReason"], 'unknown')

            vertical_crs = vertical_extent.find(f"{{{self.ns.gmd}}}verticalCRS/{{{self.ns.gml}}}VerticalCRS")
            self.assertIsNotNone(vertical_crs)
            self.assertEqual(
                vertical_crs.attrib[f"{{{self.ns.gml}}}id"],
                self.record_attributes['resource']['extent']['vertical']['identifier']
            )

            identifier = vertical_crs.find(f"{{{self.ns.gml}}}identifier")
            self.assertIsNotNone(identifier)
            self.assertEqual(identifier.attrib['codeSpace'], 'OGP')
            self.assertEqual(identifier.text, self.record_attributes['resource']['extent']['vertical']['code'])

            name = vertical_crs.find(f"{{{self.ns.gml}}}name")
            self.assertIsNotNone(name)
            self.assertEqual(name.text, self.record_attributes['resource']['extent']['vertical']['name'])

            remarks = vertical_crs.find(f"{{{self.ns.gml}}}remarks")
            self.assertIsNotNone(remarks)
            self.assertEqual(remarks.text, self.record_attributes['resource']['extent']['vertical']['remarks'])

            domain = vertical_crs.find(f"{{{self.ns.gml}}}domainOfValidity")
            self.assertIsNotNone(domain)
            self.assertEqual(
                domain.attrib[f"{{{self.ns.xlink}}}href"],
                self.record_attributes['resource']['extent']['vertical']['domain_of_validity']['href']
            )

            scope = vertical_crs.find(f"{{{self.ns.gml}}}scope")
            self.assertIsNotNone(scope)
            self.assertEqual(scope.text, self.record_attributes['resource']['extent']['vertical']['scope'])

            vertical_cs = vertical_crs.find(f"{{{self.ns.gml}}}verticalCS")
            self.assertIsNotNone(vertical_cs)
            self.assertEqual(
                vertical_cs.attrib[f"{{{self.ns.xlink}}}href"],
                self.record_attributes['resource']['extent']['vertical']['vertical_cs']['href']
            )

            vertical_datum = vertical_crs.find(f"{{{self.ns.gml}}}verticalDatum")
            self.assertIsNotNone(vertical_datum)
            self.assertEqual(
                vertical_datum.attrib[f"{{{self.ns.xlink}}}href"],
                self.record_attributes['resource']['extent']['vertical']['vertical_datum']['href']
            )

    def test_data_identification_extent_temporal(self):
        if 'extent' in self.record_attributes['resource'] and 'temporal' in \
                self.record_attributes['resource']['extent']:
            temporal_extent = self.test_response.find(
                f"{{{self.ns.gmd}}}identificationInfo/{{{self.ns.gmd}}}MD_DataIdentification/{{{self.ns.gmd}}}extent/"
                f"{{{self.ns.gmd}}}EX_Extent/{{{self.ns.gmd}}}temporalElement/{{{self.ns.gmd}}}EX_TemporalExtent/"
                f"{{{self.ns.gmd}}}extent/{{{self.ns.gml}}}TimePeriod"
            )
            self.assertIsNotNone(temporal_extent)
            self.assertEqual(temporal_extent.attrib[f"{{{self.ns.gml}}}id"], 'boundingExtent')

            beginning = temporal_extent.find(f"{{{self.ns.gml}}}beginPosition")
            self.assertIsNotNone(datetime.fromisoformat(beginning.text))
            self.assertEqual(
                self._test_date_datetime(
                    beginning.text,
                    self.record_attributes['resource']['extent']['temporal']['period']['start']
                ),
                self.record_attributes['resource']['extent']['temporal']['period']['start']
            )

            end = temporal_extent.find(f"{{{self.ns.gml}}}endPosition")
            self.assertIsNotNone(end)
            self.assertEqual(
                self._test_date_datetime(
                    end.text,
                    self.record_attributes['resource']['extent']['temporal']['period']['end']
                ),
                self.record_attributes['resource']['extent']['temporal']['period']['end']
            )

    def test_data_distribution(self):
        _has_data_distributor = False
        if 'contacts' in self.record_attributes['resource']:
            for expected_distributor in self.record_attributes['resource']['contacts']:
                for role in expected_distributor['role']:
                    if role == 'distributor':
                        _has_data_distributor = True
                        break

        if 'formats' in self.record_attributes['resource'] or 'transfer_options' in self.record_attributes['resource'] \
                or _has_data_distributor:
            data_distribution = self.test_response.find(
                f"{{{self.ns.gmd}}}distributionInfo/{{{self.ns.gmd}}}MD_Distribution/"
            )
            self.assertIsNotNone(data_distribution)

    def test_data_distribution_formats(self):
        if 'formats' in self.record_attributes['resource']:
            for expected_format in self.record_attributes['resource']['formats']:
                with self.subTest(expected_format=expected_format):
                    base_xpath = './gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format'
                    xpath = f"{base_xpath}[gmd:name[gco:CharacterString[text()=$format]]]"
                    format_identifier = expected_format['format']

                    if 'href' in expected_format:
                        xpath = f"{base_xpath}[gmd:name[gmx:Anchor[@xlink:href=$format]]]"
                        format_identifier = expected_format['href']

                    transfer_format = self.test_response.xpath(
                        xpath,
                        format=format_identifier,
                        namespaces=self.ns.nsmap()
                    )
                    self.assertEqual(len(transfer_format), 1)
                    transfer_format = transfer_format[0]

                    if 'href' in expected_format:
                        transfer_format_value = transfer_format.find(f"{{{self.ns.gmd}}}name/{{{self.ns.gmx}}}Anchor")
                        self.assertIsNotNone(transfer_format_value)
                        self.assertEqual(
                            transfer_format_value.attrib[f"{{{self.ns.xlink}}}href"],
                            expected_format['href']
                        )
                        self.assertEqual(transfer_format_value.attrib[f"{{{self.ns.xlink}}}actuate"], 'onRequest')
                        if 'title' in expected_format:
                            self.assertEqual(
                                transfer_format_value.attrib[f"{{{self.ns.xlink}}}title"],
                                expected_format['title']
                            )
                    else:
                        transfer_format_value = transfer_format.find(
                            f"{{{self.ns.gmd}}}name/{{{self.ns.gco}}}CharacterString"
                        )
                        self.assertIsNotNone(transfer_format_value)
                    self.assertEqual(transfer_format_value.text, expected_format['format'])

    def test_data_distribution_distributors(self):
        expected_distributors = []

        if 'contacts' in self.record_attributes['resource']:
            for expected_distributor in self.record_attributes['resource']['contacts']:
                for role in expected_distributor['role']:
                    if role == 'distributor':
                        _expected_poc = expected_distributor.copy()
                        _expected_poc['role'] = role
                        expected_distributors.append(_expected_poc)

            base_xpath = './gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/' \
                         'gmd:distributorContact/gmd:CI_ResponsibleParty'

            for expected_distributor in expected_distributors:
                with self.subTest(expected_distributor=expected_distributor):
                    self._test_contact(contact_type='distributor', contact=expected_distributor, base_xpath=base_xpath)

    def test_data_distribution_transfer_options(self):
        if 'transfer_options' in self.record_attributes['resource']:
            for expected_transfer_options in self.record_attributes['resource']['transfer_options']:
                with self.subTest(expected_transfer_options=expected_transfer_options):
                    xpath = './gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/' \
                            'gmd:MD_DigitalTransferOptions[gmd:onLine[gmd:CI_OnlineResource' \
                            '[gmd:linkage[gmd:URL[text()=$transfer_option]]]]]'

                    transfer_option = self.test_response.xpath(
                        xpath,
                        transfer_option=expected_transfer_options['online_resource']['href'],
                        namespaces=self.ns.nsmap()
                    )
                    self.assertEqual(len(transfer_option), 1)
                    transfer_option = transfer_option[0]

                    if 'size' in expected_transfer_options:
                        if 'unit' in expected_transfer_options['size']:
                            unit_value = transfer_option.find(
                                f"{{{self.ns.gmd}}}unitsOfDistribution/{{{self.ns.gco}}}CharacterString"
                            )
                            self.assertIsNotNone(unit_value)
                            self.assertEqual(unit_value.text, expected_transfer_options['size']['unit'])
                        if 'magnitude' in expected_transfer_options['size']:
                            unit_value = transfer_option.find(
                                f"{{{self.ns.gmd}}}transferSize/{{{self.ns.gco}}}Real"
                            )
                            self.assertIsNotNone(unit_value)
                            self.assertEqual(unit_value.text, str(expected_transfer_options['size']['magnitude']))

                    self._test_online_resource(transfer_option, expected_transfer_options)

    def test_data_quality(self):
        if 'measures' in self.record_attributes['resource'] or 'lineage' in self.record_attributes['resource'] or \
                'hierarchy_level' in self.record_attributes:
            data_quality = self.test_response.find(
                f"{{{self.ns.gmd}}}dataQualityInfo/{{{self.ns.gmd}}}DQ_DataQuality"
            )
            self.assertIsNotNone(data_quality)

    def test_data_quality_scope(self):
        if 'hierarchy_level' in self.record_attributes:
            scope = self.test_response.find(
                f"{{{self.ns.gmd}}}dataQualityInfo/{{{self.ns.gmd}}}DQ_DataQuality/{{{self.ns.gmd}}}scope/"
                f"{{{self.ns.gmd}}}DQ_Scope"
            )
            self.assertIsNotNone(scope)

            scope_code = scope.find(f"{{{self.ns.gmd}}}level/{{{self.ns.gmd}}}MD_ScopeCode")
            self.assertIsNotNone(scope_code)
            self.assertEqual(
                scope_code.attrib['codeList'],
                'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources'
                '/codelist/gmxCodelists.xml#MD_ScopeCode'
            )
            self.assertEqual(scope_code.attrib['codeListValue'], self.record_attributes['hierarchy_level'])
            self.assertEqual(scope_code.text, self.record_attributes['hierarchy_level'])

    def test_data_quality_measures(self):
        if 'measures' in self.record_attributes['resource']:
            for expected_measure in self.record_attributes['resource']['measures']:
                with self.subTest(expected_measure=expected_measure):
                    xpath = './gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_DomainConsistency' \
                            '[gmd:measureIdentification[gmd:RS_Identifier[gmd:code[gco:CharacterString[text()=$code]]' \
                            ' and gmd:codeSpace[gco:CharacterString[text()=$code_space]]]]]'

                    measure = self.test_response.xpath(
                        xpath,
                        code=expected_measure['code'],
                        code_space=expected_measure['code_space'],
                        namespaces=self.ns.nsmap()
                    )
                    self.assertEqual(len(measure), 1)
                    measure = measure[0]

                    measure_identifier = measure.find(
                        f"{{{self.ns.gmd}}}measureIdentification/{{{self.ns.gmd}}}RS_Identifier"
                    )
                    self.assertIsNotNone(measure_identifier)
                    measure_identifier_code = measure_identifier.find(
                        f"{{{self.ns.gmd}}}code/{{{self.ns.gco}}}CharacterString"
                    )
                    self.assertIsNotNone(measure_identifier_code)
                    self.assertEqual(measure_identifier_code.text, expected_measure['code'])
                    measure_identifier_code_space = measure_identifier.find(
                        f"{{{self.ns.gmd}}}codeSpace/{{{self.ns.gco}}}CharacterString"
                    )
                    self.assertIsNotNone(measure_identifier_code_space)
                    self.assertEqual(measure_identifier_code_space.text, expected_measure['code_space'])

                    measure_result = measure.find(
                        f"{{{self.ns.gmd}}}result/{{{self.ns.gmd}}}DQ_ConformanceResult"
                    )

                    measure_citation = measure_result.find(
                        f"{{{self.ns.gmd}}}specification/{{{self.ns.gmd}}}CI_Citation"
                    )
                    self.assertIsNotNone(measure_citation)
                    self._test_citation(measure_citation, expected_measure)

                    measure_explanation = measure_result.find(
                        f"{{{self.ns.gmd}}}explanation/{{{self.ns.gco}}}CharacterString"
                    )
                    self.assertIsNotNone(measure_explanation)
                    self.assertEqual(measure_explanation.text, expected_measure['explanation'])

                    measure_pass = measure_result.find(
                        f"{{{self.ns.gmd}}}pass/{{{self.ns.gco}}}Boolean"
                    )
                    self.assertIsNotNone(measure_pass)
                    self.assertEqual(measure_pass.text, str(expected_measure['pass']).lower())

    def test_data_quality_lineage(self):
        if 'lineage' in self.record_attributes['resource']:
            lineage = self.test_response.find(
                f"{{{self.ns.gmd}}}dataQualityInfo/{{{self.ns.gmd}}}DQ_DataQuality/{{{self.ns.gmd}}}lineage/"
                f"{{{self.ns.gmd}}}LI_Lineage/{{{self.ns.gmd}}}statement/{{{self.ns.gco}}}CharacterString"
            )
            self.assertIsNotNone(lineage)
            self.assertEqual(lineage.text, self.record_attributes['resource']['lineage'])

    # Route test

    def test_record_xml_response(self):
        response = self.client.get(
            f"/standards/iso-19115/{self.configuration}",
            base_url='http://localhost:9000'
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.mimetype, 'text/xml')
        self.assertEqual(response.data, self.test_document)
