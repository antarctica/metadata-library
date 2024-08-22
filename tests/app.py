
from __future__ import annotations

import json
from hashlib import sha1
from pathlib import Path
from shutil import copy
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from flask import Flask, Response, current_app, jsonify
from jsonref import JsonRef

from bas_metadata_library import MetadataRecordConfig
from bas_metadata_library.standards.iec_pas_61174_0_v1 import (
    MetadataRecord as IECPAS61174_0_MetadataRecord,
)
from bas_metadata_library.standards.iec_pas_61174_0_v1 import (
    MetadataRecordConfigV1 as IECPAS61174_0_MetadataRecordConfigV1,
)
from bas_metadata_library.standards.iec_pas_61174_1_v1 import (
    MetadataRecord as IECPAS61174_1_MetadataRecord,
)
from bas_metadata_library.standards.iec_pas_61174_1_v1 import (
    MetadataRecordConfigV1 as IECPAS61174_1_MetadataRecordConfigV1,
)
from bas_metadata_library.standards.iso_19115_1 import (
    MetadataRecord as ISO19115_1_MetadataRecord,
)
from bas_metadata_library.standards.iso_19115_1 import (
    MetadataRecordConfigV2 as ISO19115_1_MetadataRecordConfigV2,
)
from bas_metadata_library.standards.iso_19115_1 import (
    MetadataRecordConfigV3 as ISO19115_1_MetadataRecordConfigV3,
)
from bas_metadata_library.standards.iso_19115_2 import (
    MetadataRecord as ISO19115_2_MetadataRecord,
)
from bas_metadata_library.standards.iso_19115_2 import (
    MetadataRecordConfigV2 as ISO19115_2_MetadataRecordConfigV2,
)
from bas_metadata_library.standards.iso_19115_2 import (
    MetadataRecordConfigV3 as ISO19115_2_MetadataRecordConfigV3,
)
from tests.resources.configs.iec_pas_61174_0_standard import configs_v1 as iec_pas_61174_0_standard_configs_v1
from tests.resources.configs.iec_pas_61174_1_standard import configs_v1 as iec_pas_61174_1_standard_configs_v1
from tests.resources.configs.iso19115_1_standard import (
    configs_v2_all as iso19115_1_standard_configs_v2,
)
from tests.resources.configs.iso19115_1_standard import (
    configs_v3_all as iso19115_1_standard_configs_v3,
)
from tests.resources.configs.iso19115_2_standard import (
    configs_v2_all as iso19115_2_standard_configs_v2,
)
from tests.resources.configs.iso19115_2_standard import (
    configs_v3_all as iso19115_2_standard_configs_v3,
)
from tests.resources.configs.test_metadata_standard import configs_all as test_metadata_standard_configs
from tests.standards.test_standard import (
    MetadataRecord as TestStandardMetadataRecord,
)
from tests.standards.test_standard import (
    MetadataRecordConfig as TestStandardMetadataRecordConfig,
)


def _generate_record_test_standard_v1(config_label: str) -> Response:
    try:
        config = test_metadata_standard_configs[config_label]
        record_config = TestStandardMetadataRecordConfig(**config)
        record = TestStandardMetadataRecord(record_config)
        return Response(record.generate_xml_document(), mimetype="text/xml")
    except KeyError:
        return Response(f"Invalid configuration, valid options: " f"[{', '.join(list(test_metadata_standard_configs.keys()))}]")


def _generate_record_iso_19115_1(config_label: str) -> Response:
    if config_label in iso19115_1_standard_configs_v2:
        configuration_object = iso19115_1_standard_configs_v2[config_label]
        configuration_v2 = ISO19115_1_MetadataRecordConfigV2(**configuration_object)
        configuration = ISO19115_1_MetadataRecordConfigV3()
        configuration.upgrade_from_v2_config(v2_config=configuration_v2)
        record = ISO19115_1_MetadataRecord(configuration)
        return Response(record.generate_xml_document(), mimetype="text/xml")

    if config_label in iso19115_1_standard_configs_v3:
        configuration_object = iso19115_1_standard_configs_v3[config_label]
        configuration = ISO19115_1_MetadataRecordConfigV3(**configuration_object)
        record = ISO19115_1_MetadataRecord(configuration)
        return Response(record.generate_xml_document(), mimetype="text/xml")

    return Response(
        f"Invalid configuration, valid options: "
        f"[{', '.join(list(iso19115_1_standard_configs_v2.keys()) + list(iso19115_1_standard_configs_v3.keys()))}]"
    )


