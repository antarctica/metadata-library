import json

from hashlib import sha1
from pathlib import Path
from shutil import copy
from tempfile import TemporaryDirectory
from typing import Union
from zipfile import ZipFile

import requests

from flask import Flask, Response, jsonify
from jsonref import JsonRef

from bas_metadata_library import MetadataRecordConfig
from bas_metadata_library.standards.iso_19115_1 import (
    MetadataRecordConfigV2 as ISO19115_1_MetadataRecordConfigV2,
    MetadataRecordConfigV3 as ISO19115_1_MetadataRecordConfigV3,
    MetadataRecord as ISO19115_1_MetadataRecord,
)
from bas_metadata_library.standards.iso_19115_2 import (
    MetadataRecordConfigV2 as ISO19115_2_MetadataRecordConfigV2,
    MetadataRecordConfigV3 as ISO19115_2_MetadataRecordConfigV3,
    MetadataRecord as ISO19115_2_MetadataRecord,
)
from bas_metadata_library.standards.iec_pas_61174_0_v1 import (
    MetadataRecordConfigV1 as IECPAS61174_0_MetadataRecordConfigV1,
    MetadataRecord as IECPAS61174_0_MetadataRecord,
)
from bas_metadata_library.standards.iec_pas_61174_1_v1 import (
    MetadataRecordConfigV1 as IECPAS61174_1_MetadataRecordConfigV1,
    MetadataRecord as IECPAS61174_1_MetadataRecord,
)

