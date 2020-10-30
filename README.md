# BAS Metadata Library

Python library for generating metadata records.

## Purpose

This library is designed to assist in generating metadata records for the discovery of datasets. As a library, this 
package is intended to be embedded within other tools and services, to avoid the need to implement 
the complexity and verbosity of specific metadata standards.

This library is built around the needs of the British Antarctic Survey and NERC Polar Data Centre. This means only 
standards, and elements of these standards, used by BAS or the UK PDC are supported. Additions that would enable this
library to be useful to others are welcome as contributions.

### Supported standards

| Standard                                                    | Implementation                                              | Library Namespace                               | Introduced In                                                                                    |
| ----------------------------------------------------------- | ----------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [ISO 19115:2003](https://www.iso.org/standard/26020.html)   | [ISO 19139:2007](https://www.iso.org/standard/32557.html)   | `bas_metadata_library.standards.iso_19115_1_v1` | [#46](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues/46) |
| [ISO 19115-2:2009](https://www.iso.org/standard/39229.html) | [ISO 19139-2:2012](https://www.iso.org/standard/57104.html) | `bas_metadata_library.standards.iso_19115_2_v1` | [#50](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues/50) |

**Note:** In this library *ISO 19115:2003* is referred to as *ISO-19115-1* (`iso_19115_1_v1`) for consistency with 
*ISO 19115-2:2009* (referred to as *ISO-19115-2*, `iso_19115_2_v1`). As ISO have subsequently created 
[ISO 19115-1:2014](https://www.iso.org/standard/53798.html) this creates a conflict/ambiguity. To resolve this 
without making breaking changes, *ISO 19115-1:2014* will be referred to as *ISO-19115-3* when added to this library.

### Supported profiles

| Standard         | Profile                                    | Implementation                                                               | Library Namespace                                                            | Introduced In                                                                                    |
| ---------------- | ------------------------------------------ | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| ISO 19115:2003   | [EU Inspire](https://inspire.ec.europa.eu) | [UK Gemini](https://www.agi.org.uk/agi-groups/standards-committee/uk-gemini) | `bas_metadata_library.standards.iso_19115_1_v1.profiles.inspire_v1_3`        | [#40](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues/40) |
| ISO 19115:2003   | UK Polar Data Centre Discovery Metadata    | -                                                                            | `bas_metadata_library.standards.iso_19115_1_v1.profiles.uk_pdc_discovery_v1` | [#45](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues/45) |
| ISO 19115-2:2009 | [EU Inspire](https://inspire.ec.europa.eu) | [UK Gemini](https://www.agi.org.uk/agi-groups/standards-committee/uk-gemini) | `bas_metadata_library.standards.iso_19115_2_v1.profiles.inspire_v1_3`        | [#40](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues/50) |
| ISO 19115-2:2009 | UK Polar Data Centre Discovery Metadata    | -                                                                            | `bas_metadata_library.standards.iso_19115_2_v1.profiles.uk_pdc_discovery_v1` | [#45](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues/50) |

## Installation

This package can be installed using Pip from [PyPi](https://pypi.org/project/bas-metadata-library):

```
$ pip install bas-metadata-library
```

## Usage

To generate an ISO 19115 metadata record and return it as an XML document:

```python
from datetime import date
from bas_metadata_library.standards.iso_19115_2_v1 import MetadataRecordConfig, MetadataRecord

minimal_record_config = {
    "language": "eng",
    "character_set": "utf-8",
    "hierarchy_level": "dataset",
    "contacts": [{"organisation": {"name": "UK Polar Data Centre"}, "role": ["pointOfContact"]}],
    "date_stamp": date(2018, 10, 18),
    "resource": {
        "title": {"value": "Test Record"},
        "dates": [{"date": date(2018, 1, 1), "date_precision": "year", "date_type": "creation"}],
        "abstract": "Test Record for ISO 19115 metadata standard (no profile) with required properties only.",
        "character_set": "utf-8",
        "language": "eng",
        "topics": ["environment", "climatologyMeteorologyAtmosphere"],
        "extent": {
            "geographic": {
                "bounding_box": {
                    "west_longitude": -45.61521,
                    "east_longitude": -27.04976,
                    "south_latitude": -68.1511,
                    "north_latitude": -54.30761,
                }
            }
        },
    },
}
configuration = MetadataRecordConfig(**minimal_record_config)
record = MetadataRecord(configuration=configuration)
document = record.generate_xml_document()

# output document
print(document)
```

Where `metadata_configs.record` is a Python dictionary implementing the BAS metadata generic schema, documented in the
[BAS Metadata Standards](https://metadata-standards.data.bas.ac.uk) project.

To reverse this process and convert an XML record into a configuration object:

```python
from bas_metadata_library.standards.iso_19115_2_v1 import MetadataRecord

with open(f"minimal-record.xml") as record_file:
    record_data = record_file.read()

record = MetadataRecord(record=record_data)
configuration = record.make_config()
minimal_record_config = configuration.config

# output configuration
print(minimal_record_config)
```

### HTML entities

Do not include HTML entities in input to this generator, as it will be douple escaped by [Lxml](https://lxml.de), the 
underlying XML processing library.

This means `&gt;`, the HTML entity for `>`, will be escaped again to `&amp;gt;` which will not be correctly 
interpreted when decoded. Instead the literal character should be used (e.g. `>`), which Lxml will escape if needed.

This applies to any unicode character, such as accents (e.g. `å`) and symbols (e.g. `µ`).

## Implementation

This library consists of a set of base classes using [lxml](https://lxml.de) for generating XML based metadata records 
from a configuration object, or generating a configuration object from an XML record.

Each [supported standard](#supported-standards) implements these classes for supported elements as per their respective 
standard. Two methods are implemented, `make_element()` builds an XML element using values from a configuration object, 
`make_config()` typically uses XPath expressions to build a configuration object from XML. These element classes are 
combined to generate complete metadata records or configuration objects.

Configuration objects are python dicts, the properties and values of which are defined by, and validated against, a 
[JSON Schema](https://json-schema.org).

See the [development](#development) section for more information on the [base classes](#library-base-classes) used 
across all standards and how to [add a new standard](#adding-a-new-standard).

## Setup

### Terraform

Terraform is used to provision resources required to operate this application in staging and production environments.

These resources allow [Configuration schemas](#configuration-schemas) for each standard to be accessed externally.

Access to the [BAS AWS account](https://gitlab.data.bas.ac.uk/WSF/bas-aws) is needed to provisioning these resources.

**Note:** This provisioning should have already been performed (and applies globally). If changes are made to this 
provisioning it only needs to be applied once.

```shell
# start terraform inside a docker container
$ cd provisioning/terraform
$ docker-compose run terraform
# setup terraform
$ terraform init
# apply changes
$ terraform validate
$ terraform fmt
$ terraform apply
# exit container
$ exit
$ docker-compose down
```

#### Terraform remote state

State information for this project is stored remotely using a 
[Backend](https://www.terraform.io/docs/backends/index.html).

Specifically the [AWS S3](https://www.terraform.io/docs/backends/types/s3.html) backend as part of the 
[BAS Terraform Remote State](https://gitlab.data.bas.ac.uk/WSF/terraform-remote-state) project.

Remote state storage will be automatically initialised when running `terraform init`. Any changes to remote state will
be automatically saved to the remote backend, there is no need to push or pull changes.

##### Remote state authentication

Permission to read and/or write remote state information for this project is restricted to authorised users. Contact
the [BAS Web & Applications Team](mailto:servicedesk@bas.ac.uk) to request access.

See the [BAS Terraform Remote State](https://gitlab.data.bas.ac.uk/WSF/terraform-remote-state) project for how these
permissions to remote state are enforced.

## Development

This API is developed as a Python library. A bundled Flask application is used to simulate its usage and to act as
framework for running tests etc.

```shell
$ git clone https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator.git
$ cd metadata-generator
```

### Development environment

Docker and Docker Compose are required to setup a local development environment of this application.

If you have access to the [BAS GitLab instance](https://gitlab.data.bas.ac.uk), you can pull the application Docker 
image from the BAS Docker Registry. Otherwise you will need to build the Docker image locally.

```shell
# If you have access to gitlab.data.bas.ac.uk:
$ docker login docker-registry.data.bas.ac.uk
$ docker-compose pull
# If you don't have access:
$ docker-compose build
```

To run the application using the Flask development server (which reloads automatically if source files are changed):

```shell
$ docker-compose up
```

To run other commands against the Flask application (such as [Integration tests](#integration-tests)):

```shell
# in a separate terminal to `docker-compose up`
$ docker-compose run app flask [command]
# E.g.
$ docker-compose run app flask test
# List all available commands
$ docker-compose run app flask
```

### Library base classes

The `bas_metadata_library` module defines a series of modules for each standard (in `bas_metadata_library.standards`) 
as well  as *base* classes used across all standards, that providing common functionality. See existing standards for 
how these are used.

### Configuration schemas

This library accepts a 'configuration' for each metadata record. This contains values for elements, or values that are 
used to compute values. For example, a *title* element would use a value taken directly from the record configuration.

To ensure all required configuration attributes are included, and where relevant that their values are allowed, this
configuration is validated against a schema. This schema uses the [JSON Schema](https://json-schema.org) standard.

Configuration schemas are stored as JSON files in `bas_metadata_library.standards_schemas` and loaded as resource files
within this package. Schemas are also made available externally through the BAS Metadata Standards website 
[metadata-standards.data.bas.ac.uk](https://metadata-standards.data.bas.ac.uk) to allow:
 
1. other applications to ensure their output will be compatible with this library, but that can't use this library
2. to allow schema inheritance/extension where used for standards that inherit from other standards (such as profiles)

JSON Schema's can be developed using [jsonschemavalidator.net](https://www.jsonschemavalidator.net).

### Adding a new standard

To add a new standard:

1. create a new module in `bas_metadata_library.standards/` e.g. `bas_metadata_library.standards.foo_v1/__init__.py`
2. in this module, overload the `Namespaces`, `MetadataRecordConfig` and `MetadataRecord` classes as needed
3. create a suitable metadata configuration JSON schema in `bas_metadata_library.standards_schemas/` 
   e.g. `bas_metadata_library.standards_schemas/foo_v1/configuration-schema.json`
4. add a script line to the `publish-schemas-stage` and `publish-schemas-prod` to copy the configuration schema to the
   relevant S3 buckets for external access 
5. define a series of test configurations (e.g. minimal, typical and complete) for generating test records in 
   `tests/resources/configs/` e.g. `tests/resources/configs/foo_v1_standard.py`
6. update the inbuilt Flask application in `app.py` with a route for generating test records for the new standard
7. use the inbuilt Flask application to generate the test records and save to `tests/resources/records/`
8. add relevant [tests](#testing) with methods to test each metadata element class and test records

### Code Style

PEP-8 style and formatting guidelines must be used for this project, with the exception of the 80 character line limit.

[Black](https://github.com/psf/black) is used to ensure compliance, configured in `pyproject.toml`.

Black can be [integrated](https://black.readthedocs.io/en/stable/editor_integration.html#pycharm-intellij-idea) with a 
range of editors, such as PyCharm, to perform formatting automatically.

To apply formatting manually:

```shell
$ docker-compose run app black bas_metadata_library/
```

To check compliance manually:

```shell
$ docker-compose run app black --check bas_metadata_library/
```

Checks are ran automatically in [Continuous Integration](#continuous-integration).

### Dependencies

Python dependencies for this project are managed with [Poetry](https://python-poetry.org) in `pyproject.toml`.

Non-code files, such as static files, can also be included in the [Python package](#python-package) using the
`include` key in `pyproject.toml`.

#### Adding new dependencies

To add a new (development) dependency:

```shell
$ docker-compose run app ash
$ poetry add [dependency] (--dev)
```

Then rebuild the development container, and if you can, push to GitLab:

```shell
$ docker-compose build app
$ docker-compose push app
```

#### Updating dependencies

```shell
$ docker-compose run app ash
$ poetry update
```

Then rebuild the development container, and if you can, push to GitLab:

```shell
$ docker-compose build app
$ docker-compose push app
```

### Static security scanning

To ensure the security of this API, source code is checked against [Bandit](https://github.com/PyCQA/bandit) for issues 
such as not sanitising user inputs or using weak cryptography. 

**Warning:** Bandit is a static analysis tool and can't check for issues that are only be detectable when running the 
application. As with all security tools, Bandit is an aid for spotting common mistakes, not a guarantee of secure code.

Through [Continuous Integration](#continuous-integration), each commit is tested.

To check locally:

```shell
$ docker-compose run app bandit -r .
```

### Editor support

#### PyCharm

A run/debug configuration, *App*, is included in the project.

## Testing

All code in the `bas_metadata_library` module must be covered by tests, defined in `tests/`. This project uses
[PyTest](https://docs.pytest.org/en/latest/) which should be ran in a random order using
[pytest-random-order](https://pypi.org/project/pytest-random-order/).

Tests are written to create metadata records based on a series of configurations defined in `tests/config.py`. These
define 'minimal' to 'complete' test records, intended to test different ways a standard can be used, both for 
individual elements and whole records. These tests are designed to ensure that records are generally well-formed and
that where config options are used the corresponding elements in the metadata record are generated.

As this library does not seek to support all possible elements and variations within each standard, these tests are 
similarly not exhaustive, nor are they a substitute for formal metadata validation.

Test methods are used to test individual elements are formed correctly. Comparisons against static records are used to 
test the structure of whole records.

To run tests manually from the command line:

```shell
$ docker-compose run app pytest --random-order
```

To run tests manually using PyCharm, use the included *App (Tests)* run/debug configuration.

Tests are ran automatically in [Continuous Integration](#continuous-integration).

### Capturing static test records

To capture static test records, which verify complete records are assembled correctly, a custom Flask CLI command,
`capture-test-records` is available. This requires the Flask application to first be running. The Requests library is
used to make requests against the Flask app save responses to a relevant directory in `tests/resources/records`.

```shell
# start Flask application:
$ docker-compose up
# then in a separate terminal:
$ docker-compose run app flask capture-test-records
```

It is intended that this command will update pre-existing static records, with differences captured in version control
and reviewed manually to ensure they are correct.

### Test coverage

[pytest-cov](https://pypi.org/project/pytest-cov/) is used to measure test coverage.

To prevent noise, `.coveragerc` is used to omit empty `__init__.py` files from reports.

To measure coverage manually:

```shell
$ docker-compose run app pytest --random-order --cov=bas_metadata_library --cov-fail-under=100 --cov-report=html .
```

[Continuous Integration](#continuous-integration) will check coverage automatically and fail if less than 100%.

### Continuous Integration

All commits will trigger a Continuous Integration process using GitLab's CI/CD platform, configured in `.gitlab-ci.yml`.

## Deployment

### Python package

This project is distributed as a Python package, hosted in [PyPi](https://pypi.org/project/bas-metadata-library).

Source and binary packages are built and published automatically using
[Poetry](https://python-poetry.org/docs/cli/#publish) in [Continuous Delivery](#continuous-deployment).

Package versions are determined automatically using the `support/python-packaging/parse_version.py` script.

### Continuous Deployment

A Continuous Deployment process using GitLab's CI/CD platform is configured in `.gitlab-ci.yml`.

## Release procedure

For all releases:

1. create a release branch
2. close release in `CHANGELOG.md`
3. push changes, merge the release branch into `master` and tag with version

## Feedback

The maintainer of this project is the BAS Web & Applications Team, they can be contacted at: 
[servicedesk@bas.ac.uk](mailto:servicedesk@bas.ac.uk).

## Issue tracking

This project uses issue tracking, see the 
[Issue tracker](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues) for more 
information.

**Note:** Read & write access to this issue tracker is restricted. Contact the project maintainer to request access.

## License

© UK Research and Innovation (UKRI), 2019 - 2020, British Antarctic Survey.

You may use and re-use this software and associated documentation files free of charge in any format or medium, under 
the terms of the Open Government Licence v3.0.

You may obtain a copy of the Open Government Licence at http://www.nationalarchives.gov.uk/doc/open-government-licence/
