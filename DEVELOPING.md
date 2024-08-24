# BAS Metadata Library - Development Documentation

## Adding a new standard

To add a new standard:

1. create a new module under `bas_metadata_library.standards`, e.g. `bas_metadata_library.standards.foo_v1/__init__.py`
2. in this module, overload the `Namespaces`, `MetadataRecordConfig` and `MetadataRecord` classes as needed
    * version the `MetadataRecordConfig` class, e.g. `MetadataRecordConfigV1`
3. create a suitable metadata configuration JSON schema in `bas_metadata_library.schemas.src`,
   e.g. `bas_metadata_library.schemas.src.foo_v1.json`
4. update the `generate_schemas` method in `app.py` to generate distribution schemas
5. add a script line to the `publish-schemas-stage` and `publish-schemas-prod` jobs in `.gitlab-ci.yml`, to publish
   the distribution schema within the BAS Metadata Standards website
6. define a series of test configurations (e.g. minimal, typical and complete) for generating test records in
   `tests/resources/configs/` e.g. `tests/resources/configs/foo_v1_standard.py`
7. add a route in `app.py` for generating test records for the new standard
8. update the `capture_test_records` method in `app.py` to generate and save test records
9. add relevant [tests](#tests) with methods to test each metadata element class and test records

## Adding a new element to an existing standard

**Note:** These instructions are specific to the ISO 19115 metadata standards family.

1. [amend configuration schema](/README.md#configuration-schemas):
   * new or changed properties should be added to the configuration for the relevant standard (e.g. ISO 19115-1)
   * typically, this involves adding new elements to the `definitions` property and referencing these in the relevant
     parent element (e.g. to the `identification` property)
2. [generate distribution schemas](#generating-configuration-schemas)
3. amend test configs:
   * new or changed properties should be made to the relevant test record configurations in `tests/resources/configs/`
   * there are different levels of configuration, from minimal to complete, which should, where possible, build on
     each other (e.g. the complete record should include all the properties and values of the minimal record)
   * the `minimum` configuration should not be changed, as all mandatory elements are already implemented
   * the `base_simple` configuration should contain elements used most of the time, that use free-text values
   * the `base_complex` configuration should contain elements used most of the time, that use URL or other
     identifier values
   * the `complete` configuration should contain examples of all supported elements, providing this still produces a
     valid record, in order to ensure high test coverage
   * where possible, configurations should be internally consistent, but this can be ignored if needed
   * values used for identifiers and other external references should use the correct form/structure but do not need
     to exist or relate to the resource described by each configuration (i.e. DOIs should be valid URLs but could be
     a DOI for another resource for example)
4. add relevant [element class](/README.md#record-element-classes):
   * new or changed elements should be added to the configuration for the relevant package for each standard
   * for the ISO 19115 family of standards, element classes should be added to the `iso_19115_common` package
   * the exact module to use within this package will depend on the nature of the element being added, but in general,
     elements should be added to the module of their parent element (e.g. `data_identification.py` for elements
     under the `identification` record configuration property), elements used across a range of elements should be
     added to the `common_elements.py` module
   * remember to include references to new element class in the parent element class (in both the `make_element` and
     `make_config` methods)
5. [capture test records](#capturing-test-records)
    * initially this acts as a good way to check new or changed element classes encode configuration properties
      correctly
    * check the git status of these test records to check existing records have changed how you expect (and haven't
      changed things you didn't intend to for example)
6. [capture test JSON configurations](#capturing-test-configurations-as-json)
    * check the git status of these test configs to check they are encoded correctly from Python (i.e. dates)
7. add tests:
    * new test cases should be added, or existing test cases updated, in the relevant module within
      `tests/bas_metadata_library/`
    * for the ISO 19115 family of standards, this should be `test_standard_iso_19115_1.py`, unless the element is only
      part of the ISO 19115-2 standard
    * providing there are enough test configurations to test all the ways a new element can be used (e.g. with a simple
      text string or anchor element for example), adding a test case for each element is typically enough to ensure
      sufficient test coverage
    * where this isn't the case, it's suggested to add one or more 'edge case' test cases to test remaining code paths
      explicitly
8. check [test coverage](#pytest-cov-test-coverage):
    * for missing coverage, consider adding edge case test cases where applicable
    * coverage exemptions should be avoided wherever feasible and all exemptions must be discussed before they are added
    * where exceptions are added, they should be documented as an issue with information on how they will be addressed
      in the longer term
9. update `README.md` examples if common element:
    * this is probably best done before releasing a new version
10. update `CHANGELOG.md`
11. if needed, add name to `authors` property in `pyproject.toml`

## Adding a new config version for an existing standard [WIP]

**Note:** This is typically only needed if breaking changes need to be made to the schema for a configuration, as the
work involved is quite significant.

**Note:** This section is a work in progress whilst developing the ISO 19115 v3 configuration in
[#182](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/182).

**Note:** In these instructions, `v1` refers to the current/previous configuration version. `v2` refers to the new
configuration version.

## Step 1: Add new version

First, create a new configuration version that is identical to the current/previous version, but that sets up the
schema, objects, methods, tests and documentation needed for the new configuration, and to convert between the old
and new configurations.

1. create an issue summarising, and referencing specific issues for, changes to be made in the new schema version
2. copy the current/previous metadata configuration JSON schema from `bas_metadata_library.schemas.src`
   e.g. `bas_metadata_library.schemas.src.foo_v1.json` to `bas_metadata_library.schemas.src.foo_v2.json`
   1. change the version in:
       * the `$id` property
       * the `title` property
       * the `description` property
3. duplicate the configuration classes for the standard in `bas_metadata_library.standards`
    * i.e. in `bas_metadata_library.standards.foo_v1/__init__.py`, copy:
        * `MetadataRecordConfigV1` to `MetadataRecordConfigV2`
4. in the new configuration class, add `upgrade_to_v1_config()` and `downgrade_to_v2_config()` methods
    * the `upgrade_from_v2_config()` method should accept a current/previous configuration class
    * the `downgrade_to_v1_config()` method should return a current/previous configuration class
5. change the signature of the `MetadataRecord` class to use the new configuration class
6. change the `make_config()` method of the `MetadataRecord` class to return the new configuration class
7. update the `generate_schemas()` method in the [Test App](#testing-flask-app) to generate distribution schemas for
   the new schema version
8. [Generate configuration schemas](#generating-configuration-schemas)
9. add a script line to the `publish-schemas-stage` and `publish-schemas-prod` jobs in `.gitlab-ci.yml`, to publish
   the distribution schema for the new schema version within the BAS Metadata Standards website
10. define a series of test configurations (e.g. minimal, typical and complete) for generating test records in
    `tests/resources/configs/` e.g. `tests/resources/configs/foo_v1_standard.py`
     * note that the version in these file names is for the version of the standard, not the configuration
     * new config objects will be made within this file that relate to the new configuration version
     * initially these new config objects can inherit from test configurations for the current/previous version
11. update the `generate_json_test_configs()` method in [Test App](#testing-flask-app) to generate JSON versions of
    each test configuration
12. [Capture test JSON record configurations](#capturing-test-configurations-as-json)
13. update the route for the standard in [Test App](#testing-flask-app) (e.g. `standard_foo_v1`) to:
     1. upgrade configs for the old/current version of the standard (as the old/current MetadataRecordConfig class will
        now be incompatible with the updated MetadataRecord class)
     2. include configs for the new config version of the standard
14. update the `capture_test_records()` method in [Test App](#testing-flask-app) to capture test records for the new
    test configurations
15. [Capture test XML records](#capturing-test-records)

16. add test cases for the new `MetadataRecordConfig` class in the relevant module in `tests.bas_metadata_library`:
    * `test_invalid_configuration_v2`
    * `test_configuration_v2_from_json_file`
    * `test_configuration_v2_from_json_string`
    * `test_configuration_v2_to_json_file`
    * `test_configuration_v2_to_json_string`
    * `test_configuration_v2_json_round_trip`
    * `test_parse_existing_record_v2`
    * `test_lossless_conversion_v2`
17. change all test cases to target record configurations for the new version
18. update the `test_record_schema_validation_valid` and `test_record_schema_validation_valid` test cases, which test
    the XML/XSD schema for the standard, not the configuration JSON schema
19. update the existing `test_lossless_conversion_v1` test case to upgrade v1 configurations to v2, as the
    `MetadataRecord` class will no longer be compatible with the `MetadataRecordConfigV1` class
20. update the [Supported configuration versions](/README.md#supported-configuration-versions) section of the README
     * add the new schema version, with a status of 'alpha'
21. update the encode/decode subsections in the [Usage](/README.md#usage) section of the README to use the new
    `RecordConfig` class
22. if the lead standard (ISO 19115) is being updated also update these [Usage](/README.md#usage) subsections:
    * [Loading a record configuration from JSON](/README.md#loading-a-record-configuration-from-json)
    * [Dumping a record configuration to JSON](/README.md#dumping-a-record-configuration-to-json)
    * [Validating a record](/README.md#validating-a-record)
    * [Validating a record configuration](/README.md#validating-a-record-configuration)
23. add a subsection to the [Usage](/README.md#usage) section of the README explaining how to upgrade and downgrade a
    configuration between the old and new versions
24. Update the change log to reference the creation of the new schema version, referencing the summary issue

### Step 2: Make changes

Second, iteratively introduce changes to the new configuration, adding logic to convert between the old and new
configurations as needed. This logic will likely be messy and may target specific known use-cases. This is acceptable on
the basis these methods will be relatively short-lived.

1. as changes are made, add notes and caveats to the upgrade/downgrade methods in code, and summarise any
   significant points in the [Usage](/README.md#usage) instructions as needed (e.g. that the process is lossy)
2. if changes are made to the minimal record configuration, update examples in the README
3. if circumstances where data can't be mapped between schemas, consider raising exception in methods for manual
  conversion

### Step 3: Release as experimental version

... release the new configuration version as experimental for the standard.

### Step 4: Mark as stable version

1. update the [Supported configuration versions](/README.md#supported-configuration-versions) section of the README
     * update the new/current schema version with a status of 'stable'
     * update the old schema version with a status of 'deprecated'

### Step 5: Retire previous version

1. create an issue for retiring the old schema version
2. delete the previous metadata configuration JSON schema from `bas_metadata_library.schemas.src`
   e.g. `bas_metadata_library.schemas.src.foo_v1.json`
3. delete the configuration classes for the standard in `bas_metadata_library.standards`
    * i.e. in `bas_metadata_library.standards.foo_v1/__init__.py`, delete `MetadataRecordConfigV1`
4. in the new/current configuration class, remove `upgrade_to_v1_config()` and `downgrade_to_v2_config()` methods
5. delete the `upgrade_to_v1_config()` and `downgrade_to_v2_config()` methods from the standards `utils` module
6. delete the test configurations from `tests/resources/configs` (`minimal_record_v1`, etc. in `foo_v1.py`)
7. delete corresponding JSON configurations from `tests/resources/configs` (e.g. in `tests/resources/configs/foo_v1/`)
8. delete corresponding test records from `tests/resources/records` (e.g. in `tests/resources/records/foo_v1/`)
9. update the relevant `_generate_record_*()` method in the [Test App](#testing-flask-app)
10. update the `_generate_schemas()` method in the [Test App](#testing-flask-app) to remove the old schema version
11. update the `_capture_json_test_configs()` method in the [Test App](#testing-flask-app) to remove the old schema
    version
12. update the `_capture_test_records()` method in the [Test App](#testing-flask-app) to remove the old schema version
13. update the `publish-schemas-stage` and `publish-schemas-prod` jobs in `.gitlab-ci.yml`, to remove the old schema
    version
14. remove test cases for the old `MetadataRecordConfig` class in the relevant module in `tests.bas_metadata_library`:
    * `test_invalid_configuration_v1`
    * `test_configuration_v1_from_json_file`
    * `test_configuration_v1_from_json_string`
    * `test_configuration_v1_to_json_file`
    * `test_configuration_v1_to_json_string`
    * `test_configuration_v1_json_round_trip`
    * `test_parse_existing_record_v1`
    * `test_lossless_conversion_v1`
15. if applicable, remove any edge case tests for converting from the old to new/current schema version
16. update the [Supported configuration versions](/README.md#supported-configuration-versions) section of the README
     * update the old schema version with a status of 'retired'
17. remove the subsection to the [Usage](/README.md#usage) section of the README for how to upgrade and downgrade a
    configuration between the old and new/current versions
18. Update the change log to reference the removal of the new schema version, referencing the summary issue, as a
    breaking change

See [33b7509c 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/commit/33b7509cdb73525b79b1a81f7038b805769e0057)
for an example of removing a schema version.

## Generating configuration schemas

The `generate-schemas` command in the [Flask Test App](#testing-flask-app) generates
[distribution schemas from source schemas](/README.md#source-and-distribution-schemas) in
`src/bas_metadata_library/schemas/dist`.

```shell
$ FLASK_APP=tests.app poetry run flask capture-test-records
```

[`jsonref`](https://jsonref.readthedocs.io/en/latest/) is used to resolve any references in source schemas.

To add a schema for a new standard/profile:

- adjust the `schemas` list in the `_generate_schemas()` method in the [Flask Test App](#testing-flask-app)
- this list should contain dictionaries with keys for the common name of the schema (based on the common file name of
  the schema JSON file), and whether the source schema should be resolved (true) or simply copied (false)
- this should be true by default, and is only relevant to schemas that do not contain any references, as this will
  cause an error if resolved

## Setup

### Terraform

Terraform is used to provision resources required to operate this application in staging and production environments.

These resources allow [Configuration schemas](/README.md#configuration-schemas) for each standard to be accessed
externally.

Access to the [BAS AWS account 🛡️](https://gitlab.data.bas.ac.uk/WSF/bas-aws) is needed to provision these resources.

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
[BAS Terraform Remote State 🛡️](https://gitlab.data.bas.ac.uk/WSF/terraform-remote-state) project.

Remote state storage will be automatically initialised when running `terraform init`. Any changes to remote state will
be automatically saved to the remote backend, there is no need to push or pull changes.

##### Remote state authentication

Permission to read and/or write remote state information for this project is restricted to authorised users. Contact
the [BAS Web & Applications Team](mailto:servicedesk@bas.ac.uk) to request access.

See the [BAS Terraform Remote State 🛡️](https://gitlab.data.bas.ac.uk/WSF/terraform-remote-state) project for how these
permissions to remote state are enforced.

## Local development environment

Requirements:

* Python 3.9 ([pyenv](https://github.com/pyenv/pyenv) recommended)
* [Poetry](https://python-poetry.org/docs/#installation)
* Git (`brew install git`)
* Pre-commit (`pipx install pre-commit`)

Clone project:

```
$ git clone https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library.git
$ cd metadata-library
```

Install project:

```
$ poetry install
```

Install pre-commit hooks:

```
$ pre-commit install
```

## Dependencies

### Vulnerability scanning

The [Safety](https://pypi.org/project/safety/) package is used to check dependencies against known vulnerabilities.

**WARNING!** As with all security tools, Safety is an aid for spotting common mistakes, not a guarantee of secure code.
In particular this is using the free vulnerability database, which is updated less frequently than paid options.

Checks are run automatically in [Continuous Integration](#continuous-integration). To check locally:

```
$ poetry run safety scan
```

#### `lxml` dependency safety

Ruff identifies the use of `lxml` classes and methods as a security issue, specifically rule
[S320](https://docs.astral.sh/ruff/rules/suspicious-xmle-tree-usage/).

The recommendation is to use a *safe* implementation of an XML processor (`defusedxml`) that can avoid entity bombs and
other XML processing attacks. However, `defusedxml` does not offer all the methods we need, and there does not appear
to be another processor that does.

The main vulnerability this issue relates to is processing user input that can't be trusted. This is a risk that needs
to be assessed where this library is used, and not within this library in isolation. I.e. if this library is used in a
service that accepts user input, an assessment must be made whether the input is trustworthy enough, or if other
safeguards need to be put in place.

## Linting

### Ruff

[Ruff](https://docs.astral.sh/ruff/) is used to lint and format Python files. Specific checks and config options are
set in [`pyproject.toml`](./pyproject.toml). Linting checks are run automatically in
[Continuous Integration](#continuous-integration).

To check linting locally:

```
$ poetry run ruff check src/ tests/
```

To run and check formatting locally:

```
$ poetry run ruff format src/ tests/
$ poetry run ruff format --check src/ tests/
```

### Static security analysis

Ruff is configured to run [Bandit](https://github.com/PyCQA/bandit), a static analysis tool for Python.

**WARNING!** As with all security tools, Bandit is an aid for spotting common mistakes, not a guarantee of secure code.
In particular this tool can't check for issues that are only be detectable when running code.

### Editorconfig

For consistency, it's strongly recommended to configure your IDE or other editor to use the
[EditorConfig](https://editorconfig.org/) settings defined in [`.editorconfig`](./.editorconfig).

### Pre-commit hook

A set of [Pre-Commit](https://pre-commit.com) hooks are configured in
[`.pre-commit-config.yaml`](/.pre-commit-config.yaml). These checks must pass to make a commit.

To run pre-commit checks manually:

```
$ pre-commit run --all-files
```

## Tests

This library does not seek to support all possible elements and variations within each standard. Its tests are
therefore not exhaustive, nor a substitute for formal metadata validation.

### Pytest

[pytest](https://docs.pytest.org) with a number of plugins is used to test the extension. Config options are set in
[`pyproject.toml`](./pyproject.toml). Tests are run automatically in [Continuous Integration](#continuous-integration).

To run tests locally:

```
$ poetry run pytest
```

Tests are ran against an internal Flask app defined in [`tests/app.py`](./tests/app.py).

### Pytest fixtures

Fixtures should be defined in [conftest.py](./tests/conftest.py), prefixed with `fx_` to indicate they are a fixture,
e.g.:

```python
import pytest

@pytest.fixture()
def fx_test_foo() -> str:
    """Example of a test fixture."""
    return 'foo'
```

### Pytest-cov test coverage

[`pytest-cov`](https://pypi.org/project/pytest-cov/) checks test coverage. We aim for 100% coverage but don't currently
enforce this due to branching not being accounted for when originally developed. Additional exemptions are ok with good
justification:

- `# pragma: no cover` - for general exemptions
- `# pragma: no branch` - for branching exemptions (branches that can never be called but are still needed)

To run tests with coverage locally:

```
$ poetry run pytest --cov --cov-report=html
```

Where tests are added to ensure coverage, use the `cov` [mark](https://docs.pytest.org/en/7.1.x/how-to/mark.html), e.g:

```python
import pytest

@pytest.mark.cov()
def test_foo():
    assert 'foo' == 'foo'
```

### Testing Flask app

For generating and capturing test records, record configurations and schemas, an internal Flask application defined in
`tests/app.py` is used. This app:

- has routes for:
  - calling the Metadata Library to generate records from a given configuration for a standard
- has CLI commands to:
  - generate schemas for standards
  - capture record configurations as JSON
  - capture records as XML

Available routes and commands can be used listed using:

```shell
$ FLASK_APP=tests.app poetry run flask --help
```

### Test records

Test methods check individual elements are formed correctly. Comparisons against static test records are used to
test the structure of whole records for each standard. These records, from minimal through to complete usage,
defined in `tests/resources/configs/` verify basic structure, typical usage and completeness.

### Capturing test records

The `capture-test-records` command in the [Flask Test App](#testing-flask-app) generates test records for standards
encoded as JSON files in `tests/resources/records`:

```shell
$ FLASK_APP=tests.app poetry run flask capture-test-records
```

**Note:** These files will be used in tests to automatically verify element classes dump/load (encode/decode)
information from/to records correctly. These files MUST therefore be manually verified as accurate.

It is intended that this command will update pre-existing records, with differences captured in version control to aid
in manual review to ensure they are correct.

### Capturing test configurations as JSON

The `capture-json-test-configs` command in the [Flask Test App](#testing-flask-app) generate and update test
configurations for standards encoded as JSON files in `/tests/resources/configs/`:

```shell
$ FLASK_APP=tests.app poetry run flask capture-json-test-configs
```

**Note:** These files will be used in tests to automatically verify configuration classes dump/load (encode/decode)
information from/to record configurations correctly. These files MUST therefore be manually verified as accurate.

It is intended that this command will update pre-existing configurations, with differences captured in version control
to aid in manual review to ensure they are correct.

### Continuous Integration

All commits will trigger Continuous Integration using GitLab's CI/CD platform, configured in `.gitlab-ci.yml`.

## Available releases

See [README](./README.md#releases).

### Release workflow

Create a [release issue 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/new?issue[title]=x.x.x%20release&issuable_template=release)
and follow the instructions.

GitLab CI/CD will automatically create a GitLab Release based on the tag, including:

- milestone link
- change log extract
- package artefact
- link to README at the relevant tag

GitLab CI/CD will automatically trigger a [Deployment](#deployment) of the new release.

## Deployment

### Python package

This project is distributed as a Python (Pip) package available from [PyPi](https://pypi.org/project/bas-metadata-library/)

The package can also be built manually if needed:

```
$ poetry build
```

### Deployment workflow

[Continuous Deployment](#continuous-deployment) will:

- build this package using Poetry
- upload it to [PyPi](https://pypi.org/project/flask-entra-auth/)

### Continuous Deployment

Tagged commits created for [Releases](./README.md#releases) will trigger Continuous Deployment using GitLab's
CI/CD platform configured in [`.gitlab-ci.yml`](./.gitlab-ci.yml).
