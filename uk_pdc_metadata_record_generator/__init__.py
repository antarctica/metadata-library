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



class MetadataRecordElement(object):
    def __init__(self, record: MetadataRecord, attributes: dict):
        self._ns = Namespaces()
        self.record = record
        self.attributes = attributes

    def make_element(self):
        pass


class CodeListElement(MetadataRecordElement):
    def __init__(self, record: MetadataRecord, attributes: dict):
        super().__init__(record, attributes)
        self.element = None
        self.element_code = None
        self.attribute = None

        self.code_list = None
        self.code_list_values = []

    def make_element(self):
        code_list_element = etree.SubElement(self.record, self.element)
        if self.attribute in self.attributes and self.attributes[self.attribute] in self.code_list_values:
            code_list_value = etree.SubElement(code_list_element, self.element_code, attrib={
                'codeList': self.code_list,
                'codeListValue': self.attributes[self.attribute]
            })
            code_list_value.text = self.attributes[self.attribute]


class Language(CodeListElement):
    def __init__(self, record: MetadataRecord, attributes: dict):
        super().__init__(record, attributes)
        self.code_list_values = ['eng']
        self.code_list = 'http://www.loc.gov/standards/iso639-2/php/code_list.php'
        self.element = f"{{{self._ns.gmd}}}language"
        self.element_code = f"{{{self._ns.gmd}}}LanguageCode"
        self.attribute = 'language'


class CharacterSet(CodeListElement):
    def __init__(self, record: MetadataRecord, attributes: dict):
        super().__init__(record, attributes)
        self.code_list_values = ['utf8']
        self.code_list = 'http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/' \
                         'codelist/gmxCodelists.xml#MD_CharacterSetCode'
        self.element = f"{{{self._ns.gmd}}}characterSet"
        self.element_code = f"{{{self._ns.gmd}}}MD_CharacterSetCode"
        self.attribute = 'character_set'



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
