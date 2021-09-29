# UK Polar Data Centre (UK PDC) Metadata Record Generator

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed [BREAKING!]

* Distributors, Formats and Transfer Options refactored to per-distributor versions
  [#87](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/87)
* Modules for standards no longer include a version (e.g. `bas_metadata_library.standards.iso_19115_2` rather than 
  `bas_metadata_library.standards.iso_19115_2_v1`)
  [#102](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/102)
* `MetadataRecordConfiguration` classes renamed to include version (e.g. `MetadataRecordConfigurationV1`)
  [#102](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/102)

### Removed [BREAKING!]

* Support for generating DOI citations automatically from DataCite API (to remove external dependencies)
  [#117](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/117)
* Support for INSPIRE and PoC UK-PDC profiles
  [#103](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/103)
* INSPIRE specific data quality measures from JSON schema
  [#107](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/107)

### Added

* ID attributes for distribution Format and Transfer Option elements
  [#108](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/108)
* Resource credit element
  [#65](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/65)
* Title, description and example meta elements to JSON schemas
  [#80](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/80)
* Version 2 configurations for ISO 19115-1 and ISO 19115-2 to support backwards incompatible schema changes
  [#102](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/102)
* Resource identification status element 
  [#77](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/77)
* Resource identification aggregation element
  [#106](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/106)

### Fixed

* Corrected `gco:nillReason` for missing data transfer formats (from `unknown` to `missing`)
  [#64](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/64)
* Configuration schema for datestamp changed to require date values rather than date-time
  [#82](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/82)
* Configuration schema for DOIs changed to require URI values rather than free-text
  [#82](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/82)
* Adding missing rust/cargo dependencies to Docker container to enable cryptography package to be built
  [#113](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/113)

### Changed

* Identifiers structure changed in v2 record configuration (`title` property is now `namespace`)
  [#105](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/105)
* Constraints structure changed in v2 record configuration
  [#81](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/81)
* Root level properties changed in v2 record configuration (resource -> identification, new metadata)
  [#109](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/109)
* Using definitions property consistently in configuration schemas
  [#115](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/115)
* Configuration schemas relocated to `schemas` module and split into source and distribution versions to avoid relying 
  on remote schemas during development
  [#101](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/101)
* README documentation improvements
  [#112](https://gitlab.data.bas.ac.uk/uk-pdc/metadata-infrastructure/metadata-generator/-/issues/112)

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

## [0.3.0] 2020-08-25

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