def _generate_record_iso_19115_2(config_label: str) -> Response:
    if config_label in iso19115_2_standard_configs_v2:
        configuration_object = iso19115_2_standard_configs_v2[config_label]
        configuration_v2 = ISO19115_2_MetadataRecordConfigV2(**configuration_object)
        configuration = ISO19115_2_MetadataRecordConfigV3()
        configuration.upgrade_from_v2_config(v2_config=configuration_v2)
        record = ISO19115_2_MetadataRecord(configuration)
        return Response(record.generate_xml_document(), mimetype="text/xml")

    if config_label in iso19115_2_standard_configs_v3:
        configuration_object = iso19115_2_standard_configs_v3[config_label]
        configuration = ISO19115_2_MetadataRecordConfigV3(**configuration_object)
        record = ISO19115_2_MetadataRecord(configuration)
        return Response(record.generate_xml_document(), mimetype="text/xml")

    return Response(
        f"Invalid configuration, valid options: "
        f"[{', '.join(list(iso19115_2_standard_configs_v2.keys()) + list(iso19115_2_standard_configs_v2.keys()))}]"
    )


def _standard_ice_pas_61174_0(config_label: str) -> Response:
    """Generate a record from a configuration using the IEC PAS 61174-0 standard."""
    if config_label in iec_pas_61174_0_standard_configs_v1:
        configuration_object = iec_pas_61174_0_standard_configs_v1[config_label]
        config_label = IECPAS61174_0_MetadataRecordConfigV1(**configuration_object)
        record = IECPAS61174_0_MetadataRecord(config_label)
        return Response(record.generate_xml_document(), mimetype="text/xml")

    return Response(
        f"Invalid configuration, valid options: " f"[{', '.join(list(iec_pas_61174_0_standard_configs_v1.keys()))}]"
    )


def _standard_ice_pas_61174_1(config_label: str) -> Response:
    """Generate a record from a configuration using the IEC PAS 61174-1 standard."""
    if config_label in iec_pas_61174_1_standard_configs_v1:
        configuration_object = iec_pas_61174_1_standard_configs_v1[config_label]
        config_label = IECPAS61174_1_MetadataRecordConfigV1(**configuration_object)
        record = IECPAS61174_1_MetadataRecord(config_label)
        return Response(record.generate_xml_document(), mimetype="text/xml")

    return Response(
        f"Invalid configuration, valid options: " f"[{', '.join(list(iec_pas_61174_1_standard_configs_v1.keys()))}]"
    )


def _generate_schemas() -> None:
    schemas = [
        {"id": "iso_19115_1_v2", "resolve": False},
        {"id": "iso_19115_2_v2", "resolve": True},
        {"id": "iso_19115_1_v3", "resolve": False},
        {"id": "iso_19115_2_v3", "resolve": True},
        {"id": "iec_pas_61174_0_v1", "resolve": False},
        {"id": "iec_pas_61174_1_v1", "resolve": True},
    ]

    for schema in schemas:
        print(f"Generating schema for [{schema['id']}]")
        src_schema_path = Path(f"./src/bas_metadata_library/schemas/src/{schema['id']}.json")
        dest_schema_path = Path(f"./src/bas_metadata_library/schemas/dist/{schema['id']}.json")
        with src_schema_path.open() as src_schema_file, dest_schema_path.open(mode='w') as dist_schema_file:
            src_schema_data = json.load(src_schema_file)
            dist_schema_data = src_schema_data
            if schema["resolve"]:
                dist_schema_data = JsonRef.replace_refs(
                    src_schema_data, base_uri=f"file://{src_schema_path.absolute()!s}"
                )
            json.dump(dist_schema_data, dist_schema_file, indent=4)


def _capture_json_test_configs() -> None:
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


