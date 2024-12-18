from __future__ import annotations

import json
from hashlib import sha1
from pathlib import Path
from shutil import copy
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from flask import Flask, Response, current_app, jsonify
from flask.testing import FlaskClient
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
from bas_metadata_library.standards.iso_19115_0 import (
    MetadataRecord as ISO19115_0_MetadataRecord,
)
from bas_metadata_library.standards.iso_19115_0 import (
    MetadataRecordConfigV4 as ISO19115_0_MetadataRecordConfigV4,
)
from bas_metadata_library.standards.iso_19115_2 import (
    MetadataRecord as ISO19115_2_MetadataRecord,
)
from bas_metadata_library.standards.iso_19115_2 import (
    MetadataRecordConfigV4 as ISO19115_2_MetadataRecordConfigV4,
)
from tests.resources.configs.iec_pas_61174_0_standard import configs_v1 as iec_pas_61174_0_standard_configs_v1
from tests.resources.configs.iec_pas_61174_1_standard import configs_v1 as iec_pas_61174_1_standard_configs_v1
from tests.resources.configs.iso19115_0_standard import (
    configs_v4_all as iso19115_0_standard_configs_v4,
)
from tests.resources.configs.iso19115_2_standard import (
    configs_v4_all as iso19115_2_standard_configs_v4,
)
from tests.resources.configs.magic_discovery_profile import configs_v1_all as magic_discovery_profile_configs_v1
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
        return Response(
            f"Invalid configuration, valid options: " f"[{', '.join(list(test_metadata_standard_configs.keys()))}]"
        )


def _generate_record_iso_19115_0(config_label: str) -> Response:
    if config_label in iso19115_0_standard_configs_v4:
        configuration_object = iso19115_0_standard_configs_v4[config_label]
        configuration = ISO19115_0_MetadataRecordConfigV4(**configuration_object)
        record = ISO19115_0_MetadataRecord(configuration)
        return Response(record.generate_xml_document(), mimetype="text/xml")

    return Response(f"Invalid configuration, valid options: [{', '.join(list(iso19115_0_standard_configs_v4.keys()))}]")


def _generate_record_iso_19115_2(config_label: str) -> Response:
    if config_label in iso19115_2_standard_configs_v4:
        configuration_object = iso19115_2_standard_configs_v4[config_label]
        configuration = ISO19115_2_MetadataRecordConfigV4(**configuration_object)
        record = ISO19115_2_MetadataRecord(configuration)
        return Response(record.generate_xml_document(), mimetype="text/xml")

    return Response(f"Invalid configuration, valid options: [{', '.join(list(iso19115_2_standard_configs_v4.keys()))}]")


def _generate_record_magic_discovery(config_label: str) -> Response:
    if config_label in magic_discovery_profile_configs_v1:
        configuration_object = magic_discovery_profile_configs_v1[config_label]
        configuration = ISO19115_2_MetadataRecordConfigV4(**configuration_object)
        record = ISO19115_2_MetadataRecord(configuration)
        return Response(record.generate_xml_document(), mimetype="text/xml")

    return Response(
        f"Invalid configuration, valid options: [{', '.join(list(magic_discovery_profile_configs_v1.keys()))}]"
    )


def _generate_record_ice_pas_61174_0(config_label: str) -> Response:
    """Generate a record from a configuration using the IEC PAS 61174-0 standard."""
    if config_label in iec_pas_61174_0_standard_configs_v1:
        configuration_object = iec_pas_61174_0_standard_configs_v1[config_label]
        config_label = IECPAS61174_0_MetadataRecordConfigV1(**configuration_object)
        record = IECPAS61174_0_MetadataRecord(config_label)
        return Response(record.generate_xml_document(), mimetype="text/xml")

    return Response(
        f"Invalid configuration, valid options: " f"[{', '.join(list(iec_pas_61174_0_standard_configs_v1.keys()))}]"
    )


