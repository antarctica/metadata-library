from flask import Flask, Response, jsonify

from bas_metadata_library.standards.iso_19115_1 import (
    MetadataRecordConfigV1 as ISO19115_1_MetadataRecordConfigV1,
    MetadataRecordConfigV2 as ISO19115_1_MetadataRecordConfigV2,
    MetadataRecord as ISO19115_1_MetadataRecord,
)
from bas_metadata_library.standards.iso_19115_2 import (
    MetadataRecordConfigV1 as ISO19115_2_MetadataRecordConfigV1,
    MetadataRecordConfigV2 as ISO19115_2_MetadataRecordConfigV2,
    MetadataRecord as ISO19115_2_MetadataRecord,
)
from bas_metadata_library.standards.iec_pas_61174_0_v1 import (
    MetadataRecordConfigV1 as IECPAS61174_0_MetadataRecordConfigV1,
    MetadataRecord as IECPAS61174_0_MetadataRecord,
)

from tests.resources.configs.iso19115_1_standard import (
    configs_v1_all as iso19115_1_standard_configs_v1,
    configs_v2_all as iso19115_1_standard_configs_v2,
    configs_all as iso19115_1_standard_configs_all,
)
from tests.resources.configs.iso19115_2_standard import (
    configs_v1_all as iso19115_2_standard_configs_v1,
    configs_v2_all as iso19115_2_standard_configs_v2,
    configs_all as iso19115_2_standard_configs_all,
)

from tests.resources.configs.iec_pas_61174_0_standard import configs_v1 as iec_pas_61174_0_standard_configs_v1

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
    def standard_iso_19115_1(configuration: str):
        if configuration in iso19115_1_standard_configs_v1:
            configuration_object = iso19115_1_standard_configs_v1[configuration]
            configuration = ISO19115_1_MetadataRecordConfigV1(**configuration_object)
            configuration = configuration.convert_to_v2_configuration()
            record = ISO19115_1_MetadataRecord(configuration)
            return Response(record.generate_xml_document(), mimetype="text/xml")

        if configuration in iso19115_1_standard_configs_v2:
            configuration_object = iso19115_1_standard_configs_v2[configuration]
            configuration = ISO19115_1_MetadataRecordConfigV2(**configuration_object)
            record = ISO19115_1_MetadataRecord(configuration)
            return Response(record.generate_xml_document(), mimetype="text/xml")

        return KeyError(
            f"Invalid configuration, valid options: " f"[{', '.join(list(iso19115_1_standard_configs_all.keys()))}]"
        )

    @app.route("/standards/iso-19115-2/<configuration>")
    def standard_iso_19115_2(configuration: str):
        if configuration in iso19115_2_standard_configs_v1:
            configuration_object = iso19115_2_standard_configs_v1[configuration]
            configuration = ISO19115_2_MetadataRecordConfigV1(**configuration_object)
            configuration = configuration.convert_to_v2_configuration()
            record = ISO19115_2_MetadataRecord(configuration)
            return Response(record.generate_xml_document(), mimetype="text/xml")

        if configuration in iso19115_2_standard_configs_v2:
            configuration_object = iso19115_2_standard_configs_v2[configuration]
            configuration = ISO19115_2_MetadataRecordConfigV2(**configuration_object)
            record = ISO19115_2_MetadataRecord(configuration)
            return Response(record.generate_xml_document(), mimetype="text/xml")

        return KeyError(
            f"Invalid configuration, valid options: " f"[{', '.join(list(iso19115_2_standard_configs_all.keys()))}]"
        )

    @app.route("/standards/iec-pas-61174-0/<configuration>")
    def standard_ice_pas_61174_0(configuration: str):
        if configuration in iec_pas_61174_0_standard_configs_v1:
            configuration_object = iec_pas_61174_0_standard_configs_v1[configuration]
            configuration = IECPAS61174_0_MetadataRecordConfigV1(**configuration_object)
            record = IECPAS61174_0_MetadataRecord(configuration)
            return Response(record.generate_xml_document(), mimetype="text/xml")

        return KeyError(
            f"Invalid configuration, valid options: " f"[{', '.join(list(iso19115_2_standard_configs_all.keys()))}]"
        )

    return app
