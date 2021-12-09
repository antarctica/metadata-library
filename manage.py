import os
import json

import requests

from pathlib import Path

from jsonref import JsonRef

from app import create_app

from bas_metadata_library.standards.iec_pas_61174_0_v1 import (
    MetadataRecordConfigV1 as IEC_PAS_61174_0_MetadataRecordConfigV1,
    MetadataRecord as IEC_PAS_61174_0_MetadataRecord,
)
from bas_metadata_library.standards.iec_pas_61174_1_v1 import (
    MetadataRecordConfigV1 as IEC_PAS_61174_1_MetadataRecordConfigV1,
    MetadataRecord as IEC_PAS_61174_1_MetadataRecord,
)

from tests.resources.configs.iso19115_1_standard import configs_all as iso19115_1_v1_standard_configs
from tests.resources.configs.iso19115_2_standard import configs_all as iso19115_2_v1_standard_configs
from tests.resources.configs.iec_pas_61174_0_standard import configs_v1 as iec_pas_61174_0_standard_configs
from tests.resources.configs.iec_pas_61174_1_standard import configs_v1 as iec_pas_61174_1_standard_configs
from tests.resources.configs.test_metadata_standard import configs_all as test_metadata_standard_configs

app = create_app()


@app.cli.command()
def capture_test_records():
    """Capture records for use in tests."""
    standards = {
        "test-standard": {"configurations": list(test_metadata_standard_configs.keys())},
        "iso-19115-1": {"configurations": list(iso19115_1_v1_standard_configs.keys())},
        "iso-19115-2": {"configurations": list(iso19115_2_v1_standard_configs.keys())},
        "iec-pas-61174-0": {"configurations": list(iec_pas_61174_0_standard_configs.keys())},
        "iec-pas-61174-1": {"configurations": list(iec_pas_61174_1_standard_configs.keys())},
    }
    for standard, options in standards.items():
        for config in options["configurations"]:
            print(f"saving record for 'standards/{standard}/{config}'")
            response = requests.get(f"http://host.docker.internal:9000/standards/{standard}/{config}")
            response.raise_for_status()

            response_file_path = Path(f"./tests/resources/records/{standard}/{config}-record.xml")
            response_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(response_file_path, mode="w") as response_file:
                response_file.write(response.text)

    # Capture RTZP files separately for IEC PAS 61174 standard

    print(f"saving RTZP archive for 'standards/iec-pas-61174-0/minimal-v1'")
    rtz_config = IEC_PAS_61174_0_MetadataRecordConfigV1(**iec_pas_61174_0_standard_configs["minimal_v1"])
    rtz_record = IEC_PAS_61174_0_MetadataRecord(configuration=rtz_config)
    rtz_record.generate_rtzp_archive(file=Path(f"./tests/resources/records/iec-pas-61174-0/minimal-v1-record.rtzp"))

    print(f"saving RTZP archive for 'standards/iec-pas-61174-1/minimal-v1'")
    rtz_config = IEC_PAS_61174_1_MetadataRecordConfigV1(**iec_pas_61174_1_standard_configs["minimal_v1"])
    rtz_record = IEC_PAS_61174_1_MetadataRecord(configuration=rtz_config)
    rtz_record.generate_rtzp_archive(file=Path(f"./tests/resources/records/iec-pas-61174-1/minimal-v1-record.rtzp"))


@app.cli.command()
def generate_schemas():
    """Inline JSON Schema references in configuration schemas"""
    schemas = [
        {"id": "iso_19115_1_v1", "resolve": False},
        {"id": "iso_19115_2_v1", "resolve": True},
        {"id": "iso_19115_1_v2", "resolve": False},
        {"id": "iso_19115_2_v2", "resolve": True},
        {"id": "iec_pas_61174_0_v1", "resolve": False},
        {"id": "iec_pas_61174_1_v1", "resolve": True},
    ]

    for schema in schemas:
        print(f"Generating schema for [{schema['id']}]")
        src_schema_path = Path(f"./bas_metadata_library/schemas/src/{schema['id']}.json")
        dest_schema_path = Path(f"./bas_metadata_library/schemas/dist/{schema['id']}.json")
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


if "PYCHARM_HOSTED" in os.environ:
    # Exempting Bandit security issue (binding to all network interfaces)
    #
    # All interfaces option used because the network available within the container can vary across providers
    # This is only used when debugging with PyCharm. A standalone web server is used in production.
    app.run(host="0.0.0.0", port=9000, debug=True, use_debugger=False, use_reloader=False)  # nosec
