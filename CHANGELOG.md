# UK Polar Data Centre (UK PDC) Metadata Record Generator

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

* Python updated to 3.8
* Switching to a mulit-stage Dockerfile using a virtual environment and non-root user
* Switching from Pip, SetupTools and Twine to Poetry

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
