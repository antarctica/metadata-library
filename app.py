from flask import Flask, Response, jsonify

from uk_pdc_metadata_record_generator.standards.iso_19115_v1 import MetadataRecordConfig as ISO19115MetadataRecordConfig, MetadataRecord as ISO19115MetadataRecord

from tests import config


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return jsonify({'meta': 'root endpoint for Metadata Generator internal app'})

    @app.route('/standards/iso-19115')
    def standard_iso_19115():
        configuration = ISO19115MetadataRecordConfig(**config.test_record)
        record = ISO19115MetadataRecord(configuration)

        return Response(record.generate_xml_document(), mimetype='text/xml')

    return app
