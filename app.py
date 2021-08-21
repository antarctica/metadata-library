from flask import Flask, Response, jsonify

from bas_metadata_library.standards.iso_19115_1_v1 import (
    MetadataRecordConfig as ISO19115_1_MetadataRecordConfig,
    MetadataRecord as ISO19115_1_MetadataRecord,
)
from bas_metadata_library.standards.iso_19115_2_v1 import (
    MetadataRecordConfig as ISO19115_2_MetadataRecordConfig,
    MetadataRecord as ISO19115_2_MetadataRecord,
)

from tests.resources.configs.iso19115_1_v1_standard import configs_all as iso19115_1_v1_standard_configs
from tests.resources.configs.iso19115_2_v1_standard import configs_all as iso19115_2_v1_standard_configs
from tests.resources.configs.test_metadata_standard import configs_all as test_metadata_standard_configs
from tests.standards.test_standard import (
    MetadataRecordConfig as TestStandardMetadataRecordConfig,
    MetadataRecord as TestStandardMetadataRecord,
)


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return jsonify({"meta": "Root endpoint for Metadata Generator internal API"})

    @app.route("/standards/test-standard/<configuration>")
    def standard_test_standard_v1(configuration: str):
        if configuration not in test_metadata_standard_configs.keys():
            return KeyError(
                f"Invalid configuration, valid options: " f"[{', '.join(list(test_metadata_standard_configs.keys()))}]"
            )

        configuration_object = test_metadata_standard_configs[configuration]
        configuration = TestStandardMetadataRecordConfig(**configuration_object)
        record = TestStandardMetadataRecord(configuration)

        return Response(record.generate_xml_document(), mimetype="text/xml")

    @app.route("/standards/iso-19115-1/<configuration>")
    def standard_iso_19115_1_v1(configuration: str):
        if configuration not in iso19115_1_v1_standard_configs.keys():
            return KeyError(
                f"Invalid configuration, valid options: " f"[{', '.join(list(iso19115_1_v1_standard_configs.keys()))}]"
            )

        configuration_object = iso19115_1_v1_standard_configs[configuration]
        configuration = ISO19115_1_MetadataRecordConfig(**configuration_object)
        record = ISO19115_1_MetadataRecord(configuration)

        return Response(record.generate_xml_document(), mimetype="text/xml")

    @app.route("/standards/iso-19115-2/<configuration>")
    def standard_iso_19115_2_v1(configuration: str):
        if configuration not in iso19115_2_v1_standard_configs.keys():
            return KeyError(
                f"Invalid configuration, valid options: " f"[{', '.join(list(iso19115_2_v1_standard_configs.keys()))}]"
            )

        configuration_object = iso19115_2_v1_standard_configs[configuration]
        configuration = ISO19115_2_MetadataRecordConfig(**configuration_object)
        record = ISO19115_2_MetadataRecord(configuration)

        return Response(record.generate_xml_document(), mimetype="text/xml")

    return app
