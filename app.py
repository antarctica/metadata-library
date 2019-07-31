from flask import Flask, Response, jsonify

from bas_metadata_library.standards.iso_19115_v1 import MetadataRecordConfig as ISO19115MetadataRecordConfig, \
    MetadataRecord as ISO19115MetadataRecord

from tests import config


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return jsonify({'meta': 'root endpoint for Metadata Generator internal app'})

    @app.route('/standards/iso-19115/<configuration>')
    def standard_iso_19115(configuration: str):
        if configuration == 'minimal':
            configuration_object = config.iso_19115_v1_minimal_record
        elif configuration == 'minimal-required-doi-citation':
            configuration_object = config.iso_19115_v1_minimal_record_with_required_doi_citation
        elif configuration == 'base-simple':
            configuration_object = config.iso_19115_v1_base_simple_record
        elif configuration == 'base-complex':
            configuration_object = config.iso_19115_v1_base_complex_record
        elif configuration == 'complete':
            configuration_object = config.iso_19115_v1_complete_record
        elif configuration == 'gemini-complete':
            configuration_object = config.iso_19115_v1_gemini_complete_record
        else:
            return KeyError('Invalid configuration, valid options: [minimal, minimal-required-doi-citation, '
                            'base-simple, base-complex, complete, gemini-complete]')

        configuration = ISO19115MetadataRecordConfig(**configuration_object)
        record = ISO19115MetadataRecord(configuration)

        return Response(record.generate_xml_document(), mimetype='text/xml')

    return app