def _update_rtzp_artefact_if_changed(
    rtzp_standard: str, rtzp_record: IECPAS61174_0_MetadataRecord | IECPAS61174_1_MetadataRecord
) -> None:
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
            new_rtzp_hash = sha1(new_rtzp_file.read(new_rtzp_file.namelist()[0])).hexdigest()  # noqa: S324
        with ZipFile(str(new_rtzp_path)) as existing_rtzp_file:
            existing_rtzp_hash = sha1(  # noqa: S324
                existing_rtzp_file.read(existing_rtzp_file.namelist()[0])
            ).hexdigest()

        if new_rtzp_hash != existing_rtzp_hash:
            print(f"saving RTZP archive for 'standards/{rtzp_standard}/minimal-v1'")
            copy(src=new_rtzp_path, dst=existing_rtzp_path)
        else:
            print(f"saving RTZP archive for 'standards/{rtzp_standard}/minimal-v1' - skipped, no change")


def _capture_test_records() -> None:
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

    internal_client = current_app.test_client()

    for standard, options in standards.items():
        for config in options["configurations"]:
            print(f"saving record for 'standards/{standard}/{config}'")

            response = internal_client.get(f"http://localhost:5000/standards/{standard}/{config}")
            if response.status_code != 200:
                msg = f"Failed to generate response for 'standards/{standard}/{config}'"
                raise RuntimeError(msg)

            response_file_path = Path(f"./tests/resources/records/{standard}/{config}-record.xml")
            response_file_path.parent.mkdir(parents=True, exist_ok=True)
            with response_file_path.open(mode="w") as response_file:
                response_file.write(response.data.decode())

    # Capture RTZP files separately for IEC PAS 61174 standard
    rtz_0_config = IECPAS61174_0_MetadataRecordConfigV1(**iec_pas_61174_0_standard_configs_v1["minimal_v1"])
    rtz_0_record = IECPAS61174_0_MetadataRecord(configuration=rtz_0_config)
    rtz_1_config = IECPAS61174_1_MetadataRecordConfigV1(**iec_pas_61174_1_standard_configs_v1["minimal_v1"])
    rtz_1_record = IECPAS61174_1_MetadataRecord(configuration=rtz_1_config)
    rtzp_records = {"iec-pas-61174-0": rtz_0_record, "iec-pas-61174-1": rtz_1_record}
    for rtzp_standard, rtzp_record in rtzp_records.items():
        _update_rtzp_artefact_if_changed(rtzp_standard=rtzp_standard, rtzp_record=rtzp_record)


def create_app() -> Flask:
    """Create internal Flask app."""
    app = Flask(__name__)

    @app.route("/")
    def index() -> Response:
        """Root endpoint."""
        return jsonify({"meta": "Root endpoint for Metadata Library internal API"})

    @app.route("/standards/test-standard/<configuration>")
    def standard_test_standard_v1(configuration: str) -> Response:
        """Generate a record from a configuration using the test standard."""
        return _generate_record_test_standard_v1(config_label=configuration)

    @app.route("/standards/iso-19115-1/<configuration>")
    def standard_iso_19115_1(configuration: str) -> Response:
        """Generate a record from a configuration using the ISO 19115 standard."""
        return _generate_record_iso_19115_1(config_label=configuration)

    @app.route("/standards/iso-19115-2/<configuration>")
    def standard_iso_19115_2(configuration: str) -> Response:
        """Generate a record from a configuration using the ISO 19115-2 standard."""
        return _generate_record_iso_19115_2(config_label=configuration)

    @app.route("/standards/iec-pas-61174-0/<configuration>")
    def standard_ice_pas_61174_0(configuration: str) -> Response:
        """Generate a record from a configuration using the IEC PAS 61174-0 standard."""
        return _standard_ice_pas_61174_0(configuration)

    @app.route("/standards/iec-pas-61174-1/<configuration>")
    def standard_ice_pas_61174_1(configuration: str) -> Response:
        """Generate a record from a configuration using the IEC PAS 61174-1 standard."""
        return _standard_ice_pas_61174_1(configuration)

    @app.cli.command()
    def generate_schemas() -> None:
        """Inline JSON Schema references in configuration schemas."""
        _generate_schemas()

    @app.cli.command()
    def capture_json_test_configs() -> None:
        """Capture JSON encodings of test configurations for use in tests."""
        _capture_json_test_configs()

    @app.cli.command()
    def capture_test_records() -> None:
        """Capture records for use in tests."""
        _capture_test_records()

    return app
