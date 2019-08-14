# UK Polar Data Centre (UK PDC) Metadata Record Generator

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Removed [BREAKING]

* support for `gmd:UseConstraints` elements

### Added

* adding CrossRef support for DOI citations
* support for `gmd:useLimitation` elements
* documenting not to use HTML entities in input
* documenting how to use this project to generate an ISO 19115 record
* test case to ensure unicode entities are encoded correctly in XML
* `capture-test-records` command to streamline updating static test records
* documentation on how tests are used for this library

### Fixed

* correcting ISO 19115 service namespace to use ISO hosted schema rather an Inspire draft
* correcting ISO 19115 namespaces to use HTTPS endpoints
* correcting test for non-Anchor copyright elements

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

