# BAS Metadata Library - Development Documentation

## Setup

### Terraform

Terraform is used to provision IAM resources needed to host [Configuration schemas](/README.md#configuration-schemas)
for external access.

Access to the [BAS AWS Account 🛡️](https://gitlab.data.bas.ac.uk/WSF/bas-aws) is needed to provision these resources.

> [!Note]
> This provisioning should have already been performed (and applies globally). Any changes only need to be applied once.

```shell
# start terraform inside a docker container if not installed locally
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

- Git
- [UV](https://docs.astral.sh/uv/)
- [Pre-commit](https://pre-commit.com)

Setup:

1. install tools (`brew install git uv pre-commit`)
1. clone and setup project [1]

[1]

```shell
% git clone https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library.git
% cd metadata-library/
% pre-commit install
% uv sync --all-groups
```

## Development tasks

[Taskipy](https://github.com/taskipy/taskipy?tab=readme-ov-file#general) is used to define development tasks, such as
running tests and rebuilding distribution schemas. These tasks are akin to NPM scripts or similar concepts.

Run `task --list` (or `uv run task --list`) for available commands.

Run `task [task]` (`uv run task [task]`) to run a specific task.

See [Adding development tasks](#adding-development-tasks) for how to add new tasks.

> [!TIP]
> If offline, use `uv run --offline task ...` to avoid lookup errors trying to the unconstrained build system
> requirements in `pyproject.toml`, which is a [Known Issue](https://github.com/astral-sh/uv/issues/5190) within UV.

## Contributing

All changes except minor tweaks (typos, comments, etc.) MUST:

- be associated with an issue (either directly or by reference)
- be included in `CHANGELOG.md`

### Adding a new standard

> [!NOTE]
> This task requires significant work.

To add a new standard:

1. create a new module under `bas_metadata_library.standards`, e.g. `bas_metadata_library.standards.foo_v1/__init__.py`
1. in this module, overload the `Namespaces`, `MetadataRecordConfig` and `MetadataRecord` classes as needed
   - version the `MetadataRecordConfig` class, e.g. `MetadataRecordConfigV1`
1. create a suitable metadata configuration JSON schema in `bas_metadata_library.schemas.src`,
   e.g. `bas_metadata_library.schemas.src.foo_v1.json`
1. update the `generate_schemas` method in `app.py` to generate distribution schemas
1. add a script line to the `publish-schemas-stage` and `publish-schemas-prod` jobs in `.gitlab-ci.yml`, to publish
   the distribution schema within the BAS Metadata Standards website
1. define a series of test configurations (e.g. minimal, typical and complete) for generating test records in
   `tests.resources.configs` e.g. `tests.resources.configs.foo_v1_standard`
1. add a route in `app.py` for generating test records for the new standard
1. update the `capture_test_records` method in `app.py` to generate and save test records
1. add relevant [Tests](#testing) with methods to test each metadata element class and test records

### Adding a new element

> [!NOTE]
> These instructions are specific to the ISO 19115 metadata standards family.

1. [amend configuration schema](/README.md#configuration-schemas):
   - new or changed properties should be added to the configuration for the relevant standard (e.g. ISO 19115-1)
   - typically, this involves adding new elements to the `definitions` property and referencing these in the relevant
     parent element (e.g. to the `identification` property)
1. [generate distribution schemas](#generating-configuration-schemas)
1. amend test configs:
   - new or changed properties should be made to the relevant test record configurations in `tests.resources.configs`
   - there are different levels of configuration, from minimal to complete, which should, where possible, build on
     each other (e.g. the complete record should include all the properties and values of the minimal record)
   - the `minimum` configuration should not be changed, as all mandatory elements are already implemented
   - the `base_simple` configuration should contain elements used most of the time, that use free-text values
   - the `base_complex` configuration should contain elements used most of the time, that use URL or other
     identifier values
   - the `complete` configuration should contain examples of all supported elements, providing this still produces a
     valid record, in order to ensure high test coverage
   - where possible, configurations should be internally consistent, but this can be ignored if needed
   - values used for identifiers and other external references should use the correct form/structure but do not need
     to exist or relate to the resource described by each configuration (i.e. DOIs should be valid URLs but could be
     a DOI for another resource for example)
1. add relevant [element class](/README.md#record-element-classes):
   - new or changed elements should be added to the configuration for the relevant package for each standard
   - for the ISO 19115 family of standards, element classes should be added to the `iso_19115_common` package
   - the exact module to use within this package will depend on the nature of the element being added, but in general,
     elements should be added to the module of their parent element (e.g. `data_identification.py` for elements
     under the `identification` record configuration property), elements used across a range of elements should be
     added to the `common_elements.py` module
   - remember to include references to new element class in the parent element class (in both the `make_element` and
     `make_config` methods)
1. [capture test records](#capturing-test-records)
   - initially this acts as a good way to check new or changed element classes encode configuration properties
      correctly
   - check the git status of these test records to check existing records have changed how you expect (and haven't
      changed things you didn't intend to for example)
1. [capture test JSON configurations](#capturing-test-configurations-as-json)
   - check the git status of these test configs to check they are encoded correctly from Python (i.e. dates)
1. add tests:
   - new test cases should be added, or existing test cases updated, in the relevant module within
      `tests/bas_metadata_library/`
   - for the ISO 19115 family of standards, this should be `test_standard_iso_19115_1.py`, unless the element is only
      part of the ISO 19115-2 standard
   - providing there are enough test configurations to test all the ways a new element can be used (e.g. with a simple
      text string or anchor element for example), adding a test case for each element is typically enough to ensure
      sufficient test coverage
   - where this isn't the case, it's suggested to add one or more 'edge case' test cases to test remaining code paths
      explicitly
1. check [test coverage](#pytest-cov-test-coverage):
   - for missing coverage, consider adding edge case test cases where applicable
   - coverage exemptions should be avoided wherever feasible and all exemptions must be discussed before they are added
   - where exceptions are added, they should be documented as an issue with information on how they will be addressed
      in the longer term
1. update `README.md` examples if common element:
   - this is probably best done before releasing a new version
1. update `CHANGELOG.md`
1. if needed, add name to `authors` property in `pyproject.toml`

### Adding a new schema version

<!-- pyml disable md028 -->
> [!CAUTION]
> This section is Work in Progress (WIP) and may not be complete/accurate.

> [!NOTE]
> This task requires significant work. It should be reserved for breaking or major changes to a schema.

> [!TIP]
> In these instructions, `v1` refers to the current/previous configuration version. `v2` refers to the new version.
<!-- pyml enable md028 -->

#### Step 1: Add new version

First, create a new configuration version that is identical to the current/previous version, but that sets up the
schema, objects, methods, tests and documentation needed for the new configuration, and to convert between the old
and new configurations.

1. create an issue summarising, and referencing specific issues for, changes to be made in the new schema version
1. copy the current/previous metadata configuration JSON schema from `bas_metadata_library.schemas.src`
   e.g. `bas_metadata_library.schemas.src.foo_v1.json` to `bas_metadata_library.schemas.src.foo_v2.json`
   1. change the version in:
      - the `$id` property
      - the `title` property
      - the `description` property
1. duplicate the configuration classes for the standard in `bas_metadata_library.standards`
   - i.e. in `bas_metadata_library.standards.foo_v1/__init__.py`, copy `MetadataRecordConfigV1` to `MetadataRecordConfigV2`
1. in the new configuration class, add `upgrade_to_v1_config()` and `downgrade_to_v2_config()` methods
   - the `upgrade_from_v2_config()` method should accept a current/previous configuration class
   - the `downgrade_to_v1_config()` method should return a current/previous configuration class
1. change the signature of the `MetadataRecord` class to use the new configuration class
1. change the `make_config()` method of the `MetadataRecord` class to return the new configuration class
1. update the `_generate_schemas()` method in the [Test App](#testing-flask-app) to generate distribution schemas for
   the new schema version
1. [Generate configuration schemas](#generating-configuration-schemas)
1. add a line to the `publish-schemas-stage` and `publish-schemas-prod` jobs in `.gitlab-ci.yml`, to publish
   the distribution schema for the new schema version within the BAS Metadata Standards website
1. define a series of test configurations (e.g. minimal, typical and complete) for generating test records in
    `tests.resources.configs/` e.g. `tests.resources.configs.foo_v1_standard`
   - note that the version in these file names is for the version of the standard, not the configuration
   - new config objects will be made within this file that relate to the new configuration version
1. update the `_capture_json_test_configs()` method in [Test App](#testing-flask-app) to generate JSON versions of
   each test configuration
1. [Capture test JSON record configurations](#capturing-test-configurations-as-json)
1. update the route for the standard in [Test App](#testing-flask-app) (e.g. `standard_foo_v1`) to:
   1. upgrade configs for the old/current version of the standard (as the old/current MetadataRecordConfig class will
 now be incompatible with the updated MetadataRecord class)
   1. include configs for the new config version of the standard
1. update the `capture_test_records()` method in [Test App](#testing-flask-app) to capture test records for the new
    test configurations
1. [Capture test XML records](#capturing-test-records)
1. add test cases for the new `MetadataRecordConfig` class in the relevant module in `tests.bas_metadata_library`:
   - `test_invalid_configuration_v2`
   - `test_configuration_v2_from_json_file`
   - `test_configuration_v2_from_json_string`
   - `test_configuration_v2_to_json_file`
   - `test_configuration_v2_to_json_string`
   - `test_configuration_v2_json_round_trip`
   - `test_parse_existing_record_v2`
   - `test_lossless_conversion_v2`
1. change all test cases to target record configurations for the new version
1. update the `test_record_schema_validation_valid` and `test_record_schema_validation_valid` test cases, which test
    the XML/XSD schema for the standard, not the configuration JSON schema
1. update the existing `test_lossless_conversion_v1` test case to upgrade v1 configurations to v2, as the
    `MetadataRecord` class will no longer be compatible with the `MetadataRecordConfigV1` class
1. update the [Supported configuration versions](/README.md#supported-configuration-versions) section of the README
   - add the new schema version, with a status of 'alpha'
1. update the encode/decode subsections in the [Usage](/README.md#usage) section of the README to use the new
    `RecordConfig` class and `$schema` URI
1. if the lead standard (ISO 19115) is being updated also update these [Usage](/README.md#usage) subsections:
   - [Loading a record configuration from JSON](/README.md#loading-a-record-configuration-from-json)
   - [Dumping a record configuration to JSON](/README.md#dumping-a-record-configuration-to-json)
   - [Validating a record](/README.md#validating-a-record)
   - [Validating a record configuration](/README.md#validating-a-record-configuration)
1. add a subsection to the [Usage](/README.md#usage) section of the README explaining how to upgrade and downgrade a
    configuration between the old and new versions
1. Update the change log to reference the creation of the new schema version, referencing the summary issue

#### Step 2: Make changes

Second, iteratively introduce changes to the new configuration, adding logic to convert between the old and new
configurations as needed. This logic will likely be messy and may target specific known use-cases. This is acceptable on
the basis these methods will be relatively short-lived.

1. as changes are made, add notes and caveats to the upgrade/downgrade methods in code, and summarise any
   significant points in the [Usage](/README.md#usage) instructions as needed (e.g. in the 'Information that will be
   lost when downgrading:' section)
1. if changes are made to the minimal record configuration, update examples in the README
1. if circumstances where data can't be mapped between schemas, consider raising exception in methods for manual
  conversion

#### Step 3: Release as experimental version

... release the new configuration version as experimental for the standard ...

1. update the [Supported configuration versions](/README.md#supported-configuration-versions) section of the README
   - add the new/current schema version with a status of 'experimental'

#### Step 4: Mark as stable version

1. update the [Supported configuration versions](/README.md#supported-configuration-versions) section of the README
   - update the new/current schema version with a status of 'stable'
   - update the old schema version with a status of 'deprecated'

#### Step 5: Retire previous version

1. create an issue for retiring the old schema version
1. delete the previous metadata configuration JSON schema from `bas_metadata_library.schemas.src`
   e.g. `bas_metadata_library.schemas.src.foo_v1.json`
1. delete the configuration classes for the standard in `bas_metadata_library.standards`
   - i.e. in `bas_metadata_library.standards.foo_v1/__init__.py`, delete `MetadataRecordConfigV1`
1. in the new/current configuration class, remove `upgrade_to_v1_config()` and `downgrade_to_v2_config()` methods
1. delete the `upgrade_to_v1_config()` and `downgrade_to_v2_config()` methods from the standards `utils` module
1. delete the test configurations from `tests.resources.configs` (`minimal_record_v1`, etc. in `foo_v1.py`)
1. delete corresponding JSON configurations from `tests.resources.configs` (e.g. in `tests.resources.configs.foo_v1`)
1. delete corresponding test records from `tests.resources.records` (e.g. in `tests.resources.records.foo_v1`)
1. update the relevant `_generate_record_*()` method in the [Test App](#testing-flask-app)
1. update the `_generate_schemas()` method in the [Test App](#testing-flask-app) to remove the old schema version
1. update the `_capture_json_test_configs()` method in the [Test App](#testing-flask-app) to remove the old schema
    version
1. update the `_capture_test_records()` method in the [Test App](#testing-flask-app) to remove the old schema version
1. update the `publish-schemas-stage` and `publish-schemas-prod` jobs in `.gitlab-ci.yml`, to remove the old schema
    version
1. remove test cases for the old `MetadataRecordConfig` class in the relevant module in `tests.bas_metadata_library`:
   - `test_invalid_configuration_v1`
   - `test_configuration_v1_from_json_file`
   - `test_configuration_v1_from_json_string`
   - `test_configuration_v1_to_json_file`
   - `test_configuration_v1_to_json_string`
   - `test_configuration_v1_json_round_trip`
   - `test_parse_existing_record_v1`
   - `test_lossless_conversion_v1`
1. if applicable, remove any edge case tests for converting from the old to new/current schema version
1. update the [Supported configuration versions](/README.md#supported-configuration-versions) section of the README
   - update the old schema version with a status of 'retired'
1. remove the subsection to the [Usage](/README.md#usage) section of the README for how to upgrade and downgrade a
    configuration between the old and new/current versions
1. Update the change log to reference the removal of the new schema version, referencing the summary issue, as a
    breaking change

See [33b7509c 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/commit/33b7509cdb73525b79b1a81f7038b805769e0057)
for an example of removing a schema version.

### Adding a new profile

> [!CAUTION]
> This section is Work in Progress (WIP) and may not be complete/accurate.

See https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/250 for an example of adding
a profile.

### Generating configuration schemas

To generate [distribution schemas from source schemas](/README.md#source-and-distribution-schemas), run the
`generate-schemas` [Development Task](#development-tasks), which uses the internal [Flask Test App](#testing-flask-app).

> [!TIP]
> [`jsonref`](https://jsonref.readthedocs.io/en/latest/) is used to resolve any references in source schemas.

To add a schema for a new standard/profile:

- adjust the `schemas` list in the `_generate_schemas()` method in the [Flask Test App](#testing-flask-app)
- this list should contain dictionaries with keys for the common name of the schema (based on the common file name of
  the schema JSON file), and whether the source schema should be resolved (true) or simply copied (false)
- this should be true by default, and is only relevant to schemas that do not contain any references, as this will
  cause an error if resolved

### Removing a standard

> [!CAUTION]
> This section is Work in Progress (WIP) and may not be complete/accurate.

See [#266 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/266) for an
example of removing a standard.

### Adding development tasks

See the [Taskipy](https://github.com/taskipy/taskipy?tab=readme-ov-file#adding-tasks) documentation.

## Python version

The minimum Python version is 3.9 for compatibility with older BAS IT base images.

## Dependencies

### Vulnerability scanning

The [Safety](https://pypi.org/project/safety/) package checks dependencies for known vulnerabilities.

> [!WARNING]
> As with all security tools, Safety is an aid for spotting common mistakes, not a guarantee of secure code.
> In particular this is using the free vulnerability database, which is updated less frequently than paid options.

Checks are run automatically in [Continuous Integration](#continuous-integration).

> [!TIP]
> To check locally run the `safety` [Development Task](#development-tasks).

### Updating dependencies

- create an issue and switch to branch
- run `uv tree --outdated --depth=1` to list outdated packages
- follow https://docs.astral.sh/uv/concepts/projects/sync/#upgrading-locked-package-versions
- note upgrades in the issue
- review any major/breaking upgrades
- run [Tests](#testing) manually
- commit changes

## Linting

### Ty

[Ty](https://docs.astral.sh/ty/) is used for static type checking in library classes (not tests, etc.) with default
options. Type checks are run automatically in [Continuous Integration](#continuous-integration) and
the [Pre-Commit Hook](#pre-commit-hook).

<!-- pyml disable md028 -->
> [!NOTE]
> Ty is an experimental tool and may report false positives. Type checking may be removed if it becomes a burden.

> [!TIP]
> To check types manually run the `types` [Development Task](#development-tasks).
<!-- pyml enable md028 -->

### Ruff

[Ruff](https://docs.astral.sh/ruff/) is used to lint and format Python files. Specific checks and config options are
set in [`pyproject.toml`](/pyproject.toml). Linting checks are run automatically in
[Continuous Integration](#continuous-integration) and the [Pre-Commit Hook](#pre-commit-hook).

> [!TIP]
> To check linting manually run the `lint` [Development Task](#development-tasks), for formatting run the `format` task.

### Static security analysis

[Ruff](#ruff) is configured to run [Bandit](https://github.com/PyCQA/bandit), a static analysis tool for Python.

> [!WARNING]
> As with all security tools, Bandit is an aid for spotting common mistakes, not a guarantee of secure code.
> In particular this tool can't check for issues that are only be detectable when running code.

### Markdown

[PyMarkdown](https://pymarkdown.readthedocs.io/en/latest/) is used to lint Markdown files. Specific checks and config
options are set in [`pyproject.toml`](/pyproject.toml). Linting checks are run automatically in
[Continuous Integration](#continuous-integration) and the [Pre-Commit Hook](#pre-commit-hook).

> [!TIP]
> To check linting manually run the `markdown` [Development Task](#development-tasks).

Wide tables will fail rule `MD013` (max line length). Wrap such tables with pragma disable/enable exceptions:

```markdown
<!-- pyml disable md013 -->
| Header | Header |
|--------|--------|
| Value  | Value  |
<!-- pyml enable md013 -->
```

Stacked admonitions will fail rule `MD028` (blank lines in blockquote) as it's ambiguous whether a new blockquote has
started where another element isn't inbetween. Wrap such instances with pragma disable/enable exceptions:

```markdown
<!-- pyml disable md028 -->
> [!NOTE]
> ...

> [!NOTE]
> ...
<!-- pyml enable md028 -->
```

### Editorconfig

For consistency, it's strongly recommended to configure your IDE or other editor to use the
[EditorConfig](https://editorconfig.org/) settings defined in `.editorconfig`.

### Pre-commit hook

A [Pre-Commit](https://pre-commit.com) hook is configured in `.pre-commit-config.yaml`.

To update Pre-Commit and configured hooks:

```shell
% pre-commit autoupdate
```

> [!TIP]
> To run pre-commit checks against all files manually run the `pre-commit` [Development Task](#development-tasks).

## Testing

> [!Important]
> This library does not, and cannot, support all possible elements and variations within each standard. Its tests are
> therefore not exhaustive, and reflects the subset of each standard needed for use-cases within BAS.

### Pytest

[pytest](https://docs.pytest.org) with a number of plugins is used for testing the application. Config options are set
in `pyproject.toml`. Tests are defined in the `tests` package and use an internal [Flask App](#testing-flask-app).

Tests are run automatically in [Continuous Integration](#continuous-integration).

<!-- pyml disable md028 -->
> [!TIP]
> To run tests manually run the `test` [Development Task](#development-tasks).

> [!TIP]
> To run a specific test:
>
> ```shell
> % uv run pytest tests/path/to/test_module.py::<class>.<method>
> ```
<!-- pyml enable md028 -->

### Pytest fast fail

If a test run fails with a `NotImplementedError` exception run the `test-reset` [Development Task](#development-tasks).

This occurs where:

- a test fails and the failed test is then renamed or parameterised options changed
- the reference to the previously failed test has been cached to enable the `--failed-first` runtime option
- the cached reference no longer exists triggering an error which isn't handled by the `pytest-random-order` plugin

Running this task clears Pytest's cache and re-runs all tests, skipping the `--failed-first` option.

### Pytest fixtures

Fixtures SHOULD be defined in `tests.conftest`, prefixed with `fx_` to indicate they are a fixture when used in tests.
E.g.:

```python
import pytest

@pytest.fixture()
def fx_foo() -> str:
    """Example of a test fixture."""
    return 'foo'
```

### Pytest-cov test coverage

[`pytest-cov`](https://pypi.org/project/pytest-cov/) checks test coverage. We aim for 100% coverage but exemptions are
fine with good justification:

- `# pragma: no cover` - for general exemptions
- `# pragma: no branch` - where a conditional branch can never be called

[Continuous Integration](#continuous-integration) will check coverage automatically.

<!-- pyml disable md028 -->
> [!TIP]
> To check coverage manually run the `test-cov` [Development Task](#development-tasks).

> [!TIP]
> To run tests for a specific module locally:
>
> ```shell
> % uv run pytest --cov=lantern.some.module --cov-report=html tests/lantern_tests/some/module
> ```
<!-- pyml enable md028 -->

Where tests are added to ensure coverage, use the `cov` [mark](https://docs.pytest.org/en/7.1.x/how-to/mark.html), e.g:

```python
import pytest

@pytest.mark.cov()
def test_foo():
    assert 'foo' == 'foo'
```

### Testing Flask app

An internal Flask app is used to generate and capture test records, record configurations and schemas.

It is defined in `tests/app` and has:

- routes for:
  - calling the Metadata Library to generate records from a given configuration for a standard
- CLI commands to:
  - generate schemas for standards
  - capture record configurations as JSON
  - capture records as XML

Available routes and commands can be used listed using:

```shell
$ FLASK_APP=tests.app uv run flask --help
```

### Test records

Test methods check individual elements are formed correctly. Comparisons are also made against static test records to
check the structure of whole records for each standard are also formed correctly. These records, from minimal through
to 'complete' usage (against our supported subsets of standards), are defined in `tests.resources.configs/`.

### Capturing test records

To generate test records for standards encoded as JSON files in `tests.resources.records` run the `capture-test-records`
[Development Task](#development-tasks), which uses the internal [Flask Test App](#testing-flask-app).

> [!IMPORTANT]
> These records check element classes dump/load (encode/decode) information from/to records correctly. They MUST be
> manually verified as accurate.

It is intended that this command will update pre-existing records, with differences reviewed in version control to aid
in this manual verification.

### Capturing test configurations as JSON

To generate and update test configurations for standards encoded as JSON files in `tests.resources.configs`, run the
`capture-json-test-configs` [Development Task](#development-tasks), which uses the internal
[Flask Test App](#testing-flask-app).

> [!IMPORTANT]
> These records check element classes dump/load (encode/decode) information from/to records correctly. They MUST be
> manually verified as accurate.

It is intended that this command will update pre-existing records, with differences reviewed in version control to aid
in this manual verification.

### Continuous Integration

All commits will trigger Continuous Integration using GitLab's CI/CD platform, configured in `.gitlab-ci.yml`.

## Releases

See [README](./README.md#releases) for available releases.

### Release workflow

Create a [release issue 🛡️](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/new?issue[title]=x.x.x%20release&issuable_template=release)
and follow its instructions.

Creating a tag will automatically trigger a [Deployment](#deployment), which will trigger a GitLab Release, including:

- a milestone link
- the change log extract taken from `CHANGELOG.md`
- a package artefact link
- a `README.md` link at the relevant tag

## Deployment

### Python package

This project is distributed as a Python (Pip) package available from [PyPi](https://pypi.org/project/bas-metadata-library/)

> [!TIP]
> To build the package manually run the `build` [Development Task](#development-tasks).

### Deployment workflow

Follow the [Release Workflow](#release-workflow) to trigger a deployment, which will:

- build the [Python package](#python-package)
- upload it to [PyPi](https://pypi.org/project/bas-metadata-library/)

### Continuous Deployment

Tagged commits created for [Releases](#releases) will trigger Continuous Deployment using GitLab's
CI/CD platform configured in [`.gitlab-ci.yml`](./.gitlab-ci.yml).
