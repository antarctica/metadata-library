from flask import Flask, Response, jsonify

from bas_metadata_library.standards.iso_19115_v1 import (
    MetadataRecordConfig as ISO19115MetadataRecordConfig,
    MetadataRecord as ISO19115MetadataRecord,
)
from bas_metadata_library.standards.iso_19115_v1.profiles.inspire_v1_3 import (
    MetadataRecordConfig as ISO19115InspireMetadataRecordConfig,
)
from bas_metadata_library.standards.iso_19115_v1.profiles.uk_pdc_discovery_v1 import (
    MetadataRecordConfig as ISO19115UKPDCDiscoveryMetadataRecordConfig,
)

from tests.resources.configs.iso19115_v1_standard import configs_all as iso19115_v1_standard_configs
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

    @app.route("/standards/iso-19115/<configuration>")
    def standard_iso_19115_v1(configuration: str):
        if configuration not in iso19115_v1_standard_configs.keys():
            return KeyError(
                f"Invalid configuration, valid options: " f"[{', '.join(list(iso19115_v1_standard_configs.keys()))}]"
            )

        configuration_object = iso19115_v1_standard_configs[configuration]
        if configuration == "inspire-minimal":
            configuration = ISO19115InspireMetadataRecordConfig(**configuration_object)
        elif configuration == "uk-pdc-discovery-minimal":
            configuration = ISO19115UKPDCDiscoveryMetadataRecordConfig(**configuration_object)
        else:
            configuration = ISO19115MetadataRecordConfig(**configuration_object)
        record = ISO19115MetadataRecord(configuration)

        return Response(record.generate_xml_document(), mimetype="text/xml")

    return app