from tests.resources.configs.iso19115_1_standard import (
    configs_v2_all as iso19115_1_standard_configs_v2,
    configs_v3_all as iso19115_1_standard_configs_v3,
)
from tests.resources.configs.iso19115_2_standard import (
    configs_v2_all as iso19115_2_standard_configs_v2,
    configs_v3_all as iso19115_2_standard_configs_v3,
)
from tests.resources.configs.iec_pas_61174_0_standard import configs_v1 as iec_pas_61174_0_standard_configs_v1
from tests.resources.configs.iec_pas_61174_1_standard import configs_v1 as iec_pas_61174_1_standard_configs_v1
from tests.resources.configs.test_metadata_standard import configs_all as test_metadata_standard_configs
from tests.standards.test_standard import (
    MetadataRecordConfig as TestStandardMetadataRecordConfig,
    MetadataRecord as TestStandardMetadataRecord,
)


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return jsonify({"meta": "Root endpoint for Metadata Library internal API"})

    @app.route("/standards/test-standard/<configuration>")
    def standard_test_standard_v1(configuration: str):
        if configuration not in test_metadata_standard_configs.keys():
            return (
                f"Invalid configuration, valid options: " f"[{', '.join(list(test_metadata_standard_configs.keys()))}]"
            )

        configuration_object = test_metadata_standard_configs[configuration]
        configuration = TestStandardMetadataRecordConfig(**configuration_object)

        record = TestStandardMetadataRecord(configuration)

        return Response(record.generate_xml_document(), mimetype="text/xml")

    @app.route("/standards/iso-19115-1/<configuration>")
    def standard_iso_19115_1(configuration: str):
        if configuration in iso19115_1_standard_configs_v2:
            configuration_object = iso19115_1_standard_configs_v2[configuration]
            configuration_v2 = ISO19115_1_MetadataRecordConfigV2(**configuration_object)
            configuration = ISO19115_1_MetadataRecordConfigV3()
            configuration.upgrade_from_v2_config(v2_config=configuration_v2)
            record = ISO19115_1_MetadataRecord(configuration)
            return Response(record.generate_xml_document(), mimetype="text/xml")

        if configuration in iso19115_1_standard_configs_v3:
            configuration_object = iso19115_1_standard_configs_v3[configuration]
            configuration = ISO19115_1_MetadataRecordConfigV3(**configuration_object)
            record = ISO19115_1_MetadataRecord(configuration)
            return Response(record.generate_xml_document(), mimetype="text/xml")

        return (
            f"Invalid configuration, valid options: "
            f"[{', '.join(list(iso19115_1_standard_configs_v2.keys()) + list(iso19115_1_standard_configs_v3.keys()))}]"
        )

    @app.route("/standards/iso-19115-2/<configuration>")
    def standard_iso_19115_2(configuration: str):
        if configuration in iso19115_2_standard_configs_v2:
            configuration_object = iso19115_2_standard_configs_v2[configuration]
            configuration_v2 = ISO19115_2_MetadataRecordConfigV2(**configuration_object)
            configuration = ISO19115_2_MetadataRecordConfigV3()
            configuration.upgrade_from_v2_config(v2_config=configuration_v2)
            record = ISO19115_2_MetadataRecord(configuration)
            return Response(record.generate_xml_document(), mimetype="text/xml")

        if configuration in iso19115_2_standard_configs_v3:
            configuration_object = iso19115_2_standard_configs_v3[configuration]
            configuration = ISO19115_2_MetadataRecordConfigV3(**configuration_object)
            record = ISO19115_2_MetadataRecord(configuration)
            return Response(record.generate_xml_document(), mimetype="text/xml")

        return (
            f"Invalid configuration, valid options: "
            f"[{', '.join(list(iso19115_2_standard_configs_v2.keys()) + list(iso19115_2_standard_configs_v2.keys()))}]"
        )

    @app.route("/standards/iec-pas-61174-0/<configuration>")
    def standard_ice_pas_61174_0(configuration: str):
        if configuration in iec_pas_61174_0_standard_configs_v1:
            configuration_object = iec_pas_61174_0_standard_configs_v1[configuration]
            configuration = IECPAS61174_0_MetadataRecordConfigV1(**configuration_object)
            record = IECPAS61174_0_MetadataRecord(configuration)
            return Response(record.generate_xml_document(), mimetype="text/xml")

        return (
            f"Invalid configuration, valid options: " f"[{', '.join(list(iec_pas_61174_0_standard_configs_v1.keys()))}]"
        )

    @app.route("/standards/iec-pas-61174-1/<configuration>")
    def standard_ice_pas_61174_1(configuration: str):
        if configuration in iec_pas_61174_1_standard_configs_v1:
            configuration_object = iec_pas_61174_1_standard_configs_v1[configuration]
            configuration = IECPAS61174_1_MetadataRecordConfigV1(**configuration_object)
            record = IECPAS61174_1_MetadataRecord(configuration)
            return Response(record.generate_xml_document(), mimetype="text/xml")

        return (
            f"Invalid configuration, valid options: " f"[{', '.join(list(iec_pas_61174_1_standard_configs_v1.keys()))}]"
        )

    @app.cli.command()
    def generate_schemas():
        """Inline JSON Schema references in configuration schemas"""
        schemas = [
            {"id": "iso_19115_1_v2", "resolve": False},
            {"id": "iso_19115_2_v2", "resolve": True},
            {"id": "iec_pas_61174_0_v1", "resolve": False},
            {"id": "iec_pas_61174_1_v1", "resolve": True},
        ]

        for schema in schemas:
            print(f"Generating schema for [{schema['id']}]")
            src_schema_path = Path(f"./src/bas_metadata_library/schemas/src/{schema['id']}.json")
            dest_schema_path = Path(f"./src/bas_metadata_library/schemas/dist/{schema['id']}.json")
            with open(str(src_schema_path), mode="r") as src_schema_file, open(
                str(dest_schema_path), mode="w"
            ) as dist_schema_file:
                src_schema_data = json.load(src_schema_file)
                dist_schema_data = src_schema_data
                if schema["resolve"]:
                    dist_schema_data = JsonRef.replace_refs(
                        src_schema_data, base_uri=f"file://{str(src_schema_path.absolute())}"
                    )
                json.dump(dist_schema_data, dist_schema_file, indent=4)

    @app.cli.command()
    def capture_json_test_configs():
        """Capture JSON encodings of test configurations for use in tests."""
        standards = {
            "test-standard": [
                {
                    "configs": test_metadata_standard_configs,
                    "config_class": TestStandardMetadataRecordConfig,
                }
            ],
            "iso-19115-1": [
                {
                    "configs": iso19115_1_standard_configs_v2,
                    "config_class": ISO19115_1_MetadataRecordConfigV2,
                },
                {
                    "configs": iso19115_1_standard_configs_v3,
                    "config_class": ISO19115_1_MetadataRecordConfigV3,
                },
            ],
            "iso-19115-2": [
                {
                    "configs": iso19115_2_standard_configs_v2,
                    "config_class": ISO19115_2_MetadataRecordConfigV2,
                },
                {
                    "configs": iso19115_2_standard_configs_v3,
                    "config_class": ISO19115_2_MetadataRecordConfigV3,
                },
            ],
            "iec-pas-61174-0": [
                {
                    "configs": iec_pas_61174_0_standard_configs_v1,
                    "config_class": IECPAS61174_0_MetadataRecordConfigV1,
                }
            ],
            "iec-pas-61174-1": [
                {
                    "configs": iec_pas_61174_1_standard_configs_v1,
                    "config_class": IECPAS61174_1_MetadataRecordConfigV1,
                }
            ],
        }
        for standard, parameter_sets in standards.items():
            for parameters in parameter_sets:
                for config_name, config in parameters["configs"].items():
                    print(f"Saving JSON encoding of '{standard}/{config_name}' test configuration")
                    configuration: MetadataRecordConfig = parameters["config_class"](**config)
                    json_config_path = Path(f"./tests/resources/configs/{standard}/{config_name}.json")
                    json_config_path.parent.mkdir(exist_ok=True, parents=True)
                    configuration.dump(file=json_config_path)

    @app.cli.command()
    def capture_test_records():
        """Capture records for use in tests."""
        standards = {
            "test-standard": {"configurations": list(test_metadata_standard_configs.keys())},
            "iso-19115-1": {
                "configurations": list(iso19115_1_standard_configs_v2.keys())
                + list(iso19115_1_standard_configs_v3.keys())
            },
            "iso-19115-2": {
                "configurations": list(iso19115_2_standard_configs_v2.keys())
                + list(iso19115_1_standard_configs_v3.keys())
            },
            "iec-pas-61174-0": {"configurations": list(iec_pas_61174_0_standard_configs_v1.keys())},
            "iec-pas-61174-1": {"configurations": list(iec_pas_61174_1_standard_configs_v1.keys())},
        }
        for standard, options in standards.items():
            for config in options["configurations"]:
                print(f"saving record for 'standards/{standard}/{config}'")
                response = requests.get(f"http://localhost:5000/standards/{standard}/{config}")
                response.raise_for_status()

                response_file_path = Path(f"./tests/resources/records/{standard}/{config}-record.xml")
                response_file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(response_file_path, mode="w") as response_file:
                    response_file.write(response.text)

        # Capture RTZP files separately for IEC PAS 61174 standard
        rtz_0_config = IECPAS61174_0_MetadataRecordConfigV1(**iec_pas_61174_0_standard_configs_v1["minimal_v1"])
        rtz_0_record = IECPAS61174_0_MetadataRecord(configuration=rtz_0_config)
        rtz_1_config = IECPAS61174_1_MetadataRecordConfigV1(**iec_pas_61174_1_standard_configs_v1["minimal_v1"])
        rtz_1_record = IECPAS61174_1_MetadataRecord(configuration=rtz_1_config)
        rtzp_records = {"iec-pas-61174-0": rtz_0_record, "iec-pas-61174-1": rtz_1_record}
        for rtzp_standard, rtzp_record in rtzp_records.items():
            _update_rtzp_artefact_if_changed(rtzp_standard=rtzp_standard, rtzp_record=rtzp_record)

    def _update_rtzp_artefact_if_changed(
        rtzp_standard: str, rtzp_record: Union[IECPAS61174_0_MetadataRecord, IECPAS61174_1_MetadataRecord]
    ):
        """
        Checks whether a RTZP archive created for an IEC PAS 61174 based record differs compared to an earlier archive.

        In essence, this method checks whether the inner RTZ file of a RTZP package has changed, rather than checking
        the package itself.

        This is needed because:
        - RTZP files are binary, so Git can't accurately determine what has changed, or store changes efficiently
        - RTZP files are Zip files, which are non-reproducible by default due to embedded creation dates etc.

        This method is used to prevent updating RTZP test artefacts unless they have changed in terms of their contents.
        The contents of an RTZP file is assumed to only change when the configuration it is based on changes (i.e. when
        a new attribute is added or changed). If these contents have changed, the previous/existing file will be
        replaced with the new file.

        Without this method, capturing or generating test records/artefacts would always result in new RTZP artefacts
        being created, potentially giving the impression they have meaningfully changed - which in most cases would be
        misleading.

        It is assumed by this method that RTZP artefacts contain a single file, specifically the inner RTZ file. This is
        extracted using the `ZipFile.namelist()` method, which returns an index of files within a Zip archive.

        The SHA1 hash algorithm is used as this method is not used in a security related context (i.e. it isn't used for
        hashing passwords etc.)
        """
        with TemporaryDirectory() as tmp_dir_name:
            new_rtzp_path = Path(tmp_dir_name).joinpath("minimal-v1-record.rtzp")
            existing_rtzp_path = Path(f"./tests/resources/records/{rtzp_standard}/minimal-v1-record.rtzp")

            rtzp_record.generate_rtzp_archive(new_rtzp_path)

            with ZipFile(str(new_rtzp_path)) as new_rtzp_file:
                # Bandit B303 warning is exempted as these hashes are not used for any security related purposes
                new_rtzp_hash = sha1(new_rtzp_file.read(new_rtzp_file.namelist()[0])).hexdigest()  # nosec
            with ZipFile(str(new_rtzp_path)) as existing_rtzp_file:
                # Bandit B303 warning is exempted as these hashes are not used for any security related purposes
                existing_rtzp_hash = sha1(
                    existing_rtzp_file.read(existing_rtzp_file.namelist()[0])
                ).hexdigest()  # nosec

            if new_rtzp_hash != existing_rtzp_hash:
                print(f"saving RTZP archive for 'standards/{rtzp_standard}/minimal-v1'")
                copy(src=new_rtzp_path, dst=existing_rtzp_path)
            else:
                print(f"saving RTZP archive for 'standards/{rtzp_standard}/minimal-v1' - skipped, no change")

    return app