def _generate_record_ice_pas_61174_1(config_label: str) -> Response:
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
    """
    Generate distribution schemas without references to any external resources.

    Schemas within a standard typically share common elements, to avoid repeating these elements, we can use references
    between different files/schemas. This doesn't work for unpublished schemas (as their references won't resolve) so
    we inline them.

    For the ISO 19115 schemas, which have essentially identical schemas, we simply copy the `definitions` and
    `properties` members of the ISO 19115_0 schema to the ISO 19115_2 schema. This avoids a large amount of redundant
    inlining but is more fragile and specific to that standard.

    Note: The ISO 19115 V3 schemas do not use copy to prevent any accidental changes to a published schema.
    """
    schemas = [
        {"id": "iec_pas_61174_0_v1", "resolve": False},
        {"id": "iec_pas_61174_1_v1", "resolve": True},
        {"id": "iso_19115_0_v4", "copy": False},
        {"id": "iso_19115_2_v4", "copy": True},
        {"id": "magic_discovery_v1", "copy": False},
    ]
    copy_properties = ["definitions", "type", "required", "additionalProperties", "properties"]

    for schema in schemas:
        print(f"Generating schema for [{schema['id']}]")
        src_schema_path = Path(f"./src/bas_metadata_library/schemas/src/{schema['id']}.json")
        dest_schema_path = Path(f"./src/bas_metadata_library/schemas/dist/{schema['id']}.json")
        dest_schema_path.parent.mkdir(exist_ok=True, parents=True)
        with src_schema_path.open() as src_schema_file, dest_schema_path.open(mode="w") as dist_schema_file:
            src_schema_data = json.load(src_schema_file)
            dist_schema_data = src_schema_data

            if schema.get("resolve"):
                dist_schema_data = JsonRef.replace_refs(
                    src_schema_data, base_uri=f"file://{src_schema_path.absolute()!s}"
                )

            if schema.get("copy"):
                copy_schema_name = src_schema_data["allOf"][0]["$ref"]
                copy_schema_path = Path(f"./src/bas_metadata_library/schemas/src/{copy_schema_name}")
                with copy_schema_path.open() as copy_schema_file:
                    copy_schema_data = json.load(copy_schema_file)
                for prop in copy_properties:
                    dist_schema_data[prop] = copy_schema_data[prop]
                del src_schema_data["allOf"]

            json.dump(dist_schema_data, dist_schema_file, indent=4)
        # add newline to file (for compatibility with pre-commit hook)
        with dest_schema_path.open(mode="a") as dist_schema_file:
            dist_schema_file.write("\n")


def _capture_json_test_config(standard_profile: str, config_name: str, config: dict, parameters: dict) -> None:
    print(f"Saving JSON encoding of '{standard_profile}/{config_name}' test configuration")
    configuration: MetadataRecordConfig = parameters["config_class"](**config)
    json_config_path = Path(f"./tests/resources/configs/{standard_profile}/{config_name}.json")
    json_config_path.parent.mkdir(exist_ok=True, parents=True)
    configuration.dump(file=json_config_path)
    # add newline to file (for compatibility with pre-commit hook)
    with json_config_path.open(mode="a") as json_config_file:
        json_config_file.write("\n")


