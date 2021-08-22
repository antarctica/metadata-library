import os
import json

import requests
import jsonref

from pathlib import Path

from jsonref import JsonRef

from app import create_app

from tests.resources.configs.iso19115_1_v1_standard import configs_all as iso19115_1_v1_standard_configs
from tests.resources.configs.iso19115_2_v1_standard import configs_all as iso19115_2_v1_standard_configs
from tests.resources.configs.test_metadata_standard import configs_all as test_metadata_standard_configs

app = create_app()


@app.cli.command()
def capture_test_records():
    """Capture records for use in tests."""
    standards = {
        "test-standard": {"version": "v1", "configurations": list(test_metadata_standard_configs.keys())},
        "iso-19115-1": {"version": "v1", "configurations": list(iso19115_1_v1_standard_configs.keys())},
        "iso-19115-2": {"version": "v1", "configurations": list(iso19115_2_v1_standard_configs.keys())},
    }
    for standard, options in standards.items():
        for config in options["configurations"]:
            print(f"saving record for 'standards/{standard}/{config}'")
            response = requests.get(f"http://host.docker.internal:9000/standards/{standard}/{config}")
            response.raise_for_status()

            response_file_path = Path(f"./tests/resources/records/{standard}-{options['version']}/{config}-record.xml")
            with open(response_file_path, mode="w") as response_file:
                response_file.write(response.text)


@app.cli.command()
def generate_schemas():
    """Inline JSON Schema references in configuration schemas"""
    schemas = [{"id": "iso_19115_1_v1", "resolve": False}, {"id": "iso_19115_2_v1", "resolve": True}]

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
