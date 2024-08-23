# BAS Metadata Library - Change log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed [BREAKING!]

* Minimum Python version updated to 3.9
  [#211](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/211)

### Added

* Pre-commit hook
  [#222](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/222)
* ISBN identifier example to complete ISO 19115 test record
  [#219](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/219)

### Fixed

* Updating README examples to reflect V3 config changes
  [#215](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/205)
* JSON indenting when dumping record configurations for ISO 19115 standards
  [#214](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/214)
* Including static schemas without making a Python module
  [#226](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/226)

### Changed

* Upgraded project dependencies
  [#211](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/211)
* Updated `pytest` configuration (fast fail, retry failed test first, randomise tests by default)
  [#223](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/223)
* Refactored internal / testing Flask app
* Updated project documentation
  [#225](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/225)


### Removed

* Unused `requests`, `tomlkit` and `pytest-flask` dependencies
  [#211](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/211)

## 0.9.1 - 2022-10-01

### Fixed

* Assumption that existing records would have extent identifiers
  [#209](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/209)

## 0.9.0 - 2022-10-01

### Added

* Version 3 configurations for ISO 19115-1 and ISO 19115-2 to support backwards incompatible schema changes
  [#182](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/182)
* Documentation on how to add a new configuration version for an existing standard
  [#196](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/196)
* Permissions configuration property within resource constraints element
  [#191](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/191)
* Resource format element
  [#66](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/66)
* Other Citation Details element
  [#184](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/184)
* XML ID attribute (bounding extent) added to geographic extent for consistency with temporal extent
  [#189](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/189)
* Adopting extended ISO 19115-3 keyword type list in ISO 19115 V3 configuration schema
  [#71](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/71)

### Fixed

* Updating Poetry install method and location in CI/CD image
  [#208](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/208)
* Order of keys in ISO 19115 decoded configuration dictionaries
  [#200](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/200)
* Removing required citation usage constraint in test record configurations
  [#187](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/187)
* Removing the need to run Flask app separately when capturing test records
  [#197](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/197)
* Workaround for loading schema path for test standard
  [#179](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/179)
* Outdated reference to 'master' branch in CI config
  [#198](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/198)

### Changed

* Adjusting lineage configuration property from string to an object in preparation for adding lineage sources
  [#73](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/73)
* Switching to new GCMD keywords URL
  [#186](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/186)
* Metadata (title, description) updated in existing schemas made clearer
  [#194](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/194)
* Refactoring distribution format to use a new common format element alongside #66
  [#180](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/180)
* Retiring 'safe' test record configurations (all configurations are now safe)
  [#193](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/193)
* Improving consistency of ISO 19115 schema properties using definitions
  [#192](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/192)
* JSON Schema `$schema` property now required in metadata configurations
  [#129](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/129)
* Distribution options now incorporate distributor element to create a flat config structure
  [#181](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/181)

## 0.8.0 - 2022-01-13 [BREAKING!]

### Changed [BREAKING!]

* Project path (to `metadata-library`) and branch updated (to `main`)
  [#142](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/142)
* Project dependencies updated - now requires 3.6.2 as a minimum runtime
  [#122](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/122)
* Switching from Docker to Poetry managed virtual environments for local development
  [#148](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/148)
* Removed option to disable XML declaration when encoding a record into XML
  [#140](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/140)
* Partial dates should be expressed directly in JSON encodings of configuration files, not using `date_precision`
  [#137](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/137)

### Removed [BREAKING!]

* Removing support for deprecated ISO 19115 V1 record configuration
  [#116](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/116)

### Added

* GitLab issue template
  [#177](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/177)
* Flake8 Python linting, with various extensions
  [#168](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/168)
* Internal Flask command to capture all test configurations as JSON files for testing load/dump methods
  [#169](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/169)
* Basic linting for JSON Schema source files
  [#170](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/170)
* Basic package vulnerability checks
  [#166](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/166)
* Schema validation for ISO 19115 standards
  [#61](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/61)
* Base methods for XML schema validation
  [#61](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/61)
* Protocol element
  [#68](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/68)

### Fixed

* Spatial representation (scale) element used incorrect ISO elements
  [#155](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/155)
* Spatial extent element used incorrect structure where multiple type of spatial extent where used
  [#156](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/156)
* Order of ISO elements to match sequence proscribed by XML schema
  [#157](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/157)
* Element used for browse graphic IDs
  [#158](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/158)
* XML IDs for distribution format and transfer option elements
  [#159](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/159)
* Element used for aggregation identifier
  [#160](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/160)
* Disabling PyPi testing releases to avoid version clashes when merging into master branch
  [#153](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/153)
* Missing scope code options in ISO 19115 JSON config
  [#162](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/162)
* Missing JSON dump method for 19115-2 standard
  [#163](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/163)
* Internal API responses used the wrong return type (Exception instead of String)
  [#165](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/165)
* Path to configuration schemas in Continuous Deployment
  [#167](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/167)
* Indentation inconsistency between JSON dump and dumps in MetadataRecordConfig class
  [#174](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/174)
* Package builds for branches and `main` branch are correctly unversioned
  [#178](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/178)

### Changed

* Adopting new `limportlib.files` method
  [#173](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/173)
* Refactoring commands from `manage.py` to `app.py`
  [#146](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/146)
* Relocating library under a source (`src/`) directory
  [#147](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/147)
* Relocating Terraform provisioning to support directory
  [#164](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/164)

## 0.7.1 - 2021-12-12

### Fixed

* Incorrect namespace for IEC 61174:2015 standard
  [#150](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/150)
* Added logic to prevent RTZP test files being updated necessarily
  [#151](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/143)

## 0.7.0 - 2021-12-09 [BREAKING!]

### Changed [BREAKING!]

* Splitting IEC 61174 standards into separate modules (61174-0, 61174-1)
  [#144](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/143)

### Fixed

* Incorrect casting of IEC 61174 waypoint position lat/lon values to integers instead of floats
  [#143](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/143)

## 0.6.0 - 2021-12-07

### Added

* Initial support for IEC PAS 61174 standards (RTZ route planning)
  [#139](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/139)

## 0.5.0 - 2021-12-02

### Fixed

* Adding missing JSON dump/dumps methods to configuration classes
  [#135](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/135)

## 0.5.0-rc.5 - 2021-11-22

### Fixed

* Temporal extents in V1 record configurations may not have been date objects but direct values
  [#134](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/132)
* Python package version inconsistency
  [#133](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/133)

## 0.5.0-rc.4 - 2021-11-22

### Fixed

* Parsing year only dates in a JSON record configuration
  [#132](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/132)

## 0.5.0-rc.3 - 2021-11-20

### Fixed

* JSON Schema inheritance fixed (`iso-19115-2-v2.json` inherited `iso-19115-2-v1.json` rather than `iso-19115-1-v2.json`)
  [#131](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/131)

## 0.5.0-rc.2 - 2021-11-20

### Fixed

* `$schema` property was inadvertently blocked in configuration objects
  [#128](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/128)
* Errors in README quick-start example
  [#127](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/127)

## 0.5.0-rc.1 - 2021-11-17

### Fixed

* Switched to direct package versioning to avoid errors parsing pre-release versions
  [#124](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/124)

### Removed

* Unnecessary GitLab CD job for releases
  [#125](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/125)

## 0.5.0-rc.0 - 2021-11-17 [BREAKING!]

### Changed [BREAKING!]

* Re-licencing project under the MIT licence
  [#121](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/121)
* Dates refactored to use properties for each date type, rather than an array of objects containing a date type
  [#99](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/99)
* Distributors, Formats and Transfer Options refactored to per-distributor versions
  [#87](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/87)
* Modules for standards no longer include a version (e.g. `bas_metadata_library.standards.iso_19115_2` rather than
  `bas_metadata_library.standards.iso_19115_2_v1`)
  [#102](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/102)
* `MetadataRecordConfiguration` classes renamed to include version (e.g. `MetadataRecordConfigurationV1`)
  [#102](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/102)

### Removed [BREAKING!]

* Support for generating DOI citations automatically from DataCite API (to remove external dependencies)
  [#117](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/117)
* Support for INSPIRE and PoC UK-PDC profiles
  [#103](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/103)
* INSPIRE specific data quality measures from JSON schema
  [#107](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/107)

### Added

* Geographic extent descriptions/identifiers
  [#89](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/89)
* Resource purpose element
  [#70](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/70)
* Resource graphic overview element
  [#72](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/72)
* Support for loading record configurations from JSON files or strings
  [#95](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/95)
* Support for disabling the XML declaration in encoded documents (needed for CSW transactions)
  [#76](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/76)
* ID attributes for distribution Format and Transfer Option elements
  [#108](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/108)
* Resource credit element
  [#65](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/65)
* Title, description and example meta elements to JSON schemas
  [#80](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/80)
* Version 2 configurations for ISO 19115-1 and ISO 19115-2 to support backwards incompatible schema changes
  [#102](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/102)
* Resource identification status element
  [#77](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/77)
* Resource identification aggregation element
  [#106](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/106)
* Updated project Python dependencies
  [#119](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/119)

### Fixed

* Adding missing position property for responsible parties
  [#63](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/63)
* Correct Python typing for MetadataRecord.record property
  [#120](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/120)
* Adding missing tests for code coverage
  [#111](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/111)
* Configuration schema for temporal extent structure to allow date precision qualifier to be set
  [#99](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/99)
* Corrected `gco:nillReason` for missing data transfer formats (from `unknown` to `missing`)
  [#64](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/64)
* Configuration schema for datestamp changed to require date values rather than date-time
  [#82](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/82)
* Configuration schema for DOIs changed to require URI values rather than free-text
  [#82](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/82)
* Adding missing rust/cargo dependencies to Docker container to enable cryptography package to be built
  [#113](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/113)

### Changed

* Addressing test coverage exemptions
  [#111](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/111)
* Identifiers structure changed in v2 record configuration (`title` property is now `namespace`)
  [#105](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/105)
* Constraints structure changed in v2 record configuration
  [#81](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/81)
* Root level properties changed in v2 record configuration (resource -> identification, new metadata)
  [#109](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/109)
* Using definitions property consistently in configuration schemas
  [#115](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/115)
* Configuration schemas relocated to `schemas` module and split into source and distribution versions to avoid relying
  on remote schemas during development
  [#101](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/101)
* README documentation improvements
  [#112](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-library/-/issues/112)

## [0.4.0] 2021-06-30

### Fixed

* README whitespace
* Docker Compose command

### Changed

* Scope code, code list changed to ISO 19115-3 source
* Updating copyright dates

## [0.3.1] 2020-10-30

### Fixed

* XPaths that select elements by their index position (e.g. 2nd instance)
* Datestamps being incorrectly encoded as datetimes rather than dates
* Distribution format versions are decoded using the correct key (`version` instead of `value`)
* Incorrect character encoding term for UTF-8 (`utf-8` instead of `utf8`)

### Changed

* Updated minimal usage example

## [0.3.0] 2020-08-25 [BREAKING!]

### Changed [BREAKING!]

* Namespace for ISO 19115(-0) changed from `bas_metadata_library.standards.iso_19115_v1` to
  `bas_metadata_library.standards.iso_19115_1_v1`

### Added

* Including PyCharm setting in version control, including run/debug/test configurations
* CD job to create a GitLab release for each tag with link to Python package
* Ability to generate configuration objects from existing metadata records
* Support for Research Organisation Registry (ROR) identifiers
* Support for ISO 19115-2 standard

### Fixed

* incorrect DOI used in tests
* incorrect minimal record configuration for ISO 19115 standards family

### Changed

* Python dependencies updated (notably `lxml`)
* Switching to a multi-stage Dockerfile using a virtual environment and non-root user
* Switching from Pip, SetupTools and Twine to Poetry
* Using scoped API tokens to upload packages to PyPi in CD
* Updating project licence years
* Switching from Flake8 to Black
* Switching from UnitTest to PyTest and refactoring tests
* Extracted metadata configuration JSON Schemas to standalone files

### Removed

* Synk monitoring

## [0.2.2] 2019-08-19

### Fixed

* Recording missing requests dependency

### Changed

* Removed 'funder' contact from examples as per Metadata Standards project decision not to include these for awards

## [0.2.1] 2019-08-17

### Fixed

* updated configuration schema references to use production metadata standards website
* correcting CD to generate configuration schemas for tagged releases as well as master branch commits

## [0.2.0] 2019-08-17 [BREAKING!]

### Removed [BREAKING]

* support for `gmd:UseConstraints` elements

### Added

* support for UK PDC Discovery profile for ISO 19115 and Inspire
* support for custom access and use constraints
* support for `gmd:useLimitation` elements
* CrossRef support for DOI citations
* documenting not to use HTML entities in input
* documenting how to use this project to generate an ISO 19115 record
* test case to ensure unicode entities are encoded correctly in XML
* `capture-test-records` command to streamline updating static test records
* documentation on how tests are used for this library
* custom Flask command to output internal configuration JSON schemas
* copying internal configuration JSON schemas to Metadata Standards website as part of CD

### Fixed

* correcting support for ISO distribution info elements that only contain distributors
* correcting ISO 19115 service namespace to use ISO hosted schema rather an Inspire draft
* correcting ISO 19115 namespaces to use HTTPS endpoints
* correcting test for non-Anchor copyright elements

### Changed

* replaced Gemini typical record configuration with minimal Inspire configuration (validated against Inspire validator)

## [0.1.1] 2019-07-18

### Fixed

* Adding missing ID to `InspireLimitationsOnPublicAccess` access constraint elements
* The wrong code list was checked for ResponsibleParty roles
* Roles were not correctly outputted in cited ResponsibleParty elements
* Incorrect namespace used for OnlineResource FunctionCode test
* OnlineResources were incorrectly placed in ResponsibleParties, rather than inside a ContentInfo element [#33]
* Controlled titles in responsible parties (ISNI and ORCID) following
  [uk-pdc/metadata-infrastructure/metadata-standards#92]
* Adding better URL for netCDF MIME type
* Adding missing change log header

## [0.1.0] 2019-06-28

### Added

* Initial version with support for ISO 19115