def _capture_json_test_configs() -> None:
    standards = {
        "test-standard": [
            {
                "configs": test_metadata_standard_configs,
                "config_class": TestStandardMetadataRecordConfig,
            }
        ],
        "iso-19115-0": [
            {
                "configs": iso19115_0_standard_configs_v4,
                "config_class": ISO19115_0_MetadataRecordConfigV4,
            },
        ],
        "iso-19115-2": [
            {
                "configs": iso19115_2_standard_configs_v4,
                "config_class": ISO19115_2_MetadataRecordConfigV4,
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
    profiles = {
        "magic-discovery-profile": [
            {
                "configs": magic_discovery_profile_configs_v1,
                "config_class": ISO19115_2_MetadataRecordConfigV4,
            }
        ],
    }

    for standard_profile, parameter_sets in {**standards, **profiles}.items():
        for parameters in parameter_sets:
            for config_name, config in parameters["configs"].items():
                _capture_json_test_config(
                    standard_profile=standard_profile, config_name=config_name, config=config, parameters=parameters
                )


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


def _capture_test_record(internal_client: FlaskClient, kind: str, standard_profile_name: str, config_name: str) -> None:
    print(f"saving record for '{kind}/{standard_profile_name}/{config_name}'")

    response = internal_client.get(f"http://localhost:5000/{kind}/{standard_profile_name}/{config_name}")
    if response.status_code != 200:
        msg = f"Failed to generate response for '{kind}/{standard_profile_name}/{config_name}'"
        raise RuntimeError(msg)

    response_file_path = Path(f"./tests/resources/records/{standard_profile_name}/{config_name}-record.xml")
    response_file_path.parent.mkdir(parents=True, exist_ok=True)
    with response_file_path.open(mode="w") as response_file:
        response_file.write(response.data.decode())


def _capture_test_records() -> None:
    standards = {
        "test-standard": {"configurations": list(test_metadata_standard_configs.keys())},
        "iso-19115-0": {"configurations": list(iso19115_0_standard_configs_v4.keys())},
        "iso-19115-2": {"configurations": list(iso19115_2_standard_configs_v4.keys())},
        "iec-pas-61174-0": {"configurations": list(iec_pas_61174_0_standard_configs_v1.keys())},
        "iec-pas-61174-1": {"configurations": list(iec_pas_61174_1_standard_configs_v1.keys())},
    }
    profiles = {
        "magic-discovery": {"configurations": list(magic_discovery_profile_configs_v1.keys())},
    }

    internal_client = current_app.test_client()

    for standard, options in standards.items():
        for config in options["configurations"]:
            _capture_test_record(
                internal_client=internal_client, kind="standards", standard_profile_name=standard, config_name=config
            )
    for profile, options in profiles.items():
        for config in options["configurations"]:
            _capture_test_record(
                internal_client=internal_client, kind="profiles", standard_profile_name=profile, config_name=config
            )

    # Capture RTZP files separately for IEC PAS 61174 standard
    rtz_0_config = IECPAS61174_0_MetadataRecordConfigV1(**iec_pas_61174_0_standard_configs_v1["minimal_v1"])
    rtz_0_record = IECPAS61174_0_MetadataRecord(configuration=rtz_0_config)
    rtz_1_config = IECPAS61174_1_MetadataRecordConfigV1(**iec_pas_61174_1_standard_configs_v1["minimal_v1"])
    rtz_1_record = IECPAS61174_1_MetadataRecord(configuration=rtz_1_config)
    rtzp_records = {"iec-pas-61174-0": rtz_0_record, "iec-pas-61174-1": rtz_1_record}
    for rtzp_standard, rtzp_record in rtzp_records.items():
        _update_rtzp_artefact_if_changed(rtzp_standard=rtzp_standard, rtzp_record=rtzp_record)


def create_app() -> Flask:  # noqa: C901
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

    @app.route("/standards/iso-19115-0/<configuration>")
    def standard_iso_19115_0(configuration: str) -> Response:
        """Generate a record from a configuration using the ISO 19115 standard."""
        return _generate_record_iso_19115_0(config_label=configuration)

    @app.route("/standards/iso-19115-2/<configuration>")
    def standard_iso_19115_2(configuration: str) -> Response:
        """Generate a record from a configuration using the ISO 19115-2 standard."""
        return _generate_record_iso_19115_2(config_label=configuration)

    @app.route("/standards/iec-pas-61174-0/<configuration>")
    def standard_ice_pas_61174_0(configuration: str) -> Response:
        """Generate a record from a configuration using the IEC PAS 61174-0 standard."""
        return _generate_record_ice_pas_61174_0(configuration)

    @app.route("/standards/iec-pas-61174-1/<configuration>")
    def standard_ice_pas_61174_1(configuration: str) -> Response:
        """Generate a record from a configuration using the IEC PAS 61174-1 standard."""
        return _generate_record_ice_pas_61174_1(configuration)

    @app.route("/profiles/magic-discovery/<configuration>")
    def profile_magic_discovery_v1(configuration: str) -> Response:
        """Generate a record from a configuration using the MAGIC Discovery Profile for ISO 19115-2."""
        return _generate_record_magic_discovery(config_label=configuration)

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
