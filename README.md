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

| Standard                                             | Implementation                                       | Library Namespace                             | Introduced In                                                                                    |
| ---------------------------------------------------- | ---------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [ISO 19115](https://www.iso.org/standard/26020.html) | [ISO 19139](https://www.iso.org/standard/32557.html) | `bas_metadata_library.standards.iso_19115_v1` | [#46](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues/46) |

### Supported profiles

| Standard  | Profile                                    | Implementation                                                               | Library Namespace                                                          | Introduced In                                                                                    |
| --------- | ------------------------------------------ | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| ISO 19115 | [EU Inspire](https://inspire.ec.europa.eu) | [UK Gemini](https://www.agi.org.uk/agi-groups/standards-committee/uk-gemini) | `bas_metadata_library.standards.iso_19115_v1.profiles.inspire_v1_3`        | [#40](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues/40) |
| ISO 19115 | UK Polar Data Centre Discovery Metadata    | -                                                                            | `bas_metadata_library.standards.iso_19115_v1.profiles.uk_pdc_discovery_v1` | [#45](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues/45) |

## Installation

This package can be installed using Pip from [PyPi](https://pypi.org/project/bas-metadata-library):

```
$ pip install bas-metadata-library
```

## Usage

To generate an ISO 19115 metadata record and return it as an XML document:

```python
import metadata_configs

from bas_metadata_library.standards.iso_19115_v1 import MetadataRecordConfig as ISO19115MetadataRecordConfig, \
    MetadataRecord as ISO19115MetadataRecord

configuration_object = metadata_config.record
configuration = ISO19115MetadataRecordConfig(**configuration_object)

record = ISO19115MetadataRecord(configuration)
document = record.generate_xml_document()

# output document
print(document)
```

Where `metadata_configs.record` is a Python dictionary implementing the BAS metadata generic schema, documented in the
[BAS Metadata Standards](https://metadata-standards.data.bas.ac.uk) project.

### HTML entities

Do not include HTML entities in input to this generator, as it will be douple escaped by [Lxml](https://lxml.de), the 
underlying XML processing library.

This means `&gt;`, the HTML entity for `>`, will be escaped again to `&amp;gt;` which will not be correctly 
interpreted when decoded. Instead the literal character should be used (e.g. `>`), which Lxml will escape if needed.

This applies to any unicode character, such as accents (e.g. `å`) and symbols (e.g. `µ`).

## Implementation

This library consists of a set of base classes for generating XML based metadata records from a configuration object.

Each [supported standard](#supported-standards) implements these classes to generate each supported element within the 
standard, using values, or computed values, from the configuration object.

The configuration object is a python dict, the properties and values of which, including if they are required or 
controlled, are defined and validated by a [JSON Schema](https://json-schema.org).

The class for each metadata standard will validate the configuration object against the relevant JSON schema, create a 
XML tree of elements, and exporting the tree as an XML document. XML is generated using [lxml](https://lxml.de).

See the [development](#development) section for the [base classes](#library-base-classes) used across all standards and 
how to [add a new standard](#adding-a-new-standard).

## Setup

```shell
$ git clone https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator.git
$ cd metadata-generator
```

### Local development

Docker and Docker Compose are required to setup a local development environment of this application.

#### Local development - Docker Compose

If you have access to the [BAS GitLab instance](https://gitlab.data.bas.ac.uk), you can pull the application Docker 
image from the BAS Docker Registry. Otherwise you will need to build the Docker image locally.

```shell
# If you have access to gitlab.data.bas.ac.uk
$ docker login docker-registry.data.bas.ac.uk
$ docker-compose pull
# If you don't have access
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

### Staging and production

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

#### Teraform remote state

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

### Library base classes

The `bas_metadata_library` module defines a series of modules for each standard (in `bas_metadata_library.standards`) 
as well  as *base* classes used across all standards, that providing common functionality. See existing standards for 
how these are used.

### Configuration schemas

This library accepts a 'configuration' for each metadata record. This contains values for elements, or values that are 
used to compute values. For example, a *title* element would use a value taken directly from the record configuration.

To ensure all required configuration attributes are included, and where relevant that their values are allowed, this
configuration is validated against a schema. This schema uses the [JSON Schema](https://json-schema.org) standard.

These schemas are made available externally through the BAS Metadata Standards website 
[metadata-standards.data.bas.ac.uk](https://metadata-standards.data.bas.ac.uk). This to allow:
 
1. other applications that wish to ensure their output will be compatible with this library, but that do not or cannot 
  use this library themselves (i.e. if they don't use Python)
2. to allow schema inheritance/extension where used for standards that inherit from other standards (such as profiles)

A custom Flask CLI command, `output-config-schemas`, is used to generate these schema files from the various standards 
supported by this project. It will create JSON files for each configuration schema in `build/config_schemas`. These are
then uploaded to the Metadata Standards website through [Continuous Deployment](#continuous-deployment).

**Note:** The build directory, and schema's it contains, is ignored in this repository. Outputted schemas are 
considered ephemeral and should be trivial to recreate from modules in this library. The module versions of schemas act 
as the source of truth as they are used for performing validation.

### Adding a new standard

To add a new standard:

1. create a new module in `bas_metadata_library.standards` - e.g. `bas_metadata_library.standards.foo/__init__.py`
2. in this module overload the `Namespaces`, `MetadataRecordConfig` and `MetadataRecord` classes as needed, ensuring 
   to include a suitable schema property in `MetadataRecordConfig`
3. define a series of test configurations (e.g. minimal, typical and complete) for generating test records in 
   `tests/config.py`
4. update the inbuilt Flask application in `app.py` with a route for generating test records for the new standard
5. use the inbuilt Flask application to generate the test records and save to `tests/resources/records/[standard]`
6. add relevant [Integration tests](#integration-tests) with methods to test each metadata element class and that the
   generated record matches the test records saved in `tests/resources/records/[standard]`

### Code Style

PEP-8 style and formatting guidelines must be used for this project, with the exception of the 80 character line limit.

[Flake8](http://flake8.pycqa.org/) is used to ensure compliance, and is ran on each commit through 
[Continuous Integration](#continuous-integration).

To check compliance locally:

```shell
$ docker-compose run app flake8 . --ignore=E501
```

### Dependencies

Python dependencies should be defined using Pip through the `requirements.txt` file. The Docker image is configured to
install these dependencies into the application image for consistency across different environments. Dependencies should
be periodically reviewed and updated as new versions are released.

To add a new dependency:

```shell
$ docker-compose run app ash
$ pip install [dependency]==
# this will display a list of available versions, add the latest to `requirements.txt`
$ exit
$ docker-compose down
$ docker-compose build
```

If you have access to the BAS GitLab instance, push the rebuilt Docker image to the BAS Docker Registry:

```shell
$ docker login docker-registry.data.bas.ac.uk
$ docker-compose push
```

### Dependency vulnerability scanning

To ensure the security of this API, all dependencies are checked against 
[Snyk](https://app.snyk.io/org/antarctica/project/xxx/history) for vulnerabilities. 

**Warning:** Snyk relies on known vulnerabilities and can't check for issues that are not in it's database. As with all 
security tools, Snyk is an aid for spotting common mistakes, not a guarantee of secure code.

Some vulnerabilities have been ignored in this project, see `.snyk` for definitions and the 
[Dependency exceptions](#dependency-vulnerability-exceptions) section for more information.

Through [Continuous Integration](#continuous-integration), on each commit current dependencies are tested and a snapshot
uploaded to Snyk. This snapshot is then monitored for vulnerabilities.

#### Dependency vulnerability exceptions

This project contains known vulnerabilities that have been ignored for a specific reason.

* [Py-Yaml `yaml.load()` function allows Arbitrary Code Execution](https://snyk.io/vuln/SNYK-PYTHON-PYYAML-42159)
    * currently no known or planned resolution
    * indirect dependency, required through the `bandit` package
    * severity is rated *high*
    * risk judged to be *low* as we don't use the Yaml module in this application
    * ignored for 1 year for re-review

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

### Debugging

To debug using PyCharm:

* *Run* -> *Edit Configurations*
* *Add New Configuration* -> *Python*

In *Configuration* tab:

* Script path: `[absolute path to project]/manage.py`
* Python interpreter: *Project interpreter* (*app* service in project Docker Compose)
* Working directory: `[absolute path to project]`
* Path mappings: `[absolute path to project]=/usr/src/app`

## Testing

### Integration tests

This project uses integration tests to ensure features work as expected and to guard against regressions and 
vulnerabilities.

Tests are written to create metadata records based on a series of configurations defined in `tests/config.py`. These
define 'minimal' to 'complete' test records, intended to test different ways a standard can be used, both for 
individual elements and whole records.

Test case methods are used to test individual elements. Comparisons against static records are used to test whole 
records.

The Python [UnitTest](https://docs.python.org/3/library/unittest.html) library is used for running tests using Flask's 
test framework. Test cases are defined in files within `tests/` and are automatically loaded when using the 
`test` Flask CLI command.

Tests are automatically ran on each commit through [Continuous Integration](#continuous-integration).

To run tests manually:

```shell
$ docker-compose run -e FLASK_ENV=testing app flask test --test-runner text
```

#### Capturing static test records

To capture static test records, which verify how records are assembled correctly, a custom Flask CLI command,
`capture-test-records` is available. This requires the Flask application to first be running. The Requests library is
used to make requests against application routes and save the response to a relevant directory in 
`tests/resources/records`.

```shell
# start Flask application
$ docker-compose up
# in a separate terminal
$ docker-compose run app flask capture-test-records
```

It is intended that this command will update pre-existing static records, with differences captured in version control
and reviewed manually to ensure they are correct.

#### PyCharm support

To run tests using PyCharm:

* *Run* -> *Edit Configurations*
* *Add New Configuration* -> *Python Tests* -> *Unittests*

In *Configuration* tab:

* Script path: `[absolute path to project]/tests`
* Python interpreter: *Project interpreter* (*app* service in project Docker Compose)
* Working directory: `[absolute path to project]`
* Path mappings: `[absolute path to project]=/usr/src/app`

**Note:** This configuration can be also be used to debug tests (by choosing *debug* instead of *run*).

#### JUnit support

To run integration tests to produce a JUnit compatible file, test-results.xml:

```
$ docker-compose run -e FLASK_ENV=testing app flask test --test-runner junit
```

### Continuous Integration

All commits will trigger a Continuous Integration process using GitLab's CI/CD platform, configured in `.gitlab-ci.yml`.

This process will run the application [Integration tests](#integration-tests).

Pip dependencies are also [checked and monitored for vulnerabilities](#dependency-vulnerability-scanning).

## Distribution
 
Both source and binary versions of the package are build using [SetupTools](https://setuptools.readthedocs.io), which 
can then be published to the [Python package index](https://pypi.org/project/bas-metadata-library/) for use in other 
applications. Package settings are defined in `setup.py`.

This project is built and published to PyPi automatically through [Continuous Deployment](#continuous-deployment).

To build the source and binary artifact's for this project manually:

```shell
$ docker-compose run app ash
# build package to /build, /dist and /bas-metadata-library.egg-info
$ python setup.py sdist bdist_wheel
$ exit
$ docker-compose down
```

To publish built artifact's for this project manually to [PyPi testing](https://test.pypi.org):

```shell
$ docker-compose run app ash
$ python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# project then available at: https://test.pypi.org/project/bas-metadata-library/
$ exit
$ docker-compose down
```

To publish manually to [PyPi](https://pypi.org):

```shell
$ docker-compose run app ash
$ python -m twine upload --repository-url https://pypi.org/legacy/ dist/*
# project then available at: https://pypi.org/project/bas-metadata-library/
$ exit
$ docker-compose down
```

### Continuous Deployment

A Continuous Deployment process using GitLab's CI/CD platform is configured in `.gitlab-ci.yml`. This will:

* build the source and binary artifact's for this project
* publish built artifact's for this project to the relevant PyPi repository
* publish the [JSON Schemas](#configuration-schemas) for this libraries internal configuration format

On commits to the *master* branch:

* changes will be deployed to [PyPi testing](https://test.pypi.org)
* configuration schemas will be published to the 
  [Metadata Standards testing](https://metadata-standards-testing.data.bas.ac.uk) website

On tagged commits:

* changes will be deployed to [PyPi](https://pypi.org)
* configuration schemas will be published to the [Metadata Standards](https://metadata-standards.data.bas.ac.uk) 
  website

## Release procedure

### At release

1. create a `release` branch
2. bump version in `setup.py` as per SemVer
3. close release in `CHANGELOG.md`
4. push changes, merge the `release` branch into `master` and tag with version

The project will be built and published to PyPi automatically through [Continuous Deployment](#continuous-deployment).

## Feedback

The maintainer of this project is the BAS Web & Applications Team, they can be contacted at: 
[servicedesk@bas.ac.uk](mailto:servicedesk@bas.ac.uk).

## Issue tracking

This project uses issue tracking, see the 
[Issue tracker](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/issues) for more 
information.

**Note:** Read & write access to this issue tracker is restricted. Contact the project maintainer to request access.

## License

© UK Research and Innovation (UKRI), 2019, British Antarctic Survey.

You may use and re-use this software and associated documentation files free of charge in any format or medium, under 
the terms of the Open Government Licence v3.0.

You may obtain a copy of the Open Government Licence at http://www.nationalarchives.gov.uk/doc/open-government-licence/
