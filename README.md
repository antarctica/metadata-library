# BAS Metadata Library

Python library for generating metadata records.

## Purpose

This library is designed to assist in generating metadata records for the discovery of datasets, services and related
resources. As a library, this project is intended to be used as a dependency within other tools and services, to 
avoid the need to duplicate the implementation of complex and verbose metadata standards.

This library is built around the needs of the British Antarctic Survey and NERC (UK) Polar Data Centre. This means only
standards, and elements of these standards, used by BAS or the UK PDC are supported. However, additions that would 
enable this library to be useful to other organisations and use-case are welcome as contributions providing they do not
add significant complexity or maintenance.

### Supported standards

| Standard                                                    | Implementation                                              | Library Namespace                               | Introduced In                                                                                    |
| ----------------------------------------------------------- | ----------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [ISO 19115:2003](https://www.iso.org/standard/26020.html)   | [ISO 19139:2007](https://www.iso.org/standard/32557.html)   | `bas_metadata_library.standards.iso_19115_1_v1` | [#46](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues/46) |
| [ISO 19115-2:2009](https://www.iso.org/standard/39229.html) | [ISO 19139-2:2012](https://www.iso.org/standard/57104.html) | `bas_metadata_library.standards.iso_19115_2_v1` | [#50](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues/50) |

**Note:** In this library, the *ISO 19115:2003* standard is referred to as *ISO-19115-1* (`iso_19115_1_v1`) for 
consistency with *ISO 19115-2:2009* (referred to as *ISO-19115-2*, `iso_19115_2_v1`). In the future, the 
[ISO 19115-1:2014](https://www.iso.org/standard/53798.html) standard will be referred to as *ISO-19115-3*.

### Supported profiles

| Standard | Profile  | Implementation  | Library Namespace | Introduced In |
| -------- | -------- | --------------- | ----------------- | ------------- |
| -        | -        | -               | -                 | -             |

**Note:** Support for profiles has been temporarily removed to allow underlying standards to be implemented more 
easily, and to wait until stable profiles for UK PDC Discovery metadata have been developed and approved. 

### Supported configuration versions

| Standard         | Profile | Configuration Version                                                                                                 | Status     | Notes                                         |
| ---------------- | ------- | --------------------------------------------------------------------------------------------------------------------- | ---------- | --------------------------------------------- |
| ISO 19115:2003   | -       | [`v1`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v1.json) | Deprecated | Stable version to be replaced by `v2`         |
| ISO 19115:2003   | -       | [`v2`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-1-v2.json) | Alpha      | New version under development to replace `v1` |
| ISO 19115-2:2009 | -       | [`v1`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v1.json) | Deprecated | Stable version to be replaced by `v2`         |
| ISO 19115-2:2009 | -       | [`v2`](https://metadata-standards.data.bas.ac.uk/bas-metadata-generator-configuration-schemas/v2/iso-19115-2-v2.json) | Alpha      | New version under development to replace `v1` |

## Installation

This package can be installed using Pip from [PyPi](https://pypi.org/project/bas-metadata-library):

```
$ pip install bas-metadata-library
```

## Usage

To generate an ISO 19115 metadata record and return it as an XML document:

```python
from datetime import date
from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV2, MetadataRecord

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
configuration = MetadataRecordConfigV2(**minimal_record_config)
record = MetadataRecord(configuration=configuration)
document = record.generate_xml_document()

# output document
print(document)
```

Where `metadata_configs.record` is a Python dictionary implementing the relevant schema for each standard, documented 
in the [BAS Metadata Standards](https://metadata-standards.data.bas.ac.uk) project.

To reverse this process and convert a XML record into a configuration object:

```python
from bas_metadata_library.standards.iso_19115_2 import MetadataRecord

with open(f"minimal-record.xml") as record_file:
    record_data = record_file.read()

record = MetadataRecord(record=record_data)
configuration = record.make_config()
minimal_record_config = configuration.config

# output configuration
print(minimal_record_config)
```

### HTML entities

Do not include HTML entities in input to this generator, as they will be double escaped by [Lxml](https://lxml.de), the
underlying XML processing library used by this project. Instead, literal characters should be used (e.g. `>`), which 
will be escaped as needed automatically. This applies to any unicode character, such as accents (e.g. `å`) and 
symbols (e.g. `µ`).

E.g. If `&gt;`, the HTML entity for `>` (greater than), were used as input, it would be escaped again to `&amp;gt;` 
which will not be valid output. 

### Linking transfer options and formats

To support generating a table of download options for a resource (such as [1]), this library uses a 'distribution 
option' concept to group related formats and transfer option elements in [Record Configurations](#configuration-classes). 

In ISO these elements are independent of each other, with no formal mechanism to associate formats and transfer options. 
As this library seeks to be fully reversible between a configuration object and XML, this information would be lost 
once records are encoded as XML.

To avoid this, this library uses the ID attribute available in both format and transfer option elements with values 
can be used when decoding XML to reconstruct these associations. This functionality should be fully transparent to the
user, except for these auto-generated IDs being present in records.

See the [Automatic transfer option / format IDs](#automatic-transfer-option--format-ids) section for more details.

**Note:** Do not modify these IDs, as this will break this functionality.

[1]

| Format     | Size   | Download Link                |
| ---------- | ------ | ---------------------------- |
| CSV        | 68 kB  | [Link](https://example.com/) |
| GeoPackage | 1.2 MB | [Link](https://example.com/) |

## Implementation

This library is implemented in Python and consists of a set of classes used to generate XML metadata records from a 
configuration object, or to generate a configuration object from an XML record. 

### Metadata Record classes

Each [supported Standard](#supported-standards) and [Supported Profile](#supported-profiles) is implemented as a module 
under `bas_metadata_library.standards` (where profiles are implemented as modules under their respective standard).

For each, classes inherited from these parent classes are defined:

* `Namespaces`
* `MetadataRecord`
* `MetadataRecordConfig`

The `namespaces` class is a set of mappings between XML namespaces, their shorthand aliases and their definitions XSDs.

The `MetadataRecord` class represents a metadata record and defines the Root [Element](#element-classes). This class 
provides methods to generate an XML document for example.

The `MetadataRecordConfig` class represents the [Configuration](#configuration-classes) used to define values within a 
`MetadataRecord`, either for new records, or derived from existing records. This class provides methods to validate the 
configuration used in a record for example.

### Element classes

Each supported element, in each [supported standard](#supported-standards), inherit and use the `MetadataRecordElement`
class to:

* encode configuration values into an XML fragment of at least one element
* decode an XML fragment into one or more configuration values

Specifically, at least two methods are implemented:

* `make_element()` which builds an XML element using values from a configuration object
* `make_config()` which uses typically XPath expressions to build a configuration object from XML

These methods may be simple (if encoding or decoding a simple free text value for example), or quite complex through 
the use of sub-elements (which themselves may contain sub-elements as needed).

### Configuration classes

The configuration of each metadata record is held in a Python dictionary, within a `MetadataRecordConfig` class. This
class includes methods to validate its configuration against a relevant [Configuration Schema](#configuration-schemas).

Configuration classes are defined at the root of each standard or profile, alongside its root
[Metadata Element](#element-classes) and XML namespaces.

A configuration class will exist for each supported configuration schema with methods to convert from one version to
another.

### Configuration schemas

Allowed configuration values for each [supported Standard](#supported-standards) and
[Supported Profile](#supported-profiles) are described by a [JSON Schema](https://json-schema.org). These configuration 
schemas include which configuration properties are required, and in some cases, allowed values for these properties.

Configuration schemas are stored as JSON files in the `bas_metadata_library.standards_schemas` module and loaded as 
resource files from within this package. Schemas are also made available externally through the BAS Metadata Standards 
website, [metadata-standards.data.bas.ac.uk](https://metadata-standards.data.bas.ac.uk), to allow:

1. other applications to ensure their output will be compatible with this library but that can't, or don't want to, 
   use this library
2. to allow schema inheritance/extension where used for standards that inherit from other standards (such as profiles)

Configuration schemas a versioned (e.g. `v1`, `v2`) to allow for backwards incompatible changes to be made.

#### Source and distribution schemas

Standards and profiles usually inherit from other standards and profiles. In order to prevent this creating huge 
duplication within configuration schemas, inheritance is used to incorporate a base schema and extend it as needed. For 
example, the ISO 19115-2 standard extends, and therefore incorporates the configuration schema for, ISO 19115-1.

JSON Schema references and identifier properties are used to implement this, using URIs within the BAS Metadata 
Standards website. Unfortunately, this creates a problem when developing these schemas, as if Schema B relies on Schema 
A, using its published identifier as a reference, the published instance of the schema will be used (i.e. the remote 
schema will be downloaded when Schema B is validated). If Schema A is being developed, and is not ready to be 
republished, there is a difference between the local and remote schemas used, creating unreliable tests for example.

To avoid this problem, a set of *source* schemas are used which use references to avoid duplication, from which a set 
of *distribution* schemas are generated. These distribution schemas inline any references contained in their source 
counterpart. These distribution schemas are therefore self-contained and can be updated locally without any 
dependencies on remote sources. Distribution schemas are used by [Configuration Classes](#configuration-classes) and 
published to the BAS Metadata Standards website, they are located in the `bas_metadata_library.schemas.dist` module.

When editing configuration schemas, you should edit the source schemas, located in the 
`bas_metadata_library.schemas.src` module, then run the 
[regenerate distribution schemas](#generating-configuration-schemas) using an internal command line utility. 

JSON Schema's can be developed using [jsonschemavalidator.net](https://www.jsonschemavalidator.net).

### Adding a new standard

To add a new standard:

1. create a new module under `bas_metadata_library.standards`, e.g. `bas_metadata_library.standards.foo_v1/__init__.py`
2. in this module, overload the `Namespaces`, `MetadataRecordConfig` and `MetadataRecord` classes as needed
3. create a suitable metadata configuration JSON schema in `bas_metadata_library.standards_schemas/`
   e.g. `bas_metadata_library.standards_schemas/foo_v1/configuration-schema.json`
4. add a script line to the `publish-schemas-stage` and `publish-schemas-prod` jobs in `.gitlab-ci.yml`, to publish 
   the configuration schema within the BAS Metadata Standards website
5. define a series of test configurations (e.g. minimal, typical and complete) for generating test records in
   `tests/resources/configs/` e.g. `tests/resources/configs/foo_v1_standard.py`
6. update the inbuilt Flask application in `app.py` with a route for generating test records for the new standard
7. use the inbuilt Flask application to generate the test records and save to `tests/resources/records/`
8. add relevant [tests](#testing) with methods to test each metadata element class and test records

### Adding a new element to an existing standard

...
### Automatic transfer option / format IDs

ID attributes are automatically added to `gmd:MD_Format` and `gmd:MD_DigitalTransferOptions` elements in order to 
reconstruct related formats and transfer options (see the 
[Linking transfer options and formats](#linking-transfer-options-and-formats) section for more information).

When a record is encoded, ID values are generated by hashing a JSON encoded string of the distribution object. This 
ID is used as a shared base between the format and transfer option, with `-fmt` appended for the format and `-tfo` 
for the transfer option.

When a record is decoded, ID values are extracted (stripping the `-fmt`/`-tfo` suffixes) to index and then match up 
format and transfer options back into distribution options. Any format and transfer options without an ID value, or 
without a corresponding match, are added as partial distribution options.

As a worked example for encoding a (simplified) distribution object such as:

```python
do = {
   'format': 'csv',
   'transfer_option': {
      'size': '40',
      'url': 'https://example.com/foo.csv'
   }
}
```

Becomes:

```
'{"format":"csv","transfer_option":{"size":40,"url":"https://example.com/foo.csv"}}'
```

When encoded as a JSON encoded string, which when hashed becomes:

```
16b7b5df78a664b15d69feda7ccc7caed501f341
```

The ID value added to the `gmd:MD_Format` element would be:

```xml
<gmd:MD_Format id="16b7b5df78a664b15d69feda7ccc7caed501f341-fmt">
```

And for the `gmd:MD_DigitalTransferOptions` element:

```xml
<gmd:MD_DigitalTransferOptions id="16b7b5df78a664b15d69feda7ccc7caed501f341-tfo">
```

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
$ docker compose run terraform
# setup terraform
$ terraform init
# apply changes
$ terraform validate
$ terraform fmt
$ terraform apply
# exit container
$ exit
$ docker compose down
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

This API is developed as a Python library. A bundled Flask application is used to simulate its usage, act as
framework for running tests etc., and provide utility methods for generating schemas etc.

### Development environment

Git, Docker and Docker Compose are required to set up a local development environment of this application.

If you have access to the [BAS GitLab instance](https://gitlab.data.bas.ac.uk), you can clone the project and pull 
Docker images from the BAS GitLab instance and BAS Docker Registry. 

```shell
$ git clone https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator.git
$ cd metadata-generator
$ docker login docker-registry.data.bas.ac.uk
$ docker compose pull
```

Otherwise, you will need to build the Docker image locally.

```shell
$ git clone https://github.com/antarctica/metadata-library.git
$ cd metadata-library
$ docker compose build
```

To run the application using the Flask development server (which reloads automatically if source files are changed):

```shell
$ docker compose up
```

To run other commands against the Flask application (such as [Integration tests](#integration-tests)):

```shell
# in a separate terminal to `docker compose up`
$ docker compose run app flask [command]
# E.g.
$ docker compose run app flask test
# List all available commands
$ docker compose run app flask
```

### Code Style

PEP-8 style and formatting guidelines must be used for this project, with the exception of the 80 character line limit.

[Black](https://github.com/psf/black) is used to ensure compliance, configured in `pyproject.toml`.

Black can be [integrated](https://black.readthedocs.io/en/stable/editor_integration.html#pycharm-intellij-idea) with a
range of editors, such as PyCharm, to perform formatting automatically.

To apply formatting manually:

```shell
$ docker compose run app black bas_metadata_library/
```

To check compliance manually:

```shell
$ docker compose run app black --check bas_metadata_library/
```

Checks are ran automatically in [Continuous Integration](#continuous-integration).

### Dependencies

Python dependencies for this project are managed with [Poetry](https://python-poetry.org) in `pyproject.toml`.

Non-code files, such as static files, can also be included in the [Python package](#python-package) using the
`include` key in `pyproject.toml`.

#### Adding new dependencies

To add a new (development) dependency:

```shell
$ docker compose run app ash
$ poetry add [dependency] (--dev)
```

Then rebuild the development container, and if you can, push to GitLab:

```shell
$ docker compose build app
$ docker compose push app
```

#### Updating dependencies

```shell
$ docker compose run app ash
$ poetry update
```

Then rebuild the development container, and if you can, push to GitLab:

```shell
$ docker compose build app
$ docker compose push app
```

### Static security scanning

To ensure the security of this API, source code is checked against [Bandit](https://github.com/PyCQA/bandit) for issues
such as not sanitising user inputs or using weak cryptography.

**Warning:** Bandit is a static analysis tool and can't check for issues that are only be detectable when running the
application. As with all security tools, Bandit is an aid for spotting common mistakes, not a guarantee of secure code.

Through [Continuous Integration](#continuous-integration), each commit is tested.

To check locally:

```shell
$ docker compose run app bandit -r .
```

### Editor support

#### PyCharm

A run/debug configuration, *App*, is included in the project.

### Generating configuration schemas

To generate [distribution schemas from source schemas](#source-and-distribution-schemas), a custom Flask CLI command,
`generate-schemas` is available. The [`jsonref`](https://jsonref.readthedocs.io/en/latest/) library is used to resolve
any references in source schemas and write the output as distribution schemas, replacing any existing output.

```shell
# start Flask application:
$ docker compose up
# then in a separate terminal:
$ docker compose run app flask generate-schemas
```

To configure this command, (e.g. to add a new schema for a new standard/profile), adjust the `schemas` list in the 
`generate_schemas` method in `manage.py`. This list should contain dictionaries with keys for the common name of the 
schema (based on the common file name of the schema JSON file), and whether the source schema should be resolved or 
simply copied. This should be true by default, and is only relevant to schemas that do not contain any references, as
this will cause an error if resolved.

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
$ docker compose run app pytest --random-order
```

To run tests manually using PyCharm, use the included *App (Tests)* run/debug configuration.

Tests are ran automatically in [Continuous Integration](#continuous-integration).

### Capturing static test records

To capture static test records, which verify complete records are assembled correctly, a custom Flask CLI command,
`capture-test-records` is available. This requires the Flask application to first be running. The Requests library is
used to make requests against the Flask app save responses to a relevant directory in `tests/resources/records`.

```shell
# start Flask application:
$ docker compose up
# then in a separate terminal:
$ docker compose run app flask capture-test-records
```

It is intended that this command will update pre-existing static records, with differences captured in version control
and reviewed manually to ensure they are correct.

### Test coverage

[pytest-cov](https://pypi.org/project/pytest-cov/) is used to measure test coverage.

To prevent noise, `.coveragerc` is used to omit empty `__init__.py` files from reports.

To measure coverage manually:

```shell
$ docker compose run app pytest --random-order --cov=bas_metadata_library --cov-fail-under=100 --cov-report=html .
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

© UK Research and Innovation (UKRI), 2019 - 2021, British Antarctic Survey.

You may use and re-use this software and associated documentation files free of charge in any format or medium, under
the terms of the Open Government Licence v3.0.

You may obtain a copy of the Open Government Licence at http://www.nationalarchives.gov.uk/doc/open-government-licence/
