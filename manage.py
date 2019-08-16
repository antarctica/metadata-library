import os
import sys
import unittest
import json

import requests
import xmlrunner

from pathlib import Path

# noinspection PyPackageRequirements
from click import option, Choice, echo, style

from app import create_app
from bas_metadata_library.standards.iso_19115_v1 import MetadataRecordConfig as ISO19115MetadataRecordConfig
from bas_metadata_library.standards.iso_19115_v1.profiles.inspire_v1_3 import MetadataRecordConfig as \
    ISO19115InspireMetadataRecordConfig

app = create_app()


@app.cli.command()
def capture_test_records():
    """Capture records for use in tests."""
    standards = {
        'iso-19115': {
            'version': 'v1',
            'configurations': [
                'minimal',
                'minimal-required-doi-citation',
                'base-simple',
                'base-complex',
                'complete',
                'inspire-minimal',
                'gemini-complete'
            ]
        }
    }
    for standard, options in standards.items():
        for config in options['configurations']:
            print(f"saving record for 'standards/{standard}/{config}'")
            response = requests.get(f"http://host.docker.internal:9000/standards/{standard}/{config}")
            response.raise_for_status()

            response_file_path = Path(f"./tests/resources/records/{standard}-{options['version']}/{config}-record.xml")
            with open(response_file_path, mode='w') as response_file:
                response_file.write(response.text)


@app.cli.command()
def output_config_schemas():
    """Save configuration schemas as files."""
    iso_19115_v1 = Path('./build/config-schemas/iso-19115-v1')
    iso_19115_v1_profiles = Path.joinpath(iso_19115_v1, 'profiles')
    iso_19115_v1_profiles_inspire = Path.joinpath(iso_19115_v1_profiles, 'inspire-v1_3')

    iso_19115_v1.mkdir(parents=True, exist_ok=True)
    iso_19115_v1_profiles.mkdir(parents=True, exist_ok=True)
    iso_19115_v1_profiles_inspire.mkdir(parents=True, exist_ok=True)

    iso_19115_v1_file_path = Path.joinpath(iso_19115_v1, 'configuration-schema.json')
    with open(iso_19115_v1_file_path, mode='w') as config_schema_file:
        config_schema = ISO19115MetadataRecordConfig()
        json.dump(config_schema.schema, config_schema_file, indent=4)

    iso_19115_v1_inspire_v1_3_file_path = Path.joinpath(iso_19115_v1_profiles_inspire, 'configuration-schema.json')
    with open(iso_19115_v1_inspire_v1_3_file_path, mode='w') as config_schema_file:
        config_schema = ISO19115InspireMetadataRecordConfig()
        json.dump(config_schema.schema, config_schema_file, indent=4)


@app.cli.command()
@option('--test-runner', type=Choice(['text', 'junit']))
def test(test_runner: str = 'text'):
    """Run integration tests."""
    tests = unittest.TestLoader().discover(os.path.join(os.path.dirname(__file__), 'tests'))

    if test_runner == 'text':
        tests_runner = unittest.TextTestRunner(verbosity=2)
        return sys.exit(not tests_runner.run(tests).wasSuccessful())
    elif test_runner == 'junit':
        with open('test-results.xml', 'wb') as output:
            tests_runner = xmlrunner.XMLTestRunner(output=output)
            return sys.exit(not tests_runner.run(tests).wasSuccessful())

    echo(style('Unknown Python unit test runner type', fg='red'), err=True)


if 'PYCHARM_HOSTED' in os.environ:
    # Exempting Bandit security issue (binding to all network interfaces)
    #
    # All interfaces option used because the network available within the container can vary across providers
    # This is only used when debugging with PyCharm. A standalone web server is used in production.
    app.run(host='0.0.0.0', port=9000, debug=True, use_debugger=False, use_reloader=False)  # nosec
