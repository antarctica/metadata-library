import os
import json
from shutil import copy
from typing import Union
from zipfile import ZipFile

import requests

from hashlib import sha1
from tempfile import TemporaryDirectory
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

    rtz_0_config = IEC_PAS_61174_0_MetadataRecordConfigV1(**iec_pas_61174_0_standard_configs["minimal_v1"])
    rtz_0_record = IEC_PAS_61174_0_MetadataRecord(configuration=rtz_0_config)
    rtz_1_config = IEC_PAS_61174_1_MetadataRecordConfigV1(**iec_pas_61174_1_standard_configs["minimal_v1"])
    rtz_1_record = IEC_PAS_61174_1_MetadataRecord(configuration=rtz_1_config)

    rtzp_records = {"iec-pas-61174-0": rtz_0_record, "iec-pas-61174-1": rtz_1_record}

    for rtzp_standard, rtzp_record in rtzp_records.items():
        _update_rtzp_artefact_if_changed(rtzp_standard=rtzp_standard, rtzp_record=rtzp_record)


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


def _update_rtzp_artefact_if_changed(
    rtzp_standard: str, rtzp_record: Union[IEC_PAS_61174_0_MetadataRecord, IEC_PAS_61174_1_MetadataRecord]
):
    """
    Checks whether a RTZP archive created for a IEC PAS 61174 based record differs compared to an earlier archive.

    In essence, this method checks whether the inner RTZ file of a RTZP package has changed, rather than checking the
    package itself.

    This is needed because:
    - RTZP files are binary, meaning Git can't accurately determine what has changed, or store such changes efficiently
    - RTZP files are Zip files, which are non-reproducible by default as they contain attributes such as a creation date

    This method is used to prevent updating RTZP test artefacts unless they have changed in terms of their contents.
    The contents of an RTZP file is assumed to only change when the configuration it is based on changes (i.e. when a
    new attribute is added or changed). If this contents have changed, the previous/existing file will be replaced with
    the new file.

    Without this method, capturing or generating test records/artefacts would always result in new RTZP artefacts being
    created, potentially giving the impression they have meaningfully changed - which in most cases would be misleading.

    It is assumed by this method that RTZP artefacts contain a single file, specifically the inner RTZ file. This is
    extracted using the `ZipFile.namelist()` method, which returns an index of files within a Zip archive.

    The SHA1 hash algorithm is used as this method is not used in a security related context (i.e. it isn't used for
    hashing passwords etc.
    """
    with TemporaryDirectory() as tmpdirname:
        new_rtzp_path = Path(tmpdirname).joinpath("/minimal-v1-record.rtzp")
        existing_rtzp_path = Path(f"./tests/resources/records/{rtzp_standard}/minimal-v1-record.rtzp")

        rtzp_record.generate_rtzp_archive(new_rtzp_path)

        with ZipFile(str(new_rtzp_path)) as new_rtzp_file:
            # Bandit B303 warning is exempted as these hashes are not used for any security related purposes
            new_rtzp_hash = sha1(new_rtzp_file.read(new_rtzp_file.namelist()[0])).hexdigest()  # nosec
        with ZipFile(str(new_rtzp_path)) as existing_rtzp_file:
            # Bandit B303 warning is exempted as these hashes are not used for any security related purposes
            existing_rtzp_hash = sha1(existing_rtzp_file.read(existing_rtzp_file.namelist()[0])).hexdigest()  # nosec

        if new_rtzp_hash != existing_rtzp_hash:
            print(f"saving RTZP archive for 'standards/{rtzp_standard}/minimal-v1'")
            copy(src=new_rtzp_path, dst=existing_rtzp_path)
        else:
            print(f"saving RTZP archive for 'standards/{rtzp_standard}/minimal-v1' - skipped, no change")


if "PYCHARM_HOSTED" in os.environ:
    # Exempting Bandit security issue (binding to all network interfaces)
    #
    # All interfaces option used because the network available within the container can vary across providers
    # This is only used when debugging with PyCharm. A standalone web server is used in production.
    app.run(host="0.0.0.0", port=9000, debug=True, use_debugger=False, use_reloader=False)  # nosec
